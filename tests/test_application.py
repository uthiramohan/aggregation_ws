from fastapi.testclient import TestClient
import pytest
from databases import Database
from sqlalchemy import MetaData, Table, Column, String, create_engine, Integer
from fastapi import status

from main import flow_aggregation_app
from app.settings import get_config, Config
from app.settings import config

from app.persistent_backend.database import get_db, get_raw_flow_events

DATABASE_URL = config.test_database_url

database = None
raw_flow_events = None

client = TestClient(flow_aggregation_app)

POST_URL_ENDPOINT = "/flows"
GET_URL_ENDPOINT = "/flows"

database = Database(DATABASE_URL, force_rollback=True)
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


@pytest.fixture()
def create_test_database():
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

    metadata.create_all(bind=engine)

    # Run the test suite
    yield

    # Drop test databases
    metadata.drop_all(engine)


def override_get_db():
    return database


def override_get_table():
    return raw_flow_events


flow_aggregation_app.dependency_overrides[get_db] = override_get_db
flow_aggregation_app.dependency_overrides[get_raw_flow_events] = override_get_table


@pytest.fixture()
def setup_values_in_test_db(create_test_database):
    json_items = [
        {"src_app": "foo", "dest_app": "bar", "vpc_id": "vpc-0", "bytes_tx": 100, "bytes_rx": 300, "hour": 1},
        {"src_app": "foo", "dest_app": "bar", "vpc_id": "vpc-0", "bytes_tx": 200, "bytes_rx": 600, "hour": 1},
        {"src_app": "baz", "dest_app": "qux", "vpc_id": "vpc-0", "bytes_tx": 100, "bytes_rx": 500, "hour": 1},
        {"src_app": "baz", "dest_app": "qux", "vpc_id": "vpc-0", "bytes_tx": 100, "bytes_rx": 500, "hour": 2},
        {"src_app": "baz", "dest_app": "qux", "vpc_id": "vpc-1", "bytes_tx": 100, "bytes_rx": 500, "hour": 2}
    ]
    client.post(
        POST_URL_ENDPOINT,
        json=json_items,
    )


def test_get_flows(create_test_database, setup_values_in_test_db):
    expected_responses = {
        'hour_1': [
            {"src_app": "baz", "dest_app": "qux", "vpc_id": "vpc-0", "hour": 1, "bytes_rx": 500, "bytes_tx": 100},
            {"src_app": "foo", "dest_app": "bar", "vpc_id": "vpc-0", "hour": 1, "bytes_rx": 900, "bytes_tx": 300}],
        'hour_2': [
            {"src_app": "baz", "dest_app": "qux", "vpc_id": "vpc-0", "hour": 2, "bytes_rx": 500, "bytes_tx": 100},
            {"src_app": "baz", "dest_app": "qux", "vpc_id": "vpc-1", "hour": 2, "bytes_rx": 500, "bytes_tx": 100}],
        'hour_3': []
    }

    # testing get responses
    response_hour_1 = client.get(GET_URL_ENDPOINT + "?hour=1")
    data_hour_1 = response_hour_1.json()

    assert response_hour_1.status_code == 200
    assert len(data_hour_1['items']) == 2
    assert data_hour_1['items'] == expected_responses['hour_1']

    response_hour_2 = client.get(GET_URL_ENDPOINT + "?hour=2")
    data_hour_2 = response_hour_2.json()

    assert response_hour_2.status_code == 200
    assert len(data_hour_2['items']) == 2
    assert data_hour_2['items'] == expected_responses['hour_2']

    response_hour_3 = client.get(GET_URL_ENDPOINT + "?hour=3")
    data_hour_3 = response_hour_3.json()

    assert response_hour_3.status_code == 200
    assert len(data_hour_3['items']) == 0
    assert data_hour_3['items'] == expected_responses['hour_3']

    # testing input query parameters
    res = client.get(GET_URL_ENDPOINT + "?hour=five")
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    res = client.get(GET_URL_ENDPOINT + "?hour")
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_unsupported_http_methods():
    response_put_method = client.put(POST_URL_ENDPOINT, json={})
    assert response_put_method.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    response_delete_method = client.delete(POST_URL_ENDPOINT, json={})
    assert response_delete_method.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_post_flows_request(create_test_database):
    json_items = [
        {"src_app": "foo", "dest_app": "bar", "vpc_id": "vpc-0", "bytes_tx": 100, "bytes_rx": 300, "hour": 1},
        {"src_app": "baz", "dest_app": "qux", "vpc_id": "vpc-1", "bytes_tx": 100, "bytes_rx": 500, "hour": 2}
    ]
    response = client.post(
        POST_URL_ENDPOINT,
        json=json_items,
    )
    assert response.status_code == status.HTTP_201_CREATED


def override_get_config():
    return Config(total_input_flow_events=1)


def test_post_flows_request_exception(create_test_database):
    flow_aggregation_app.dependency_overrides[get_config] = override_get_config
    json_items = [
        {"src_app": "baz", "dest_app": "qux", "vpc_id": "vpc-1", "bytes_tx": 100, "bytes_rx": 500, "hour": 2},
        {"src_app": "foo", "dest_app": "bar", "vpc_id": "vpc-0", "bytes_tx": 100, "bytes_rx": 300, "hour": 1},
        {"src_app": "baz", "dest_app": "qux", "vpc_id": "vpc-1", "bytes_tx": 100, "bytes_rx": 500, "hour": 2}
    ]
    response = client.post(
        POST_URL_ENDPOINT,
        json=json_items,
    )
    assert response.status_code == 500
    assert response.json() == {'error_message': 'Too many flow objects are being registered', 'status_code': 406}

    flow_aggregation_app.dependency_overrides[get_config] = get_config