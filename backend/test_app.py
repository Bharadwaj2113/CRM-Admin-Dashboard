from app import app
import pytest
import sqlite3
from flask import json
from unittest.mock import patch

class Psycopg2CursorWrapper:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        query = query.replace('%s', '?')
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def __getattr__(self, name):
        return getattr(self.cursor, name)

class Psycopg2ConnectionWrapper:
    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return Psycopg2CursorWrapper(self.conn.cursor())

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    def __getattr__(self, name):
        return getattr(self.conn, name)

@pytest.fixture(scope='function')
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'

    # Create a single in-memory database instance for the test
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    cur.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            purchase_history TEXT
        )
    """)
    conn.commit()
    cur.close()

    # Define the mock connection function
    def test_db_connection():
        return Psycopg2ConnectionWrapper(conn)

    # Apply the patch for the entire test duration
    patcher = patch('app.get_db_connection', side_effect=test_db_connection)
    patcher.start()
    client = app.test_client()
    yield client
    patcher.stop()
    conn.close()  # Close only after all test operations are done

def test_register(client):
    response = client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'User registered'

def test_login(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
    response = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200, f"Login failed: {response.data}"
    data = json.loads(response.data)
    assert data['message'] == 'Login successful'
    assert 'token' in data

def test_customers_get(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
    login_response = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    token = json.loads(login_response.data)['token']
    response = client.get('/customers', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_customers_post(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
    login_response = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    token = json.loads(login_response.data)['token']
    response = client.post('/customers',
                          json={'name': 'John Doe', 'email': 'john@example.com', 'purchase_history': 'Laptop'},
                          headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Customer added'

def test_customer_details(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpass'})
    login_response = client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
    token = json.loads(login_response.data)['token']
    client.post('/customers',
                json={'name': 'John Doe', 'email': 'john@example.com', 'purchase_history': 'Laptop'},
                headers={'Authorization': f'Bearer {token}'})
    response = client.get('/customers/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'John Doe'
    assert data['email'] == 'john@example.com'