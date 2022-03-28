import databases
from sqlalchemy import Column, String, Integer, create_engine, MetaData, Table
from app.settings import config

DATABASE_URL = config.database_url

database = databases.Database(DATABASE_URL)

metadata = MetaData()

raw_flow_events = Table(
    "raw_flow_events",
    metadata,
    Column("src_app", String),
    Column("dest_app", String),
    Column("vpc_id", String),
    Column("hour", String),
    Column("bytes_rx", Integer),
    Column("bytes_tx", Integer)
)

async def create_database_engine():
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)

async def get_db():
    await create_database_engine()
    yield database

async def get_raw_flow_events():
    return raw_flow_events