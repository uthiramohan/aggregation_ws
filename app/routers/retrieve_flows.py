import logging
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from databases import Database
from sqlalchemy import select, Table
from sqlalchemy.sql import func
from fastapi_pagination import Page, paginate
from fastapi_versioning import version

from app.models.flows_definitions import FlowObject
from app.persistent_backend.database import get_db,get_raw_flow_events

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/flows", response_model=Page[FlowObject])
#@version(1)
async def get_flow_metrics(
        hour: int,
        db: Database = Depends(get_db),
        table: Table = Depends(get_raw_flow_events)
):
    """
    Handles the get request with query parameter hour. A sqlachemy select statement is first constructed where we filter
    by given hour and group by the keys. We then submit an async query to fetch all the results. The results are then
    paginated and responded.
    :param hour: Request query parameter
    :param db: Database object injected
    :param table: table name injected
    :return:
    """
    try:
        return paginate(await db.fetch_all(get_query_statement(table, hour)))
    except Exception as e:
        return JSONResponse(content={'error_message': str(e), 'status_code': 500}, status_code=500)

def get_query_statement(table: Table, hour: int):
    """
    Constructs a sqlalchemy select statement. Expectation is that the filter predicate will pushed inside during
    execution
    :param table: Sqlalchemy Table object
    :param hour: hour value in the filter.
    :return:
    """
    query_statement = select([
        table.c.src_app.label('src_app'),
        table.c.dest_app.label('dest_app'),
        table.c.vpc_id.label('vpc_id'),
        table.c.hour.label('hour'),
        func.sum(table.c.bytes_tx).label('bytes_tx'),
        func.sum(table.c.bytes_rx).label('bytes_rx')
    ]).group_by(table.c.src_app,
                table.c.dest_app,
                table.c.vpc_id,
                table.c.hour
                ).where(table.c.hour == hour) # to extend and handle multiple hour values, we can use IN predicate.
    logger.info("Query generated: {}".format(query_statement))
    return query_statement
