import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker


def connect_to_base(base_driver, login, pwd, ip, port, base_name):
    DSN = f"{base_driver}://{login}:{pwd}@{ip}:{port}/{base_name}"
    engine = sq.create_engine(DSN)
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session
