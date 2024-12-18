from sqlite3 import IntegrityError
import pytest

from querys import create_board,get_board,get_color,update_board,update_color
from models.board import BoardTable, BoardValidationError

def test_create_board(test_db):
    
    #Caso 1: Crear un tablero correctamente.
    create_board(id_game=1,db=test_db)
    tab = test_db.query(BoardTable).filter_by(id_game=1).first()
    assert tab is not None
    
    #Caso 2: Intentar introducir el mismo id_game.
    try:
        create_board(id_game=1, db=test_db)
    except IntegrityError:
        #Deberia ocurrir un rollback
        pass
    count = test_db.query(BoardTable).count()
    assert count == 1

def test_get_color(test_db):

    #Color no se puede modificar todavia.
    create_board(id_game=1,db=test_db)
    tab = test_db.query(BoardTable).filter_by(id_game=1).first()
    assert tab.color == "NOT" == get_color(1,test_db)

def test_get_board(test_db):

    #Comprobar que los board del metodo y de la tabla son iguales.
    create_board(id_game=1,db=test_db)
    tab = test_db.query(BoardTable).filter_by(id_game=1).first()
    assert comp_boards(tab.get_board(), get_board(1,test_db))

def test_update_board(test_db):
    BoardValidationError()
    #Caso 0:
    success=[['R','R','R','R','R','R'],
            ['R','R','R','G','G','G'],
            ['G','G','G','G','G','G'],
            ['B','B','B','B','B','B'],
            ['B','B','B','Y','Y','Y'],
            ['Y','Y','Y','Y','Y','Y']]

    #Caso 1: Tratando de insertar colores imposibles.
    error1=[['Z','R','R','R','R','R'],
            ['R','Z','R','G','G','G'],
            ['G','G','Z','G','G','G'],
            ['B','B','B','Z','B','B'],
            ['B','B','B','Y','Z','Y'],
            ['Y','Y','Y','Y','Y','Z']]
    
    #Caso 2: No hay la misma cantidad de (R,G,B,Y).
    error2=[['R','R','R','R','R','R'],
            ['R','R','R','R','R','R'],
            ['G','G','G','G','G','G'],
            ['B','B','B','B','B','B'],
            ['B','B','B','Y','Y','Y'],
            ['Y','Y','Y','Y','Y','Y']]
    
    #Caso 3: No es un tablero valido de 6x6 en las columnas.
    error3=[['R','R','R','R','R','R','R'],
            ['R','R','R','R','R','R','G'],
            ['G','G','G','G','G','G','B'],
            ['B','B','B','B','B','B','Y'],
            ['B','B','B','Y','Y','Y'],
            ['Y','Y','Y','Y','Y','Y']]
    
    #Caso 4: No es un tablero valido de 6x6 en las filas.
    error4=[['R','R','R','R','R','R'],
            ['R','R','R','R','R','R'],
            ['G','G','G','G','G','G'],
            ['B','B','B','B','B','B'],
            ['B','B','B','Y','Y','Y'],
            ['Y','Y','Y','Y','Y','Y'],
            ['R','R','R','R','R','R'],
            ['R','R','R','R','R','R'],
            ['G','G','G','G','G','G'],
            ['B','B','B','B','B','B'],
            ['B','B','B','Y','Y','Y'],
            ['Y','Y','Y','Y','Y','Y']]
    
    #C0
    create_board(id_game=1,db=test_db)
    update_board(1,success,test_db)
    assert comp_boards(success, get_board(1,test_db))
    

    #C1: Deberia hacer rollback cuando intenta updatear.
    create_board(id_game=2,db=test_db)
    try:
        update_board(2,error1,test_db)
    except BoardValidationError as e:
        pass
    finally:
        assert not comp_boards(error1, get_board(2,test_db))

    #C2: Deberia hacer rollback cuando intenta updatear.
    create_board(id_game=3,db=test_db)
    try:
        update_board(3,error2,test_db)
    except BoardValidationError as e:
        pass
    finally:
        assert not comp_boards(error2, get_board(3,test_db))

    #C3: Deberia hacer rollback cuando intenta updatear.
    create_board(id_game=4,db=test_db)
    try:
        update_board(4,error3,test_db)
    except BoardValidationError as e:
        pass
    finally:
        assert not comp_boards(error3, get_board(4,test_db))

    #C4
    create_board(id_game=5,db=test_db)
    try:
        update_board(5,error4,test_db)
    except BoardValidationError as e:
        pass
    finally:
        assert not comp_boards(error4, get_board(5,test_db))

def test_color_change(test_db):
    
    create_board(id_game=1,db=test_db)
    update_color(1,"R",test_db)
    assert get_color(1,test_db) == "R"

    update_color(1,"G",test_db)
    assert get_color(1,test_db) == "G"

    update_color(1,"B",test_db)
    assert get_color(1,test_db) == "B"

    update_color(1,"Y",test_db)
    assert get_color(1,test_db) == "Y"

    try:
        update_color(1,'P',test_db)
    except BoardValidationError as e:
        pass
    finally:
        assert get_color(1,test_db) != "P"
        assert get_color(1,test_db) == "Y"

@staticmethod
def comp_boards(b1: list[list[str]], b2: list[list[str]]):
    for row1,row2 in zip(b1,b2):
        if len(row1) != len(row2):
            return False
        for col1,col2 in zip(row1,row2):
            if col1 != col2:
                return False

    return True 