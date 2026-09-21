# Student Management System

A full-stack Student Management System developed using **Python, Flask, MySQL, HTML, CSS, and JavaScript**.

The application allows users to manage student records, calculate marks and percentages, generate grades, identify qualified and failed students, and display the topper.

## Features

* Add student details
* View all students
* Search student by ID or name
* Update student details
* Delete student records
* Calculate total marks
* Calculate percentage
* Generate student grades
* Display topper
* Display qualified students
* Display failed students
* Dashboard with student statistics
* MySQL database integration
* Flask REST API
* Frontend and backend integration using JavaScript Fetch API
* CORS support

## Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS

### Database

* MySQL
* MySQL Connector for Python

## Project Structure

```text
STUDENT_MS/
│
├── backend/
│   ├── main.py
│   └── api.py
│
├── frontend/
│   ├── index.html
│   ├── students.html
│   ├── add-student.html
│   ├── search.html
│   ├── update-student.html
│   ├── delete-student.html
│   ├── results.html
│   ├── topper.html
│   ├── qualified.html
│   ├── failed.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

## Database Setup

Create the database in MySQL:

```sql
CREATE DATABASE student_db;
```

Select the database:

```sql
USE student_db;
```

Create the student table:

```sql
CREATE TABLE student_details (
    student_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(20),
    maths INT,
    statistics INT,
    computer_science INT,
    english INT,
    hr_ethics INT
);
```

## Backend Configuration

The Flask API connects to MySQL using the following configuration:

```python
host="localhost"
user="root"
password="mysql@123"
database="student_db"
```

Update the password in `api.py` if your MySQL password is different.

## Installation

Open the terminal inside the backend folder:

```bash
cd backend
```

Install the required packages:

```bash
pip install flask flask-cors mysql-connector-python
```

## Run the Backend

Start the Flask API:

```bash
python api.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## Test the API

Open the following URL in your browser:

```text
http://127.0.0.1:5000/
```

Expected response:

```json
{
    "message": "Student Management System API is running"
}
```

### Test Database Connection

Open:

```text
http://127.0.0.1:5000/test-db
```

Expected response:

```json
{
    "message": "MySQL Connected Successfully"
}
```

### View Students

```text
GET /students
```

Example:

```text
http://127.0.0.1:5000/students
```

### Add Student

```text
POST /students
```

Example JSON:

```json
{
    "student_name": "Anvesh",
    "maths": 85,
    "statistics": 80,
    "computer_science": 90,
    "english": 75,
    "hr_ethics": 88
}
```

### Search Student

```text
GET /search/<student_id_or_name>
```

Example:

```text
http://127.0.0.1:5000/search/1
```

or:

```text
http://127.0.0.1:5000/search/Anvesh
```

### Update Student

```text
PUT /students/<student_id>
```

### Delete Student

```text
DELETE /students/<student_id>
```

### Student Results

```text
GET /results
```

### Topper

```text
GET /topper
```

### Qualified Students

```text
GET /qualified
```

### Failed Students

```text
GET /failed
```

### Dashboard

```text
GET /dashboard
```

## Grading System

The system calculates grades based on percentage:

| Percentage | Grade |
| ---------- | ----- |
| 90 - 100   | A     |
| 80 - 89    | B     |
| 70 - 79    | C     |
| 60 - 69    | D     |
| 50 - 59    | E     |
| Below 50   | F     |

## Qualification Criteria

A student is considered **Qualified** when they score at least **35 marks in every subject**.

If a student scores below 35 in any subject, the student is classified as **Failed**.

## Application Flow

```text
HTML
   ↓
CSS
   ↓
JavaScript
   ↓
Fetch API
   ↓
Flask REST API
   ↓
Python
   ↓
MySQL Database
```

## API Flow

```text
Frontend
   ↓
script.js
   ↓
HTTP Request
   ↓
Flask api.py
   ↓
MySQL
   ↓
JSON Response
   ↓
Frontend
```

## How to Run the Project

### Step 1: Start MySQL

Make sure MySQL Server is running.

### Step 2: Start Flask Backend

```bash
cd backend
python api.py
```

### Step 3: Start Frontend

Open the `frontend` folder in VS Code.

Use **Live Server** to open:

```text
index.html
```

The frontend communicates with Flask through:

```text
http://127.0.0.1:5000
```

## Important

Do not run `script.js` using Node.js.

```bash
node script.js
```

should not be used because `script.js` uses browser objects such as:

```javascript
document
```

Instead:

1. Run `python api.py`
2. Start the frontend using Live Server
3. Open `index.html` in the browser

## Future Improvements

* User authentication and login
* Admin dashboard
* Student profile management
* Attendance management
* Subject-wise performance charts
* Export student results to PDF
* Export student data to Excel
* Email notifications
* Responsive mobile application

## Author

**Anvesh Arepally**

GitHub: `https://github.com/ArepallyAnvesh`

LinkedIn: `https://www.linkedin.com/in/arepally-anvesh-1a1438298/`

## License

This project is created for learning and educational purposes.
