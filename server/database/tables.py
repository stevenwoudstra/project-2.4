from sqlalchemy import Table, Column, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship, backref
from database.db_model import DBModel

class UserGame(DBModel):
    
    __tablename__='user_game'
    
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'), primary_key=True)
    
    user=relationship("User", backref="games")
    game=relationship("Game", backref="users")

class User(DBModel):

    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    user_name = Column(VARCHAR(45), nullable=False, unique=True)
    user_age = Column(Integer, default=None)
    scores = relationship("TopScore")
    games = relationship("Game", secondary="user_game")
    

    def to_dict(self, full=True):
        if full:
            return dict(
                id=self.id,
                name=self.user_name,
                age=self.user_age,
                games=[game.to_dict(False) for game in self.games],
                scores=[ts.to_dict(False) for ts in self.scores]
            )
        else:
            return dict(
                id=self.id,
                name=self.user_name,
                age=self.user_age,
            )
            
        
class Game(DBModel):

    __tablename__ = "game"

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    game_name = Column(VARCHAR(45), nullable=False, unique=True)
    scores = relationship("TopScore")
    users = relationship("User", secondary="user_game")

    def to_dict(self, full=True):
        if full:
            return dict(
                id=self.id,
                name=self.game_name,
                scores=[ts.to_dict(False) for ts in self.scores],
                users=[user.to_dict(False) for user in self.users]
            )
        else:
            return dict(
                id=self.id,
                name=self.game_name,
            )

class TopScore(DBModel):

    __tablename__ = "topscore"

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    game_id = Column(ForeignKey(Game.id), nullable=False)
    user_id = Column(ForeignKey(User.id), nullable=False)
    score = Column(Integer, nullable=False)
    
    game=relationship("Game")
    user=relationship("User")

    def to_dict(self, full=True):
        if full:
            return dict(
                id=self.id,
                user=self.user.to_dict(False),
                game=self.game.to_dict(False),
                score = self.score
            )
        else:
            return dict(
                id=self.id,
                user_id=self.user_id,
                game_id=self.game_id,
                score = self.score
            )
