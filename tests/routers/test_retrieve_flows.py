import pytest

from app.routers.retrieve_flows import get_query_statement
from sqlalchemy import MetaData, Column, String, Integer, Table

def test_get_query_statement():
    hour = 5
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
    expected_query = str(('SELECT raw_flow_events.src_app AS src_app, raw_flow_events.dest_app AS '
 'dest_app, raw_flow_events.vpc_id AS vpc_id, raw_flow_events.hour AS hour, '
 'sum(raw_flow_events.bytes_tx) AS bytes_tx, sum(raw_flow_events.bytes_rx) AS '
 'bytes_rx \n'
 'FROM raw_flow_events \n'
 'WHERE raw_flow_events.hour = :hour_1 GROUP BY raw_flow_events.src_app, '
 'raw_flow_events.dest_app, raw_flow_events.vpc_id, raw_flow_events.hour'))

    response = get_query_statement(raw_flow_events, hour)
    assert str(get_query_statement(raw_flow_events, hour)) == expected_query
