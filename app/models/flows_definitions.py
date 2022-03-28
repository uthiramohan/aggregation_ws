from pydantic import BaseModel, Field

class FlowObject(BaseModel):
    src_app: str = Field(title='Source App')
    dest_app: str = Field(title='Destination App')
    vpc_id: str = Field(title='VPC ID')
    hour: int = Field(title='Hour')
    bytes_rx: int = Field(title='Bytes Received')
    bytes_tx: int = Field(title='Bytes Transmitted')
