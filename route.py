
from flask import Flask, request, jsonify, flash, redirect, url_for,render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import apps,db
from models import Account
import datetime
from datetime import datetime, timedelta
from flask import session
from urllib.parse import urlparse, urljoin
from flask import Response




app = apps()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Specify the login view endpoint
login_manager.login_message = 'Please log in to access this page.'  # Custom login message

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

# Set the allowed account creation limit per hour
first_user_time = None
registered_users = 0
reset_interval = timedelta(hours=1)

@app.route('/register', methods=['POST'])
def register():
    try:
        global first_user_time, registered_users

        data = request.get_json()

        if not data:
            return jsonify({'error': 'Invalid data format'}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        limit = 5  # Example limit

        current_time = datetime.now()

        if first_user_time is None or current_time > (first_user_time + reset_interval):
            # If it's the first user or more than one hour has passed since the first user,
            # update the first_user_time and reset the registered_users count
            first_user_time = current_time
            registered_users = 0

        if registered_users >= limit:
            # If the account creation limit is reached, save the new account to the database with is_active=False
            new_account = Account(username=username, password=password, is_active=False)
            db.session.add(new_account)
            db.session.commit()
            return jsonify({'message': 'Account creation limit exceeded. You cannot log in.'}), 403
        else:
            # If the account creation limit is not reached, save the new account to the database with is_active=True
            new_account = Account(username=username, password=password, is_active=True)
            registered_users += 1
            db.session.add(new_account)
            db.session.commit()
            print('ress', registered_users)
            return jsonify({"message": "Registration successful!"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        if current_user.is_authenticated:
            return jsonify({"error": "Already authenticated"})

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"})

        username = data.get('username')
        password = data.get('password')
        print(username, password)
        account = Account.query.filter_by(username=username, is_active=True).first()

        if account and account.password == password:
            login_user(account)
            session['username'] = account.username

            return jsonify({'message': 'Login successful', 'username': account.username})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

    

        
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        print('in dash')
        print("cuu", current_user.username)
        username = current_user.username
        return render_template('dashboard.html', username=username)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/logout')
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logout successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/adminlogin', methods=['POST'])
def admin_log():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"})

        username = data.get('username')
        password = data.get('password')
        print(username, password)
        account = Account.query.filter_by(username=username, is_active=True, is_admin=True).first()

        if account and account.password == password:
            login_user(account)
            session['username'] = account.username

            return jsonify({'message': 'Login successful', 'username': account.username})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/admin_home', methods=['POST','GET'])
def admin_home():
    try:
        accounts = Account.query.filter_by(is_admin=False)
        serialized_accounts = [account.serialize() for account in accounts]
        return jsonify(serialized_accounts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/block_user/<int:id>', methods=['POST','GET'])
def block_user(id):
    try:
        accounts = Account.query.filter_by(id=id, is_admin=False).first()
        if accounts:
            if accounts.is_active:
                accounts.is_active = False
                db.session.commit()
                return jsonify({"message": "Blocked"})
            else:
                accounts.is_active = True
                db.session.commit()
                return jsonify({"message": "Unblocked"})
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
            
    
    
    
    
    

    
    

    # if 'username' in session:
    #     username = session['username']
    #     return jsonify({'username':username})
    # else:
    #     resp = jsonify({"message":"unauthorized"})
    #     resp.status_code = 401
    #     return resp
    # username = session.get('username')
    # print('user',username)
    # if username:
    #     return {'username': username}
    # else:
    #     return {'message': 'Username not found in session'}