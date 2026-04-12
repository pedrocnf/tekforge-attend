from google.cloud import firestore
from app.core.config import settings

_client: firestore.Client | None = None


def get_firestore_client() -> firestore.Client:
    global _client
    if _client is None:
        _client = firestore.Client(project=settings.gcp_project_id)
    return _client
