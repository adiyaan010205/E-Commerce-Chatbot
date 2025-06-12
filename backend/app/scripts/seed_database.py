import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
import random
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.product import Product
from app.models.user import User
from app.core.security import get_password_hash

fake = Faker()

# Product categories and their typical items
PRODUCT_DATA = {
    "Electronics": {
        "items": [
            "Smartphone", "Laptop", "Tablet", "Headphones", "Smart Watch", 
            "Bluetooth Speaker", "Gaming Console", "TV", "Camera", "Router"
        ],
        "brands": ["Apple", "Samsung", "Sony", "LG", "Dell", "HP", "Asus", "Microsoft"],
        "price_range": (50, 2000)
    },
    "Clothing": {
        "items": [
            "T-Shirt", "Jeans", "Dress", "Jacket", "Sneakers", "Boots", 
            "Sweater", "Shirt", "Pants", "Hoodie"
        ],
        "brands": ["Nike", "Adidas", "Zara", "H&M", "Levi's", "Puma", "Under Armour"],
        "price_range": (20, 300)
    },
    "Books": {
        "items": [
            "Fiction Novel", "Science Textbook", "Biography", "Cookbook", 
            "Self-Help Book", "History Book", "Art Book", "Children's Book"
        ],
        "brands": ["Penguin", "Random House", "HarperCollins", "Scholastic", "O'Reilly"],
        "price_range": (10, 80)
    },
    "Home & Garden": {
        "items": [
            "Coffee Maker", "Vacuum Cleaner", "Bedding Set", "Garden Tools", 
            "Dinnerware", "Lamp", "Mirror", "Plant Pot", "Kitchen Knife Set"
        ],
        "brands": ["IKEA", "KitchenAid", "Dyson", "Black & Decker", "Cuisinart"],
        "price_range": (25, 500)
    },
    "Sports & Outdoors": {
        "items": [
            "Basketball", "Yoga Mat", "Dumbbells", "Hiking Boots", "Tent", 
            "Bicycle", "Swimming Goggles", "Running Shoes", "Fitness Tracker"
        ],
        "brands": ["Nike", "Adidas", "Coleman", "Wilson", "Spalding", "Reebok"],
        "price_range": (15, 800)
    },
    "Beauty & Personal Care": {
        "items": [
            "Face Cream", "Shampoo", "Perfume", "Makeup Kit", "Electric Toothbrush", 
            "Hair Dryer", "Skincare Set", "Razor", "Nail Polish"
        ],
        "brands": ["L'Oreal", "Maybelline", "Neutrogena", "Oral-B", "Gillette"],
        "price_range": (8, 200)
    }
}

def create_sample_products(db: Session, num_products: int = 120):
    """Create sample products for the database"""
    print(f"Creating {num_products} sample products...")
    
    for i in range(num_products):
        # Choose random category
        category = random.choice(list(PRODUCT_DATA.keys()))
        category_data = PRODUCT_DATA[category]
        
        # Generate product details
        item_name = random.choice(category_data["items"])
        brand = random.choice(category_data["brands"])
        
        # Create more specific product titles
        color_adjectives = ["Black", "White", "Blue", "Red", "Silver", "Gold", "Green"]
        size_adjectives = ["Compact", "Large", "Mini", "Professional", "Premium", "Deluxe"]
        
        if random.choice([True, False]):
            adjective = random.choice(color_adjectives + size_adjectives)
            title = f"{adjective} {brand} {item_name}"
        else:
            title = f"{brand} {item_name}"
        
        # Generate price within category range
        min_price, max_price = category_data["price_range"]
        price = round(random.uniform(min_price, max_price), 2)
        
        # Generate description
        features = [
            "High quality materials", "Durable construction", "Modern design",
            "Easy to use", "Energy efficient", "Lightweight", "Portable",
            "Professional grade", "User-friendly", "Innovative technology"
        ]
        
        description = f"Premium {item_name.lower()} from {brand}. Features {random.choice(features).lower()}, {random.choice(features).lower()}, and {random.choice(features).lower()}. Perfect for daily use and designed to last."
        
        # Generate image URL (using placeholder service)
        image_url = f"https://picsum.photos/400/300?random={i}"
        
        # Create product
        product = Product(
            title=title,
            description=description,
            price=price,
            category=category,
            image_url=image_url,
            brand=brand,
            rating=round(random.uniform(3.0, 5.0), 1),
            stock_quantity=random.randint(0, 100),
            is_active=True
        )
        
        db.add(product)
        
        if i % 20 == 0:
            print(f"Created {i} products...")
            db.commit()
    
    db.commit()
    print(f"✅ Successfully created {num_products} products!")

def create_sample_users(db: Session):
    """Create sample users for testing"""
    print("Creating sample users...")
    
    # Create admin user
    admin_user = User(
        email="admin@uplyft.com",
        hashed_password=get_password_hash("admin123"),
        first_name="Admin",
        last_name="User",
        is_active=True
    )
    db.add(admin_user)
    
    # Create test user
    test_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("test123"),
        first_name="Test",
        last_name="User",
        is_active=True
    )
    db.add(test_user)
    
    # Create additional sample users
    for i in range(5):
        user = User(
            email=fake.email(),
            hashed_password=get_password_hash("password123"),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            is_active=True
        )
        db.add(user)
    
    db.commit()
    print("✅ Successfully created sample users!")
    print("Admin user: admin@uplyft.com / admin123")
    print("Test user: test@example.com / test123")

def seed_database():
    """Main seeding function"""
    print("🌱 Starting database seeding...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_products = db.query(Product).count()
        existing_users = db.query(User).count()
        
        if existing_products > 0 or existing_users > 0:
            print(f"Database already has {existing_products} products and {existing_users} users")
            response = input("Do you want to clear existing data? (y/N): ")
            if response.lower() == 'y':
                print("Clearing existing data...")
                db.query(Product).delete()
                db.query(User).delete()
                db.commit()
        
        # Create sample data
        create_sample_users(db)
        create_sample_products(db, 120)
        
        print("🎉 Database seeding completed successfully!")
        
        # Show summary
        total_products = db.query(Product).count()
        total_users = db.query(User).count()
        categories = db.query(Product.category).distinct().count()
        
        print(f"\n📊 Database Summary:")
        print(f"Total Products: {total_products}")
        print(f"Total Users: {total_users}")
        print(f"Product Categories: {categories}")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
