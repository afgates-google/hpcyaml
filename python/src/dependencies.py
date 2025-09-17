from functools import lru_cache
from src.gcp_client import GcpClient

@lru_cache()
def get_gcp_client(project_id: str) -> GcpClient:
    return GcpClient(project_id=project_id)
