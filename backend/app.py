from flask_cors import CORS
from flask import Flask, request, jsonify
import psycopg2
import bcrypt
import jwt
from functools import wraps
from config import DB_NAME, DB_USER, DB_PASS, DB_HOST, SECRET_KEY

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
    )
    return conn

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token.split()[1], SECRET_KEY, algorithms=['HS256'])
            current_user = data['username']
        except Exception:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Bytes
    
    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed_password, role)
        )
        conn.commit()
        print(f"Registered user: {username}, hash: {hashed_password}")  # Debug
        return jsonify({'message': 'User registered'}), 201
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({'error': 'Username already exists'}), 400
    finally:
        cur.close()
        # Removed conn.close() here

@app.route('/login', methods=['POST'])
def login():
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    cur.execute("SELECT password, role FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    
    if user:
        stored_password = user[0]
        print(f"Stored password: {stored_password}, type: {type(stored_password)}")  # Debug
        print(f"Input password hash: {bcrypt.hashpw(password.encode('utf-8'), stored_password)}")  # Debug
        
        if isinstance(stored_password, str):  # For PostgreSQL TEXT
            stored_password = stored_password.encode('utf-8')
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            token = jwt.encode({'username': username, 'role': user[1]}, SECRET_KEY, algorithm='HS256')
            cur.close()
            # Removed conn.close() here
            return jsonify({'message': 'Login successful', 'token': token, 'role': user[1]}), 200
    
    cur.close()
    # Removed conn.close() here
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/customers', methods=['GET'])
@token_required
def get_customers(current_user):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()
    cur.close()
    # Removed conn.close() here
    return jsonify([dict(row) for row in customers]), 200

@app.route('/customers', methods=['POST'])
@token_required
def add_customer(current_user):
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    purchase_history = data.get('purchase_history')
    
    cur.execute(
        "INSERT INTO customers (name, email, purchase_history) VALUES (%s, %s, %s) RETURNING id",
        (name, email, purchase_history)
    )
    customer_id = cur.fetchone()[0]
    conn.commit()
    
    cur.close()
    # Removed conn.close() here
    
    return jsonify({'message': 'Customer added', 'id': customer_id}), 201

@app.route('/customers/<int:id>', methods=['GET'])
@token_required
def get_customer_details(current_user, id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE id = %s", (id,))
    customer = cur.fetchone()
    cur.close()
    # Removed conn.close() here
    
    if customer:
        return jsonify(dict(customer)), 200
    return jsonify({'message': 'Customer not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
