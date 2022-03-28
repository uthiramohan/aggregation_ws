import databases
import sqlalchemy

from app.settings import config

DATABASE_URL = config.database_url

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

raw_flow_events = sqlalchemy.Table(
    "raw_flow_events",
    metadata,
    sqlalchemy.Column("src_app", sqlalchemy.String),
    sqlalchemy.Column("dest_app", sqlalchemy.String),
    sqlalchemy.Column("vpc_id", sqlalchemy.String),
    sqlalchemy.Column("hour", sqlalchemy.String),
    sqlalchemy.Column("bytes_rx", sqlalchemy.Integer),
    sqlalchemy.Column("bytes_tx", sqlalchemy.Integer)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

async def create_engine():
    metadata.create_all(engine)

async def get_db():
    return database

async def get_raw_flow_events():
    return raw_flow_events