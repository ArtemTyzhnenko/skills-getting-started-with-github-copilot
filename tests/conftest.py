import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture providing a test client for the FastAPI app"""
    return TestClient(app)
