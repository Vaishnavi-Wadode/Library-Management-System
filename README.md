# 📚 Library Management System

A full-stack Library Management System developed using HTML, CSS,
JavaScript, Python Flask and SQLite.

## 🎯 Aim

To design and develop a Library Management System that allows users
to add, search, issue, return and delete books while demonstrating
CRUD operations and frontend-backend communication.

## 🛠️ Technologies Used

- HTML
- CSS
- JavaScript
- Node.js
- Python
- Flask
- SQLite
- REST API
- Fetch API
- JSON

## ✨ Features

### Books

- Add new book
- View all books
- Search books
- Issue books
- Return books
- Delete books
- Check availability

### Members

- Add members
- View members
- Store member details

### Issue Management

- Issue book to a member
- Return book
- Maintain issue history
- Prevent issuing an already issued book

### Validation

- Required fields
- Duplicate ISBN checking
- Book availability checking
- Member validation
- Invalid return validation
- Prevent deletion of issued books

## 📁 Project Structure

library-management-system/

├── frontend/

│   ├── index.html

│   ├── style.css

│   └── script.js

│

├── backend/

│   ├── app.py

│   ├── database.py

│   └── library.db

│

├── package.json

└── README.md

## 🚀 How to Run

### 1. Install Python

Make sure Python is installed.

Check:

python --version

### 2. Install Flask

Open the terminal inside the project folder:

pip install flask flask-cors

### 3. Start Flask

Run:

python backend/app.py

You should see:

Running on http://127.0.0.1:5000

### 4. Open the Frontend

Open:

frontend/index.html

in your browser.

## 🗄️ Database

SQLite is used as the database.

The following tables are created automatically:

- books
- members
- issue_records

The database file is:

backend/library.db

## 🔌 API Endpoints

### Books

GET /api/books

POST /api/books

GET /api/books/search?q=keyword

DELETE /api/books/<id>

PUT /api/books/<id>/issue

PUT /api/books/<id>/return

### Members

GET /api/members

POST /api/members

### Issue Records

GET /api/issues

## 🔄 Application Flow

User
↓
HTML/CSS/JavaScript
↓
Fetch API
↓
Flask REST API
↓
Business Logic
↓
SQLite Database
↓
JSON Response
↓
Updated Web Page

## 🎓 Learning Outcomes

Through this project, students understand:

- Full-stack web development
- CRUD operations
- RESTful APIs
- Flask backend development
- SQLite database management
- Frontend-backend communication
- JSON
- Fetch API
- Form validation
- Database relationships