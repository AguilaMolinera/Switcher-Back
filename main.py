from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.base import DBManager
from router.cards import cards
from router.game import game
from router.pre_game import pre_game

# TODO -> Agregar los import con los modelos implementados, esto crea la tabla en la base de datos.

from models.figure import FigureTable
from models.move import MoveTable
from models.board import  BoardTable

app = FastAPI(
    title="Switcher - TuringSoft™",
    description="Descripcion de prueba.",
    version="0.1.0",
)

origins = ["http://localhost:5173",
           "http://localhost:5174",
           "http://localhost:5175",
           "http://localhost:8000", ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pre_game)
app.include_router(game)
app.include_router(cards)

# Crea las tablas en base a los models importados.
db = DBManager()
db.teardown()

from schemas.board_schema import Board
from querys.board_queries import *

create_board(1)
b=Board.create(1)
print(b.matrix)
aux = b.matrix[0][0]
b.matrix[0][0] = b.matrix[1][0]
b.matrix[1][0] = aux
print(b.matrix)
update_board(b.id_game,b.matrix)