from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from querys.game_queries import *
from querys.user_queries import *
from querys.board_queries import create_board
from querys.move_queries import *
from querys.figure_queries import *
from schemas.response_models import *
from utils.ws import manager
from utils.database import SERVER_DB

pre_game = APIRouter()


# Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@pre_game.get("/")
def default():
    """Mensaje predeterminado."""
    return f"El Switcher."


@pre_game.get("/active_players/{id_game}", response_model=CurrentUsers)
def get_active_players(id_game: int):
    """Devuelve los jugadors conectados a una partida."""
    return get_users(id_game=id_game,
                     db=SERVER_DB)


@pre_game.post("/create_game", response_model=ResponseCreate)
def create(e: CreateEntry):
    """Crear el juego."""
    # En caso de exito se debe retornar {id_player,id_game}.
    # Se debe crear un game_schema.Game.
    # TODO Agregar TESTs ->

    new_id_game = create_game(name=e.game_name,
                              max_players=e.max_player,
                              min_players=e.min_player,
                              db=SERVER_DB)
    
    new_user_id = create_user(name=e.owner_name,
                              id_game=new_id_game,
                              db=SERVER_DB)
    
    set_game_host(id_game=new_id_game,
                  host=new_user_id,
                  db=SERVER_DB)
    
    create_board(id_game=new_id_game,
                 db=SERVER_DB)

    return ResponseCreate(id_game=new_id_game, id_player=new_user_id)


@pre_game.post("/join_game", response_model=ResponseJoin)
def join(e: JoinEntry):
    """Unirse al juego."""

    # En caso de exito debe conectar al jugador con el servidor por WebSocket?.
    # Se deben aplicar todos los cambios a la estructura interna de la paritda.
    # TODO Testing ->
    if get_max_players(e.id_game,SERVER_DB) > get_players(e.id_game,SERVER_DB):
        
        add_player(id_game=e.id_game,
                   db=SERVER_DB)
        p_id = create_user(name=e.player_name,
                           id_game=e.id_game,
                           db=SERVER_DB)
    else:
        raise HTTPException(status_code=409, detail="El lobby está lleno.")

    return ResponseJoin(new_player_id=p_id)


@pre_game.get("/list_games", response_model=ResponseList)
def list_games():
    """Listar los juegos creados."""

    # En caso de exito debe retornar un json con todos los juegos disponibles.
    # TODO Testing ->
    g_list = listing_games(SERVER_DB)

    return ResponseList(games_list=g_list)


@pre_game.post("/start_game/{id_game}")
async def start(id_game: int):
    """Empezar un juego."""

    # En caso de exito debe iniciar la partida posteriormente sera implementado.
    # Actualizar los datos de la partida para que no se siga listando como disponible para unirse.
    # Tiene que repartir las cartas a todos los jugadores.
    # Tiene que cambiar el estado a "Playing".
    # Tiene que inicializar el tablero randomizado.
    # Tiene que avisar a todos los clientes.

    if get_players(id_game,SERVER_DB) >= get_min_players(id_game,SERVER_DB):
        
        set_game_state(id_game=id_game,
                       state="Playing",
                       db=SERVER_DB)
        
        first = set_users_turn(id_game=id_game,
                               players=get_players(id_game, SERVER_DB),
                               db=SERVER_DB)
        
        await manager.broadcast(f"GAME_STARTED {first}", id_game)
    
    else:
        raise HTTPException(status_code=409, detail="El lobby no alcanzo su capacidad minima para comenzar.")
    
    for i in range(1, 8):
        create_move(f"mov{i}", id_game, SERVER_DB)
    
    easy_figures = []
    hard_figures = []
    
    for _ in range(2):
        for i in range(1, 8):
                easy_figures.append((f"fige{i:02d}"))     
        for i in range(1,19):     
                hard_figures.append((f"fig{i:02d}"))
                   
    random.shuffle(easy_figures)
    random.shuffle(hard_figures)
    
    for player in range(get_players(id_game, SERVER_DB)):
        
        for _ in range(round(14/get_players(id_game, SERVER_DB))):
            random_easy_figure = easy_figures.pop()
            create_figure(random_easy_figure, player, SERVER_DB)
            await manager.send_personal_message(random_easy_figure, id_game, player)
            
        for _ in range(round(36/get_players(id_game, SERVER_DB))):
            random_hard_figure = hard_figures.pop()
            create_figure(random_hard_figure, player, SERVER_DB)
            await manager.send_personal_message(random_hard_figure, id_game, player)

    return {"message": "El juego comenzo correctamente."}


@pre_game.websocket("/ws/{id_game}/{user_id}")
async def websocket_endpoint(ws: WebSocket, id_game: int, user_id: int):
    """Canal para que el servidor envie datos de la partida."""
    await manager.connect(ws, id_game, user_id)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws, id_game, user_id)
