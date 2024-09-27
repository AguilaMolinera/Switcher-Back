from sqlalchemy import Column, Integer, String
from models.base import Base
from sqlalchemy.orm import relationship

Users = relationship("BoardTable", backref="GameTable")

class GameTable(Base):
    
    __tablename__ = 'GameTable'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    state = Column(String, default="Waiting", index=True)
    turn = Column(Integer, default=0, index=True)
    host = Column(Integer, index=True, nullable=False, default=0)
    players = Column(Integer, default=1, index=True)
    max_players = Column(Integer, default=4)
    min_players = Column(Integer, default=2)
    password = Column(String, default="password")
    Users = relationship("UserTable", backref="GameTable")
