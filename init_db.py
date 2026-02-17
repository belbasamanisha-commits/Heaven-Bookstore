#!/usr/bin/env python3
"""
Database Initialization Script for Heaven Bookstore
Creates tables and populates with sample data
"""

from app import create_app, db
from app.models import User, Book

def init_database():
    """Initialize database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate (for development)
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@heavenbookstore.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample regular user
        print("Creating sample user...")
        user = User(
            username='john_doe',
            email='john@example.com',
            is_admin=False
        )
        user.set_password('password123')
        db.session.add(user)
        
        # Commit users
        db.session.commit()
        
        # Sample books data
        print("Adding sample books...")
        
        books_data = [
            {
                'title': 'The Photographer\'s Eye',
                'author': 'Michael Freeman',
                'price_npr': 1850.00,
                'category': 'Photography',
                'description': 'The Photographer\'s Eye by Michael Freeman is a visual guide to understanding composition and design for better photography. This book breaks down the principles of great composition into clear, practical advice that will help photographers at all levels improve their work. Freeman explores concepts like balance, pattern, rhythm, and more with stunning visual examples.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/81B3QP5p7HL.jpg',
                'stock_quantity': 25
            },
            {
                'title': 'National Geographic: The Photographs',
                'author': 'National Geographic',
                'price_npr': 2500.00,
                'category': 'Photography',
                'description': 'A stunning collection of National Geographic\'s most iconic photographs from over 130 years of exploration and storytelling. This breathtaking anthology showcases the world\'s most compelling images, from wildlife and nature to culture and adventure. Each photograph tells a unique story and captures moments that have defined our understanding of the planet.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/91xjKvqKdvL.jpg',
                'stock_quantity': 15
            },
            {
                'title': 'The Intelligent Investor',
                'author': 'Benjamin Graham',
                'price_npr': 1200.00,
                'category': 'Investing',
                'description': 'The Intelligent Investor by Benjamin Graham is widely considered the most important book ever written on investing. Graham\'s philosophy of "value investing" has protected and enriched countless investors worldwide. This classic text provides strategies for successful long-term investing and teaches readers how to minimize risk while maximizing returns through careful analysis and disciplined decision-making.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/91yOK7AFAWL.jpg',
                'stock_quantity': 30
            },
            {
                'title': 'Rich Dad Poor Dad',
                'author': 'Robert Kiyosaki',
                'price_npr': 950.00,
                'category': 'Investing',
                'description': 'Rich Dad Poor Dad is Robert Kiyosaki\'s best-selling personal finance book that challenges conventional wisdom about money and investing. Through the contrasting lessons of his "rich dad" and "poor dad," Kiyosaki reveals how the wealthy think differently about money, work, and wealth-building. This book has inspired millions to take control of their financial future and build lasting wealth.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/81bsw6fnUiL.jpg',
                'stock_quantity': 40
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'price_npr': 750.00,
                'category': 'Literature',
                'description': 'George Orwell\'s dystopian masterpiece 1984 is a chilling portrait of a totalitarian society where Big Brother watches everything. Written in 1949, this prophetic novel explores themes of government surveillance, propaganda, and the manipulation of truth. Its warnings about authoritarianism and loss of individual freedom remain powerfully relevant today, making it essential reading for understanding modern society.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/71rpa1-kyvL.jpg',
                'stock_quantity': 50
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'price_npr': 800.00,
                'category': 'Literature',
                'description': 'Harper Lee\'s Pulitzer Prize-winning novel is a timeless story of justice, prejudice, and moral growth in the American South. Through the eyes of young Scout Finch, readers witness her father Atticus\'s courageous defense of a Black man falsely accused of assault. This beloved classic explores themes of racial injustice, childhood innocence, and the importance of standing up for what\'s right.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/81aY1lxk+9L.jpg',
                'stock_quantity': 35
            },
            {
                'title': 'Steve Jobs',
                'author': 'Walter Isaacson',
                'price_npr': 1350.00,
                'category': 'Biography',
                'description': 'Based on more than forty interviews with Steve Jobs over two years, as well as interviews with family, friends, adversaries, and colleagues, Walter Isaacson has written a riveting story of the roller-coaster life and searingly intense personality of a creative entrepreneur. This definitive biography reveals the man behind the Macintosh, iPhone, iPad, and Pixar—a perfectionist who revolutionized six industries.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/81VStYnDGrL.jpg',
                'stock_quantity': 20
            },
            {
                'title': 'The Secret History',
                'author': 'Donna Tartt',
                'price_npr': 1100.00,
                'category': 'Literature',
                'description': 'Under the influence of their charismatic classics professor, a group of clever, eccentric misfits at an elite New England college discover a way of thinking and living that is a world away from the humdrum existence of their contemporaries. But when they go beyond the boundaries of normal morality, their lives are changed profoundly and forever. This psychological thriller is a contemporary classic.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/81e5PQhG-WL.jpg',
                'stock_quantity': 18
            },
            {
                'title': 'Atomic Habits',
                'author': 'James Clear',
                'price_npr': 1050.00,
                'category': 'Wellness',
                'description': 'Atomic Habits presents a proven framework for improving every day. James Clear reveals practical strategies that will teach you exactly how to form good habits, break bad ones, and master the tiny behaviors that lead to remarkable results. Drawing on scientific research and real-life examples, this book shows how small changes can transform your life through the compound effect of marginal gains.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/81YkqyaFVEL.jpg',
                'stock_quantity': 45
            },
            {
                'title': 'The Love Hypothesis',
                'author': 'Ali Hazelwood',
                'price_npr': 850.00,
                'category': 'Wellness',
                'description': 'When a fake relationship between scientist Olive Smith and Professor Adam Carlsen turns unexpectedly real, Olive must navigate the complex world of academia, relationships, and her own heart. This contemporary romance combines humor, heart, and STEM with a charming love story. Perfect for fans of romantic comedies who appreciate smart, quirky characters and swoon-worthy moments.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/81cE+-x+jaL.jpg',
                'stock_quantity': 28
            },
            {
                'title': 'Hooked: How to Build Habit-Forming Products',
                'author': 'Nir Eyal',
                'price_npr': 1150.00,
                'category': 'Reference',
                'description': 'Why do some products capture widespread attention while others flop? What makes us engage with certain products out of habit? Nir Eyal answers these questions and more by explaining the Hook Model—a four-step process embedded into successful products. Through consecutive hook cycles, these products reach their ultimate goal of bringing users back again and again without depending on costly advertising or aggressive messaging.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/71kp6cCG3uL.jpg',
                'stock_quantity': 22
            },
            {
                'title': 'Maus',
                'author': 'Art Spiegelman',
                'price_npr': 1400.00,
                'category': 'Graphic Novels',
                'description': 'Maus is a haunting tale within a tale, weaving the author\'s account of his tortured relationship with his aging father into an astonishing retelling of one of history\'s most unspeakable tragedies. Art Spiegelman depicts the Holocaust with Jews as mice and Nazis as cats, creating a powerful and unforgettable narrative. This Pulitzer Prize-winning graphic novel is a masterpiece of storytelling.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/81XsRJEH2kL.jpg',
                'stock_quantity': 12
            },
            {
                'title': 'Watchmen',
                'author': 'Alan Moore',
                'price_npr': 1600.00,
                'category': 'Graphic Novels',
                'description': 'In an alternate world where superheroes have changed the course of history, one hero\'s murder leads to a conspiracy that threatens the entire world. Watchmen is a groundbreaking graphic novel that deconstructs the superhero genre while exploring themes of power, morality, and the human condition. Alan Moore and Dave Gibbons created this dark, complex narrative that remains one of the most influential comics ever published.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/81dKWNOz3lL.jpg',
                'stock_quantity': 16
            },
            {
                'title': 'Sapiens: A Brief History of Humankind',
                'author': 'Yuval Noah Harari',
                'price_npr': 1250.00,
                'category': 'Reference',
                'description': 'From a renowned historian comes a groundbreaking narrative of humanity\'s creation and evolution that explores the ways in which biology and history have defined us. Sapiens challenges everything we thought we knew about being human: our thoughts, our actions, our heritage, and our future. This international bestseller takes readers on a journey through 100,000 years of Homo sapiens history.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/713jIoMO3UL.jpg',
                'stock_quantity': 33
            },
            {
                'title': 'The 4-Hour Workweek',
                'author': 'Timothy Ferriss',
                'price_npr': 1050.00,
                'category': 'Investing',
                'description': 'Forget the old concept of retirement and the rest of the deferred-life plan – there is no need to wait and every reason not to. Whether your dream is escaping the rat race, experiencing high-end world travel, earning a monthly five-figure income with zero management, or just living more and working less, The 4-Hour Workweek is the blueprint for achieving it.',
                'image_url': 'https://images-na.ssl-images-amazon.com/images/I/81qw+-dFwbL.jpg',
                'stock_quantity': 27
            }
        ]
        
        for book_data in books_data:
            book = Book(**book_data)
            db.session.add(book)
        
        # Commit all books
        db.session.commit()
        
        print(f"\n{'='*50}")
        print("Database initialization complete!")
        print(f"{'='*50}")
        print(f"✓ Created {User.query.count()} users")
        print(f"✓ Created {Book.query.count()} books")
        print(f"\nAdmin Credentials:")
        print(f"  Username: admin")
        print(f"  Password: admin123")
        print(f"\nTest User Credentials:")
        print(f"  Username: john_doe")
        print(f"  Password: password123")
        print(f"{'='*50}\n")


if __name__ == '__main__':
    init_database()
