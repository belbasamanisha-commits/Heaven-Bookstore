# Heaven Bookstore - Quick Start Guide

## Installation & Setup

1. **Navigate to project directory:**
   ```bash
   cd "/Users/user/Desktop/Heaven Bookstore"
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Run the application:**
   ```bash
   python run.py
   ```

4. **Access the website:**
   - Open your browser and visit: **http://localhost:5001**

## Login Credentials

### Admin Account (Full Access)
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Admin dashboard, book management, all features

### Test User Account
- **Username:** `john_doe`
- **Password:** `password123`
- **Access:** Shopping cart, reviews, profile

## Quick Feature Tour

1. **Browse Books** - Homepage displays 15 books with cover images
2. **Search** - Use the search bar to find books by title
3. **Categories** - Click any category in the navigation bar
4. **Book Details** - Click any book to see full details and reviews
5. **Register** - Create your own account (top right)
6. **Shopping Cart** - Add books to cart (login required)
7. **Reviews** - Rate and review books (login required)
8. **Admin Panel** - Login as admin and visit `/admin` to manage books

## Project Details

- **Framework:** Flask 3.0.0
- **Database:** SQLite (bookstore.db)
- **Books:** 15 books across 8 categories
- **Port:** 5001
- **Theme:** Light brown aesthetic

## File Locations

- **Main App:** `run.py`
- **Configuration:** `config.py`
- **Database:** `bookstore.db`
- **Templates:** `app/templates/`
- **Styles:** `app/static/css/style.css`
- **JavaScript:** `app/static/js/main.js`

---

**Ready to explore!** The application is fully functional with authentication, shopping cart, reviews, and admin panel. 🎉
