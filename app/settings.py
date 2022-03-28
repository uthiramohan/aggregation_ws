from pydantic import BaseSettings

class Config(BaseSettings):
    database_url: str = "sqlite:///./flows.db"
    test_database_url: str = "sqlite:///./test.db"
    total_input_flow_events: int = 100000
    per_page: int = 1000000
    server_log_path: str = "./server.log"

config = Config()

def get_config():
    return config
