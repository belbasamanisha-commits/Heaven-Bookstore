from flask import current_app as app, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from app import db
from app.models import User, Book, Cart, Review
from app.forms import RegistrationForm, LoginForm, BookForm, ReviewForm
from sqlalchemy import or_


def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ============== PUBLIC ROUTES ==============

@app.route('/')
@app.route('/index')
def index():
    """Home page with best sellers"""
    books = Book.query.order_by(Book.average_rating.desc()).limit(15).all()
    categories = ['Photography', 'Investing', 'Literature', 'Languages', 
                  'Biography', 'Reference', 'Wellness', 'Graphic Novels']
    
    # Get cart count
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = Cart.query.filter_by(user_id=current_user.id).count()
    
    return render_template('index.html', books=books, categories=categories, cart_count=cart_count)


@app.route('/category/<category>')
def category(category):
    """Display books by category"""
    books = Book.query.filter_by(category=category).all()
    categories = ['Photography', 'Investing', 'Literature', 'Languages', 
                  'Biography', 'Reference', 'Wellness', 'Graphic Novels']
    
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = Cart.query.filter_by(user_id=current_user.id).count()
    
    return render_template('category.html', books=books, category=category, 
                         categories=categories, cart_count=cart_count)


@app.route('/book/<int:id>')
def book_detail(id):
    """Book detail page with reviews"""
    book = Book.query.get_or_404(id)
    reviews = Review.query.filter_by(book_id=id).order_by(Review.created_at.desc()).all()
    form = ReviewForm()
    
    categories = ['Photography', 'Investing', 'Literature', 'Languages', 
                  'Biography', 'Reference', 'Wellness', 'Graphic Novels']
    
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = Cart.query.filter_by(user_id=current_user.id).count()
        # Check if user already reviewed this book
        user_review = Review.query.filter_by(user_id=current_user.id, book_id=id).first()
    else:
        user_review = None
    
    return render_template('book_detail.html', book=book, reviews=reviews, 
                         form=form, user_review=user_review, categories=categories, 
                         cart_count=cart_count)


@app.route('/search')
def search():
    """Search for books by name"""
    query = request.args.get('q', '')
    
    if query:
        books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
    else:
        books = []
    
    categories = ['Photography', 'Investing', 'Literature', 'Languages', 
                  'Biography', 'Reference', 'Wellness', 'Graphic Novels']
    
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = Cart.query.filter_by(user_id=current_user.id).count()
    
    return render_template('search.html', books=books, query=query, 
                         categories=categories, cart_count=cart_count)


# ============== AUTHENTICATION ROUTES ==============

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Try to find user by username or email
        user = User.query.filter(
            or_(User.username == form.username.data, User.email == form.username.data)
        ).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username/email or password.', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    categories = ['Photography', 'Investing', 'Literature', 'Languages', 
                  'Biography', 'Reference', 'Wellness', 'Graphic Novels']
    cart_count = Cart.query.filter_by(user_id=current_user.id).count()
    
    return render_template('profile.html', categories=categories, cart_count=cart_count)


# ============== CART ROUTES ==============

@app.route('/cart')
@login_required
def cart():
    """Shopping cart page"""
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    
    # Calculate total
    total = sum(item.book.price_npr * item.quantity for item in cart_items)
    
    categories = ['Photography', 'Investing', 'Literature', 'Languages', 
                  'Biography', 'Reference', 'Wellness', 'Graphic Novels']
    cart_count = len(cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total, 
                         categories=categories, cart_count=cart_count)


@app.route('/cart/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    """Add book to cart"""
    book = Book.query.get_or_404(book_id)
    
    # Check if book already in cart
    cart_item = Cart.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    
    if cart_item:
        # Increase quantity
        cart_item.quantity += 1
    else:
        # Add new cart item
        cart_item = Cart(user_id=current_user.id, book_id=book_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    
    # Get updated cart count
    cart_count = Cart.query.filter_by(user_id=current_user.id).count()
    
    # Return JSON for AJAX requests
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'cart_count': cart_count, 'message': 'Book added to cart!'})
    
    flash('Book added to cart!', 'success')
    return redirect(request.referrer or url_for('index'))


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    """Remove item from cart"""
    cart_item = Cart.query.get_or_404(item_id)
    
    # Ensure user owns this cart item
    if cart_item.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.', 'success')
    
    return redirect(url_for('cart'))


@app.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    """Update cart item quantity"""
    cart_item = Cart.query.get_or_404(item_id)
    
    # Ensure user owns this cart item
    if cart_item.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('cart'))
    
    quantity = request.form.get('quantity', type=int)
    
    if quantity and quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
        flash('Cart updated.', 'success')
    else:
        flash('Invalid quantity.', 'danger')
    
    return redirect(url_for('cart'))


# ============== REVIEW ROUTES ==============

@app.route('/book/<int:id>/review', methods=['POST'])
@login_required
def submit_review(id):
    """Submit a book review"""
    book = Book.query.get_or_404(id)
    form = ReviewForm()
    
    if form.validate_on_submit():
        # Check if user already reviewed this book
        existing_review = Review.query.filter_by(user_id=current_user.id, book_id=id).first()
        
        if existing_review:
            # Update existing review
            existing_review.rating = int(form.rating.data)
            existing_review.review_text = form.review_text.data
            flash('Your review has been updated.', 'success')
        else:
            # Create new review
            review = Review(
                user_id=current_user.id,
                book_id=id,
                rating=int(form.rating.data),
                review_text=form.review_text.data
            )
            db.session.add(review)
            flash('Thank you for your review!', 'success')
        
        db.session.commit()
        
        # Update book's average rating
        book.update_average_rating()
    
    return redirect(url_for('book_detail', id=id))


# ============== ADMIN ROUTES ==============

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    books = Book.query.all()
    total_books = Book.query.count()
    total_users = User.query.count()
    total_reviews = Review.query.count()
    
    categories = ['Photography', 'Investing', 'Literature', 'Languages', 
                  'Biography', 'Reference', 'Wellness', 'Graphic Novels']
    cart_count = Cart.query.filter_by(user_id=current_user.id).count()
    
    return render_template('admin/dashboard.html', books=books, 
                         total_books=total_books, total_users=total_users, 
                         total_reviews=total_reviews, categories=categories, 
                         cart_count=cart_count)


@app.route('/admin/book/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_book():
    """Add new book"""
    form = BookForm()
    
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            price_npr=form.price_npr.data,
            category=form.category.data,
            description=form.description.data,
            image_url=form.image_url.data,
            stock_quantity=form.stock_quantity.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    categories = ['Photography', 'Investing', 'Literature', 'Languages', 
                  'Biography', 'Reference', 'Wellness', 'Graphic Novels']
    cart_count = Cart.query.filter_by(user_id=current_user.id).count()
    
    return render_template('admin/add_book.html', form=form, categories=categories, 
                         cart_count=cart_count)


@app.route('/admin/book/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_book(id):
    """Edit existing book"""
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.price_npr = form.price_npr.data
        book.category = form.category.data
        book.description = form.description.data
        book.image_url = form.image_url.data
        book.stock_quantity = form.stock_quantity.data
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    categories = ['Photography', 'Investing', 'Literature', 'Languages', 
                  'Biography', 'Reference', 'Wellness', 'Graphic Novels']
    cart_count = Cart.query.filter_by(user_id=current_user.id).count()
    
    return render_template('admin/edit_book.html', form=form, book=book, 
                         categories=categories, cart_count=cart_count)


@app.route('/admin/book/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_book(id):
    """Delete book"""
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))
