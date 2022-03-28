from databases import Database
from sqlalchemy import Table
from typing import List

async def insert_events(db: Database, values: List, table: Table):
    query = table.insert()
    await db.execute_many(query=query, values=values)
