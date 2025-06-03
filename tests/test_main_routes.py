import json


def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    expected_data = {"status": "healthy", "message": "API is running"}
    assert response.get_json() == expected_data
