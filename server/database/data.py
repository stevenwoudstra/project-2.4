from datetime import datetime, date
import click

from database.db_model import DBModel
from database.tables import User, Game, TopScore, UserGame

def user_data(app):
    click.echo("Adding user data...")
    app.session.add(
        User(
            id=1,
            user_name="Pietje Puk",
            user_age=25
        )
    )
    app.session.add(
        User(
            id=2,
            user_name="Jan Janssen",
            user_age=17,
        )
    )
    app.session.flush()
    app.session.commit()
    
def game_data(app):
    click.echo("Adding game data...")
    app.session.add(
        Game(
            id=1,
            game_name="Memory"
        )
    )
    app.session.add(
        Game(
            id=2,
            game_name="TicTacToe"
        )
    )
    app.session.add(
        Game(
            id=3,
            game_name="Reversi"
        )
    )
    app.session.flush()
    app.session.commit()

def topscore_data(app):
    click.echo("Adding score data...")
    app.session.add(
        TopScore(
            user_id=1,
            game_id=1,
            score=23
        )
    )
    app.session.add(
        TopScore(
            user_id=2,
            game_id=1,
            score=45
        )
    )
    app.session.flush()
    app.session.commit()

def usergame_data(app):
    click.echo("Adding usergame data...")
    app.session.add(
        UserGame(
            user_id=1,
            game_id=1
        )
    )
    app.session.add(
        UserGame(
            user_id=2,
            game_id=1
        )
    )
    app.session.flush()
    app.session.commit()    
    
def setup_db(app, cache):
    try:
        if (app.session.query(User).first() is not None):
            print('done')
            return
    except:
        print('nieuwe data')
        # drop all databases and clear cache
        DBModel.metadata.drop_all(bind=app.engine)
        cache.clear()

        # create a new database and add new data
        DBModel.metadata.create_all(bind=app.engine)

        user_data(app)
        game_data(app)
        topscore_data(app)
        usergame_data(app)
