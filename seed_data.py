from database import get_db_connection


books = [
    ("Clean Code", "Robert C. Martin", "9780132350884", "Programming"),
    ("Atomic Habits", "James Clear", "9780735211292", "Self Help"),
    ("The Alchemist", "Paulo Coelho", "9780062315007", "Fiction"),
    ("Rich Dad Poor Dad", "Robert Kiyosaki", "9781612680194", "Finance"),
    ("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "9780590353427", "Fiction"),
    ("Python Crash Course", "Eric Matthes", "9781593279288", "Programming"),
    ("Don't Make Me Think", "Steve Krug", "9780321344755", "Web Development"),
    ("Introduction to Algorithms", "Thomas H. Cormen", "9780262046305", "Algorithms"),
    ("Database System Concepts", "Abraham Silberschatz", "9780073523323", "Database"),
    ("Artificial Intelligence: A Modern Approach", "Stuart Russell", "9780134610993", "AI")
]


members = [
    ("Aarav Sharma", "aarav@example.com", "9098572601"),
    ("Ananya Patil", "ananya@example.com", "9082085402"),
    ("Rohan Verma", "rohan@example.com", "9985437843"),
    ("Sneha Joshi", "sneha@example.com", "9006587544"),
    ("Rahila Khan", "rahila@example.com", "9098433455"),
    ("Kanika Sharma", "kanika@example.com", "9876445685"),
    ("Rahul Mehta", "rahul@example.com", "9098433455"),
    ("Tarak Mehta", "tarak@example.com", "9543896290"),
    ("Rahul Shukla", "rahul@example.com", "9854378435"),
    ("Satendra Mishra", "sattu@example.com", "8985437843")
]


connection = get_db_connection()

# Add books
for book in books:
    connection.execute("""
        INSERT OR IGNORE INTO books
        (title, author, isbn, category, available)
        VALUES (?, ?, ?, ?, 1)
    """, book)


# Add members
for member in members:
    connection.execute("""
        INSERT INTO members
        (name, email, phone)
        VALUES (?, ?, ?)
    """, member)


connection.commit()
connection.close()

print("Sample data added successfully!")
print("10 books and 5 members have been added.")