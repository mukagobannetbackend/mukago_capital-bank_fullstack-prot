"""
MUKAGO CAPITAL BANK - Flask Backend API
Advanced Banking and Hedge Fund Trading Platform
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/mukago_bank')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(db.Model):
    """User model for authentication and account management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin, super_admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


class Account(db.Model):
    """Bank account model"""
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(50), nullable=False)  # savings, checking, investment
    balance = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), default='USD')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'balance': self.balance,
            'currency': self.currency,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


class Transaction(db.Model):
    """Transaction history model"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # transfer, deposit, withdrawal
    status = db.Column(db.String(20), default='completed')
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'from_account_id': self.from_account_id,
            'to_account_id': self.to_account_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'status': self.status,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }


class Investment(db.Model):
    """Investment/Hedge fund model"""
    __tablename__ = 'investments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    investment_type = db.Column(db.String(50), nullable=False)  # stocks, bonds, crypto, hedge_fund
    symbol = db.Column(db.String(20))
    quantity = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float)
    total_value = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'account_id': self.account_id,
            'investment_type': self.investment_type,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'purchase_price': self.purchase_price,
            'current_price': self.current_price,
            'total_value': self.total_value,
            'created_at': self.created_at.isoformat()
        }


class AdminLog(db.Model):
    """Admin activity logging"""
    __tablename__ = 'admin_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'details': self.details,
            'created_at': self.created_at.isoformat()
        }


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        full_name=data.get('full_name', ''),
        role='user'
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'User account is inactive'}), 403
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


# ============================================================================
# USER ENDPOINTS
# ============================================================================

@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user details"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@app.route('/api/users', methods=['GET'])
@jwt_required()
def list_users():
    """List all users (admin only)"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


# ============================================================================
# ACCOUNT ENDPOINTS
# ============================================================================

@app.route('/api/accounts', methods=['GET'])
@jwt_required()
def get_accounts():
    """Get user's accounts"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    
    accounts = Account.query.filter_by(user_id=user_id).all()
    return jsonify([account.to_dict() for account in accounts]), 200


@app.route('/api/accounts', methods=['POST'])
@jwt_required()
def create_account():
    """Create a new account"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    data = request.get_json()
    
    account = Account(
        user_id=user_id,
        account_number=f"MCB{user_id}{datetime.utcnow().timestamp()}",
        account_type=data.get('account_type', 'savings'),
        currency=data.get('currency', 'USD')
    )
    
    db.session.add(account)
    db.session.commit()
    
    return jsonify({
        'message': 'Account created successfully',
        'account': account.to_dict()
    }), 201


@app.route('/api/accounts/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
    """Get account details"""
    account = Account.query.get(account_id)
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    return jsonify(account.to_dict()), 200


# ============================================================================
# TRANSACTION ENDPOINTS
# ============================================================================

@app.route('/api/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """Get user's transactions"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    
    accounts = Account.query.filter_by(user_id=user_id).all()
    account_ids = [acc.id for acc in accounts]
    
    transactions = Transaction.query.filter(
        db.or_(
            Transaction.from_account_id.in_(account_ids),
            Transaction.to_account_id.in_(account_ids)
        )
    ).all()
    
    return jsonify([trans.to_dict() for trans in transactions]), 200


@app.route('/api/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    """Create a new transaction"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    data = request.get_json()
    
    from_account = Account.query.get(data.get('from_account_id'))
    
    if not from_account or from_account.user_id != user_id:
        return jsonify({'error': 'Invalid account'}), 400
    
    if from_account.balance < data.get('amount', 0):
        return jsonify({'error': 'Insufficient funds'}), 400
    
    transaction = Transaction(
        from_account_id=data.get('from_account_id'),
        to_account_id=data.get('to_account_id'),
        amount=data.get('amount'),
        transaction_type=data.get('transaction_type', 'transfer'),
        description=data.get('description', '')
    )
    
    from_account.balance -= data.get('amount')
    
    if data.get('to_account_id'):
        to_account = Account.query.get(data.get('to_account_id'))
        if to_account:
            to_account.balance += data.get('amount')
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        'message': 'Transaction created successfully',
        'transaction': transaction.to_dict()
    }), 201


# ============================================================================
# INVESTMENT ENDPOINTS
# ============================================================================

@app.route('/api/investments', methods=['GET'])
@jwt_required()
def get_investments():
    """Get user's investments"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    
    investments = Investment.query.filter_by(user_id=user_id).all()
    return jsonify([inv.to_dict() for inv in investments]), 200


@app.route('/api/investments', methods=['POST'])
@jwt_required()
def create_investment():
    """Create a new investment"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    data = request.get_json()
    
    investment = Investment(
        user_id=user_id,
        account_id=data.get('account_id'),
        investment_type=data.get('investment_type'),
        symbol=data.get('symbol'),
        quantity=data.get('quantity'),
        purchase_price=data.get('purchase_price'),
        current_price=data.get('purchase_price'),
        total_value=data.get('quantity') * data.get('purchase_price')
    )
    
    db.session.add(investment)
    db.session.commit()
    
    return jsonify({
        'message': 'Investment created successfully',
        'investment': investment.to_dict()
    }), 201


# ============================================================================
# ADMIN ENDPOINTS
# ============================================================================

@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    """Get admin dashboard statistics"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    if user.role not in ['admin', 'super_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    stats = {
        'total_users': User.query.count(),
        'total_accounts': Account.query.count(),
        'total_transactions': Transaction.query.count(),
        'total_investments': Investment.query.count(),
        'total_balance': db.session.query(db.func.sum(Account.balance)).scalar() or 0,
        'active_users': User.query.filter_by(is_active=True).count()
    }
    
    return jsonify(stats), 200


@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def admin_list_users():
    """List all users for admin"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    if user.role not in ['admin', 'super_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


@app.route('/api/admin/users/<int:user_id>/deactivate', methods=['PUT'])
@jwt_required()
def deactivate_user(user_id):
    """Deactivate a user (admin only)"""
    from flask_jwt_extended import get_jwt_identity
    admin_id = get_jwt_identity()
    
    admin = User.query.get(admin_id)
    if admin.role not in ['admin', 'super_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.is_active = False
    
    log = AdminLog(
        admin_id=admin_id,
        action='deactivate_user',
        resource_type='user',
        resource_id=user_id
    )
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': 'User deactivated successfully'}), 200


@app.route('/api/admin/logs', methods=['GET'])
@jwt_required()
def get_admin_logs():
    """Get admin activity logs"""
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    if user.role not in ['admin', 'super_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    logs = AdminLog.query.order_by(AdminLog.created_at.desc()).limit(100).all()
    return jsonify([log.to_dict() for log in logs]), 200


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
