import pytest
from conftest import client

def test_list_indicators():
    client.post("/auth/register", json={"email": "test@test.com", "password": "testpass"})
    login_response = client.post("/auth/login", json={"email": "test@test.com", "password": "testpass"})
    token = login_response.json()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/indicators", headers=headers)
    assert response.status_code == 200

def test_create_indicator():
    client.post("/auth/register", json={"email": "test@test.com", "password": "testpass"})
    login_response = client.post("/auth/login", json={"email": "test@test.com", "password": "testpass"})
    
    token = login_response.json()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/indicators", json={"type": "test", "value": "test", "severity": "test"}, headers=headers)
    assert response.status_code == 201

def test_create_indicator_missing_fields():
    client.post("/auth/register", json={"email": "test@test.com", "password": "testpass"})
    login_response = client.post("/auth/login", json={"email": "test@test.com", "password": "testpass"})
    token = login_response.json()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/api/indicators", json={"type": "test", "value": "test"}, headers=headers)
    assert response.status_code == 422
    

def test_no_token():
    response = client.post("/api/indicators", json={"type": "test", "value": "test", "severity": "test"})
    assert response.status_code == 401

def test_get_non_existent_indicator():
    client.post("/auth/register", json={"email": "test2@test.com", "password": "testpass"})
    login_response = client.post("/auth/login", json={"email": "test2@test.com", "password": "testpass"})
    token = login_response.json()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/indicators/9999", headers=headers)
    assert response.status_code == 404

def test_filter_severity():
    client.post("/auth/register", json={"email": "test3@test.com", "password": "testpass"})
    login_response = client.post("/auth/login", json={"email": "test3@test.com", "password": "testpass"})
    token = login_response.json()
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/api/indicators", json={"type": "IP", "value": "1.2.3.4", "severity": "HIGH"}, headers=headers)
    client.post("/api/indicators", json={"type": "IP", "value": "5.6.7.8", "severity": "LOW"}, headers=headers)
    

    client.post("/api/indicators", json={"type": "test", "value": "test", "severity": "HIGH"}, headers=headers)
    response = client.get("/api/indicators?severity=HIGH", headers=headers)
    assert response.status_code == 200
    assert all(i["severity"] == "HIGH" for i in response.json())    

