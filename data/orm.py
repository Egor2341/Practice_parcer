from data.database import Base, engine


def create_tables():
    Base.metadata.drop_all(engine)
    engine.echo = False
    Base.metadata.create_all(engine)
    engine.echo = False

