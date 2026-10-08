from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from database import get_db_connection, initialize_database

app = Flask(__name__)
CORS(app)

# Create database and tables
initialize_database()


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Library Management System API is running"
    })


# ---------------------------------------------------------
# GET ALL BOOKS
# ---------------------------------------------------------

@app.route("/api/books", methods=["GET"])
def get_books():

    connection = get_db_connection()

    books = connection.execute("""
        SELECT
            id,
            title,
            author,
            isbn,
            category,
            available
        FROM books
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    result = []

    for book in books:
        result.append({
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "isbn": book["isbn"],
            "category": book["category"],
            "available": bool(book["available"])
        })

    return jsonify(result)


# ---------------------------------------------------------
# SEARCH BOOKS
# ---------------------------------------------------------

@app.route("/api/books/search", methods=["GET"])
def search_books():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Search query is required"
        }), 400

    connection = get_db_connection()

    books = connection.execute("""
        SELECT
            id,
            title,
            author,
            isbn,
            category,
            available
        FROM books
        WHERE title LIKE ?
           OR author LIKE ?
           OR isbn LIKE ?
           OR category LIKE ?
        ORDER BY id DESC
    """, (
        f"%{query}%",
        f"%{query}%",
        f"%{query}%",
        f"%{query}%"
    )).fetchall()

    connection.close()

    result = []

    for book in books:
        result.append({
            "id": book["id"],
            "title": book["title"],
            "author": book["author"],
            "isbn": book["isbn"],
            "category": book["category"],
            "available": bool(book["available"])
        })

    return jsonify(result)


# ---------------------------------------------------------
# ADD BOOK
# ---------------------------------------------------------

@app.route("/api/books", methods=["POST"])
def add_book():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    title = data.get("title", "").strip()
    author = data.get("author", "").strip()
    isbn = data.get("isbn", "").strip()
    category = data.get("category", "").strip()

    # Validation
    if not title or not author or not isbn or not category:
        return jsonify({
            "error": "All book fields are required"
        }), 400

    connection = get_db_connection()

    # Check duplicate ISBN
    existing_book = connection.execute(
        "SELECT id FROM books WHERE isbn = ?",
        (isbn,)
    ).fetchone()

    if existing_book:
        connection.close()

        return jsonify({
            "error": "A book with this ISBN already exists"
        }), 409

    connection.execute("""
        INSERT INTO books
        (title, author, isbn, category, available)
        VALUES (?, ?, ?, ?, 1)
    """, (
        title,
        author,
        isbn,
        category
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Book added successfully"
    }), 201


# ---------------------------------------------------------
# DELETE BOOK
# ---------------------------------------------------------

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):

    connection = get_db_connection()

    book = connection.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    ).fetchone()

    if not book:
        connection.close()

        return jsonify({
            "error": "Book not found"
        }), 404

    # Don't allow deleting an issued book
    if book["available"] == 0:
        connection.close()

        return jsonify({
            "error": "Issued book cannot be deleted. Return the book first."
        }), 400

    connection.execute(
        "DELETE FROM books WHERE id = ?",
        (book_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Book deleted successfully"
    })


# ---------------------------------------------------------
# GET MEMBERS
# ---------------------------------------------------------

@app.route("/api/members", methods=["GET"])
def get_members():

    connection = get_db_connection()

    members = connection.execute("""
        SELECT id, name, email, phone
        FROM members
        ORDER BY name
    """).fetchall()

    connection.close()

    result = []

    for member in members:
        result.append({
            "id": member["id"],
            "name": member["name"],
            "email": member["email"],
            "phone": member["phone"]
        })

    return jsonify(result)


# ---------------------------------------------------------
# ADD MEMBER
# ---------------------------------------------------------

@app.route("/api/members", methods=["POST"])
def add_member():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received"
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()

    if not name:
        return jsonify({
            "error": "Member name is required"
        }), 400

    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO members
        (name, email, phone)
        VALUES (?, ?, ?)
    """, (
        name,
        email,
        phone
    ))

    connection.commit()

    member_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Member added successfully",
        "id": member_id
    }), 201


# ---------------------------------------------------------
# ISSUE BOOK
# ---------------------------------------------------------

@app.route("/api/books/<int:book_id>/issue", methods=["PUT"])
def issue_book(book_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Member information is required"
        }), 400

    member_id = data.get("member_id")

    if not member_id:
        return jsonify({
            "error": "Member ID is required"
        }), 400

    connection = get_db_connection()

    # Check book
    book = connection.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    ).fetchone()

    if not book:
        connection.close()

        return jsonify({
            "error": "Book not found"
        }), 404

    # Check availability
    if book["available"] == 0:
        connection.close()

        return jsonify({
            "error": "Book is already issued"
        }), 400

    # Check member
    member = connection.execute(
        "SELECT * FROM members WHERE id = ?",
        (member_id,)
    ).fetchone()

    if not member:
        connection.close()

        return jsonify({
            "error": "Member not found"
        }), 404

    issue_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create issue record
    connection.execute("""
        INSERT INTO issue_records
        (book_id, member_id, issue_date)
        VALUES (?, ?, ?)
    """, (
        book_id,
        member_id,
        issue_date
    ))

    # Mark book unavailable
    connection.execute("""
        UPDATE books
        SET available = 0
        WHERE id = ?
    """, (book_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Book issued successfully"
    })


# ---------------------------------------------------------
# RETURN BOOK
# ---------------------------------------------------------

@app.route("/api/books/<int:book_id>/return", methods=["PUT"])
def return_book(book_id):

    connection = get_db_connection()

    book = connection.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)
    ).fetchone()

    if not book:
        connection.close()

        return jsonify({
            "error": "Book not found"
        }), 404

    # Book is already available
    if book["available"] == 1:
        connection.close()

        return jsonify({
            "error": "Book has not been issued"
        }), 400

    return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Find active issue record
    issue_record = connection.execute("""
        SELECT *
        FROM issue_records
        WHERE book_id = ?
        AND return_date IS NULL
        ORDER BY id DESC
        LIMIT 1
    """, (book_id,)).fetchone()

    if not issue_record:
        connection.close()

        return jsonify({
            "error": "No active issue record found"
        }), 400

    # Update issue record
    connection.execute("""
        UPDATE issue_records
        SET return_date = ?
        WHERE id = ?
    """, (
        return_date,
        issue_record["id"]
    ))

    # Make book available
    connection.execute("""
        UPDATE books
        SET available = 1
        WHERE id = ?
    """, (book_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Book returned successfully"
    })


# ---------------------------------------------------------
# ISSUE RECORDS
# ---------------------------------------------------------

@app.route("/api/issues", methods=["GET"])
def get_issue_records():

    connection = get_db_connection()

    records = connection.execute("""
        SELECT
            issue_records.id,
            books.title AS book_title,
            members.name AS member_name,
            issue_records.issue_date,
            issue_records.return_date
        FROM issue_records
        JOIN books
            ON issue_records.book_id = books.id
        JOIN members
            ON issue_records.member_id = members.id
        ORDER BY issue_records.id DESC
    """).fetchall()

    connection.close()

    result = []

    for record in records:
        result.append({
            "id": record["id"],
            "book_title": record["book_title"],
            "member_name": record["member_name"],
            "issue_date": record["issue_date"],
            "return_date": record["return_date"]
        })

    return jsonify(result)


# ---------------------------------------------------------
# RUN SERVER
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)