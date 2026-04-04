import pytest
from conftest import client

def test_register():
    response = client.post("/auth/register", json={"email": "test@test.com", "password": "testpass"})
    assert response.status_code == 200

def test_login():
    client.post("/auth/register", json={"email": "test@test.com", "password": "testpass"})
    response = client.post("/auth/login", json={"email": "test@test.com", "password": "testpass"})
    assert response.json().startswith("ey")
