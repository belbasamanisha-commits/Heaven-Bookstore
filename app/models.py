from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager
from sqlalchemy import UniqueConstraint

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model for authentication and cart management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    cart_items = db.relationship('Cart', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Book(db.Model):
    """Book model for catalog"""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(150), nullable=False, index=True)
    price_npr = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    stock_quantity = db.Column(db.Integer, default=0, nullable=False)
    average_rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    cart_items = db.relationship('Cart', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='book', lazy='dynamic', cascade='all, delete-orphan')
    
    def update_average_rating(self):
        """Calculate and update average rating from all reviews"""
        reviews = self.reviews.all()
        if reviews:
            total = sum(review.rating for review in reviews)
            self.average_rating = round(total / len(reviews), 1)
        else:
            self.average_rating = 0.0
        db.session.commit()
    
    def __repr__(self):
        return f'<Book {self.title}>'


class Cart(db.Model):
    """Shopping cart model"""
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Cart User:{self.user_id} Book:{self.book_id}>'


class Review(db.Model):
    """Book review model"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Unique constraint: one review per user per book
    __table_args__ = (UniqueConstraint('user_id', 'book_id', name='unique_user_book_review'),)
    
    def __repr__(self):
        return f'<Review User:{self.user_id} Book:{self.book_id} Rating:{self.rating}>'
