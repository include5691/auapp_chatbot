from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, registry
from e5lib.orm import get_engine

Base: registry = declarative_base()
engine = get_engine()
SessionMaker = scoped_session(sessionmaker(bind=engine))