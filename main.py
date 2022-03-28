import logging

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_versioning import VersionedFastAPI

from app.persistent_backend.database import database
from app.routers import store_flow_metrics, retrieve_flows


logger = logging.getLogger(__name__)

flow_aggregation_app = FastAPI()


@flow_aggregation_app.on_event("startup")
async def startup():
    await database.connect()
    logger.info("Succesfully connected to database on startup")


@flow_aggregation_app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.info("Succesfully disconnected from database on startup")


flow_aggregation_app.include_router(store_flow_metrics.router)
flow_aggregation_app.include_router(retrieve_flows.router)

add_pagination(flow_aggregation_app)


# flow_aggregation_app = VersionedFastAPI(flow_aggregation_app,
#    version_format='{major}',
#    prefix_format='/v{major}')

@flow_aggregation_app.get("/")
async def welcome():
    """
    Stub with a simple display of the service name
    :return:
    """
    return {'message': 'Flow Aggregation Service, version 1'}
