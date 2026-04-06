import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, 
    jwt_required, get_jwt_identity
)
from config import config
from models import db, bcrypt, User, Task

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # JWT configuration - ensure it's set
    app.config['JWT_SECRET_KEY'] = app.config.get('JWT_SECRET_KEY', 'fallback-secret-key-must-be-at-least-32-characters-long')
    jwt = JWTManager(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # ==================== HEALTH CHECK ====================
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({"status": "healthy"}), 200
    
    # ==================== AUTHENTICATION ====================
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        """Register a new user"""
        try:
            data = request.get_json(force=True)
        except:
            return jsonify({"error": "Invalid JSON"}), 400
            
        # Validate input
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 400
        
        # Create user
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Login user and return JWT token"""
        try:
            data = request.get_json(force=True)
        except:
            return jsonify({"error": "Invalid JSON"}), 400
            
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({"error": "Missing username or password"}), 400
        
        # Find user
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Create token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            "access_token": access_token,
            "user": user.to_dict()
        }), 200
    
    # ==================== TASK CRUD ====================
    @app.route('/api/tasks', methods=['GET'])
    @jwt_required()
    def get_tasks():
        """Get all tasks for the authenticated user"""
        user_id = get_jwt_identity()
        
        # Optional filters
        status = request.args.get('status')
        priority = request.args.get('priority')
        category = request.args.get('category')
        
        # Build query
        query = Task.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if category:
            query = query.filter_by(category=category)
        
        tasks = query.all()
        
        return jsonify([task.to_dict() for task in tasks]), 200
    
    @app.route('/api/tasks', methods=['POST'])
    @jwt_required()
    def create_task():
        """Create a new task"""
        user_id = get_jwt_identity()
        
        try:
            data = request.get_json(force=True)
        except:
            return jsonify({"error": "Invalid JSON"}), 400
        
        # Validate input
        if not data or not data.get('title'):
            return jsonify({"error": "Title is required"}), 400
        
        # Validate status
        if data.get('status') and data['status'] not in ['todo', 'in_progress', 'done']:
            return jsonify({"error": "Invalid status"}), 400
        
        # Validate priority
        if data.get('priority') and data['priority'] not in ['low', 'medium', 'high']:
            return jsonify({"error": "Invalid priority"}), 400
        
        # Create task
        task = Task(
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'todo'),
            priority=data.get('priority', 'medium'),
            category=data.get('category'),
            user_id=user_id
        )
        
        # Parse due date if provided
        if data.get('due_date'):
            try:
                task.due_date = datetime.fromisoformat(data['due_date'])
            except ValueError:
                return jsonify({"error": "Invalid due_date format (use ISO format)"}), 400
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify(task.to_dict()), 201
    
    @app.route('/api/tasks/<int:task_id>', methods=['GET'])
    @jwt_required()
    def get_task(task_id):
        """Get a specific task"""
        user_id = get_jwt_identity()
        
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        return jsonify(task.to_dict()), 200
    
    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    @jwt_required()
    def update_task(task_id):
        """Update a task"""
        user_id = get_jwt_identity()
        
        try:
            data = request.get_json(force=True)
        except:
            return jsonify({"error": "Invalid JSON"}), 400
        
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        # Update fields
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            if data['status'] not in ['todo', 'in_progress', 'done']:
                return jsonify({"error": "Invalid status"}), 400
            task.status = data['status']
        if 'priority' in data:
            if data['priority'] not in ['low', 'medium', 'high']:
                return jsonify({"error": "Invalid priority"}), 400
            task.priority = data['priority']
        if 'category' in data:
            task.category = data['category']
        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.fromisoformat(data['due_date'])
                except ValueError:
                    return jsonify({"error": "Invalid due_date format"}), 400
            else:
                task.due_date = None
        
        db.session.commit()
        
        return jsonify(task.to_dict()), 200
    
    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    @jwt_required()
    def delete_task(task_id):
        """Delete a task"""
        user_id = get_jwt_identity()
        
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({"message": "Task deleted"}), 200
    
    return app

# Create app instance
app = create_app(os.environ.get('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)