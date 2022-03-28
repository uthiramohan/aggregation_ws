import logging

from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Table
from databases import Database
from fastapi_versioning import version

from app.settings import get_config
from app.settings import Config
from app.models.flows_definitions import FlowObject
from app.persistent_backend.database import get_db,get_raw_flow_events
from app.persistent_backend.query_statements import insert_events

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/flows")
#@version(1)
async def report_usage(
        flow_objects: List[FlowObject],
        db: Database = Depends(get_db),
        table: Table = Depends(get_raw_flow_events),
        config: Config = Depends(get_config)
    ) -> JSONResponse:
    """
    This method accepts the flow metrics from each of the agents in the distributed systems. It performs a validation
    on number of input events that could be registered and persists the events in the database
    :param flow_objects: Input flow events unpackaged as FlowObjects by pydantic
    :param db: database injected
    :param table: table object that is injected
    :param config: config object that is injected.
    :return:
    """
    try:
        # using flow_object.__dict__ had a good performance as opposed to flow_object.dict(). Reference https://stackoverflow.com/a/64700151
        raw_events = [flow_object.__dict__ for flow_object in flow_objects]
        num_events = len(raw_events)
        logger.info("Persisting {} flow events to database".format(num_events))
        if num_events > config.total_input_flow_events:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Too many flow objects are being registered")
        await insert_events(db, raw_events, table)
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    except HTTPException as he:
        return JSONResponse(content={'error_message': he.detail, 'status_code': he.status_code}, status_code=500)