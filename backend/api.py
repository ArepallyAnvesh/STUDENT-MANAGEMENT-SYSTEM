import mysql.connector
from flask import Flask,request,jsonify
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="##########",
        database="student_db"
    )

def calculate_total(maths,statistics,computer_science,english,hr_ethics):
    return maths+statistics+computer_science+english+hr_ethics

def calculate_percentage(total):
    return round((total/500)*100,2)

def calculate_grade(percentage):
    if percentage>=90:
        return "A"
    elif percentage>=80:
        return "B"
    elif percentage>=70:
        return "C"
    elif percentage>=60:
        return "D"
    elif percentage>=50:
        return "E"
    else:
        return "F"

def check_qualified(maths,statistics,computer_science,english,hr_ethics):
    return (
        maths>=35 and
        statistics>=35 and
        computer_science>=35 and
        english>=35 and
        hr_ethics>=35
    )

def make_student(row):
    return {
        "student_id":row[0],
        "student_name":row[1],
        "maths":row[2],
        "statistics":row[3],
        "computer_science":row[4],
        "english":row[5],
        "hr_ethics":row[6]
    }

@app.route("/")
def home():
    return jsonify({
        "message":"Student Management System API is running"
    })

@app.route("/test-db")
def test_db():
    connect=None
    cursor=None

    try:
        connect=get_connection()
        cursor=connect.cursor()

        cursor.execute("SELECT 1")
        cursor.fetchone()

        return jsonify({
            "message":"MySQL Connected Successfully"
        })

    except Exception as e:
        print("DATABASE ERROR:",e)

        return jsonify({
            "message":"Database Connection Failed",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.route("/students",methods=["GET"])
def get_students():
    connect=None
    cursor=None

    try:
        connect=get_connection()
        cursor=connect.cursor()

        cursor.execute("""
        SELECT student_id,
        student_name,
        maths,
        statistics,
        computer_science,
        english,
        hr_ethics
        FROM student_details
        """)

        rows=cursor.fetchall()

        students=[]

        for row in rows:
            students.append(make_student(row))

        return jsonify(students)

    except Exception as e:
        print("GET STUDENTS ERROR:",e)

        return jsonify({
            "message":"Error loading students",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.route("/students",methods=["POST"])
def add_student():
    connect=None
    cursor=None

    try:
        data=request.get_json()

        print("DATA RECEIVED:",data)

        if not data:
            return jsonify({
                "message":"No data received"
            }),400

        name=str(data.get("student_name","")).strip()

        if not name:
            return jsonify({
                "message":"Student name is required"
            }),400

        maths=int(data.get("maths"))
        statistics=int(data.get("statistics"))
        computer_science=int(data.get("computer_science"))
        english=int(data.get("english"))
        hr_ethics=int(data.get("hr_ethics"))

        marks=[
            maths,
            statistics,
            computer_science,
            english,
            hr_ethics
        ]

        for mark in marks:
            if mark<0 or mark>100:
                return jsonify({
                    "message":"Marks must be between 0 and 100"
                }),400

        connect=get_connection()
        cursor=connect.cursor()

        query="""
        INSERT INTO student_details
        (
        student_name,
        maths,
        statistics,
        computer_science,
        english,
        hr_ethics
        )
        VALUES(%s,%s,%s,%s,%s,%s)
        """

        values=(
            name,
            maths,
            statistics,
            computer_science,
            english,
            hr_ethics
        )

        cursor.execute(query,values)

        connect.commit()

        student_id=cursor.lastrowid

        return jsonify({
            "message":"Student added successfully",
            "student_id":student_id
        }),201

    except ValueError:
        return jsonify({
            "message":"Marks must be valid numbers"
        }),400

    except Exception as e:
        print("ADD STUDENT ERROR:",e)

        if connect:
            connect.rollback()

        return jsonify({
            "message":"Error adding student",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.route("/search/<search>",methods=["GET"])
def search_student(search):
    connect=None
    cursor=None

    try:
        connect=get_connection()
        cursor=connect.cursor()

        try:
            student_id=int(search)
        except:
            student_id=-1

        query="""
        SELECT student_id,
        student_name,
        maths,
        statistics,
        computer_science,
        english,
        hr_ethics
        FROM student_details
        WHERE student_id=%s
        OR student_name LIKE %s
        """

        cursor.execute(
            query,
            (
                student_id,
                "%"+search+"%"
            )
        )

        rows=cursor.fetchall()

        students=[]

        for row in rows:
            students.append(make_student(row))

        return jsonify(students)

    except Exception as e:
        print("SEARCH ERROR:",e)

        return jsonify({
            "message":"Error searching student",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.route("/students/<int:student_id>",methods=["PUT"])
def update_student(student_id):
    connect=None
    cursor=None

    try:
        data=request.get_json()

        if not data:
            return jsonify({
                "message":"No data received"
            }),400

        name=str(data.get("student_name","")).strip()

        if not name:
            return jsonify({
                "message":"Student name is required"
            }),400

        maths=int(data.get("maths"))
        statistics=int(data.get("statistics"))
        computer_science=int(data.get("computer_science"))
        english=int(data.get("english"))
        hr_ethics=int(data.get("hr_ethics"))

        marks=[
            maths,
            statistics,
            computer_science,
            english,
            hr_ethics
        ]

        for mark in marks:
            if mark<0 or mark>100:
                return jsonify({
                    "message":"Marks must be between 0 and 100"
                }),400

        connect=get_connection()
        cursor=connect.cursor()

        cursor.execute(
            "SELECT student_id FROM student_details WHERE student_id=%s",
            (student_id,)
        )

        student=cursor.fetchone()

        if not student:
            return jsonify({
                "message":"Student not found"
            }),404

        query="""
        UPDATE student_details
        SET student_name=%s,
        maths=%s,
        statistics=%s,
        computer_science=%s,
        english=%s,
        hr_ethics=%s
        WHERE student_id=%s
        """

        values=(
            name,
            maths,
            statistics,
            computer_science,
            english,
            hr_ethics,
            student_id
        )

        cursor.execute(query,values)

        connect.commit()

        return jsonify({
            "message":"Student updated successfully"
        })

    except ValueError:
        return jsonify({
            "message":"Invalid student data"
        }),400

    except Exception as e:
        print("UPDATE ERROR:",e)

        if connect:
            connect.rollback()

        return jsonify({
            "message":"Error updating student",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.route("/students/<int:student_id>",methods=["DELETE"])
def delete_student(student_id):
    connect=None
    cursor=None

    try:
        connect=get_connection()
        cursor=connect.cursor()

        cursor.execute(
            "SELECT student_id FROM student_details WHERE student_id=%s",
            (student_id,)
        )

        student=cursor.fetchone()

        if not student:
            return jsonify({
                "message":"Student not found"
            }),404

        cursor.execute(
            "DELETE FROM student_details WHERE student_id=%s",
            (student_id,)
        )

        connect.commit()

        return jsonify({
            "message":"Student deleted successfully"
        })

    except Exception as e:
        print("DELETE ERROR:",e)

        if connect:
            connect.rollback()

        return jsonify({
            "message":"Error deleting student",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.route("/results",methods=["GET"])
def get_results():
    connect=None
    cursor=None

    try:
        connect=get_connection()
        cursor=connect.cursor()

        cursor.execute("""
        SELECT student_id,
        student_name,
        maths,
        statistics,
        computer_science,
        english,
        hr_ethics
        FROM student_details
        """)

        rows=cursor.fetchall()

        results=[]

        for row in rows:

            student_id=row[0]
            name=row[1]
            maths=row[2]
            statistics=row[3]
            computer_science=row[4]
            english=row[5]
            hr_ethics=row[6]

            total=calculate_total(
                maths,
                statistics,
                computer_science,
                english,
                hr_ethics
            )

            percentage=calculate_percentage(total)
            grade=calculate_grade(percentage)

            if check_qualified(
                maths,
                statistics,
                computer_science,
                english,
                hr_ethics
            ):
                status="Qualified"
            else:
                status="Failed"

            results.append({
                "student_id":student_id,
                "student_name":name,
                "total":total,
                "percentage":percentage,
                "grade":grade,
                "status":status
            })

        return jsonify(results)

    except Exception as e:
        print("RESULTS ERROR:",e)

        return jsonify({
            "message":"Error loading results",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.route("/topper",methods=["GET"])
def get_topper():
    connect=None
    cursor=None

    try:
        connect=get_connection()
        cursor=connect.cursor()

        query="""
        SELECT student_id,
        student_name,
        maths,
        statistics,
        computer_science,
        english,
        hr_ethics,
        (
        maths+
        statistics+
        computer_science+
        english+
        hr_ethics
        ) AS total
        FROM student_details
        ORDER BY total DESC
        LIMIT 1
        """

        cursor.execute(query)

        row=cursor.fetchone()

        if not row:
            return jsonify({
                "student_id":None,
                "student_name":"-",
                "maths":0,
                "statistics":0,
                "computer_science":0,
                "english":0,
                "hr_ethics":0,
                "total":0,
                "percentage":0,
                "grade":"-"
            })

        total=row[7]

        percentage=calculate_percentage(total)
        grade=calculate_grade(percentage)

        return jsonify({
            "student_id":row[0],
            "student_name":row[1],
            "maths":row[2],
            "statistics":row[3],
            "computer_science":row[4],
            "english":row[5],
            "hr_ethics":row[6],
            "total":total,
            "percentage":percentage,
            "grade":grade
        })

    except Exception as e:
        print("TOPPER ERROR:",e)

        return jsonify({
            "message":"Error loading topper",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.route("/qualified",methods=["GET"])
def get_qualified():
    connect=None
    cursor=None

    try:
        connect=get_connection()
        cursor=connect.cursor()

        cursor.execute("""
        SELECT student_id,
        student_name,
        maths,
        statistics,
        computer_science,
        english,
        hr_ethics
        FROM student_details
        """)

        rows=cursor.fetchall()

        students=[]

        for row in rows:

            maths=row[2]
            statistics=row[3]
            computer_science=row[4]
            english=row[5]
            hr_ethics=row[6]

            if check_qualified(
                maths,
                statistics,
                computer_science,
                english,
                hr_ethics
            ):

                total=calculate_total(
                    maths,
                    statistics,
                    computer_science,
                    english,
                    hr_ethics
                )

                percentage=calculate_percentage(total)

                students.append({
                    "student_id":row[0],
                    "student_name":row[1],
                    "maths":maths,
                    "statistics":statistics,
                    "computer_science":computer_science,
                    "english":english,
                    "hr_ethics":hr_ethics,
                    "total":total,
                    "percentage":percentage
                })

        return jsonify(students)

    except Exception as e:
        print("QUALIFIED ERROR:",e)

        return jsonify({
            "message":"Error loading qualified students",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.route("/failed",methods=["GET"])
def get_failed():
    connect=None
    cursor=None

    try:
        connect=get_connection()
        cursor=connect.cursor()

        cursor.execute("""
        SELECT student_id,
        student_name,
        maths,
        statistics,
        computer_science,
        english,
        hr_ethics
        FROM student_details
        """)

        rows=cursor.fetchall()

        students=[]

        for row in rows:

            maths=row[2]
            statistics=row[3]
            computer_science=row[4]
            english=row[5]
            hr_ethics=row[6]

            if not check_qualified(
                maths,
                statistics,
                computer_science,
                english,
                hr_ethics
            ):

                total=calculate_total(
                    maths,
                    statistics,
                    computer_science,
                    english,
                    hr_ethics
                )

                percentage=calculate_percentage(total)

                students.append({
                    "student_id":row[0],
                    "student_name":row[1],
                    "maths":maths,
                    "statistics":statistics,
                    "computer_science":computer_science,
                    "english":english,
                    "hr_ethics":hr_ethics,
                    "total":total,
                    "percentage":percentage
                })

        return jsonify(students)

    except Exception as e:
        print("FAILED ERROR:",e)

        return jsonify({
            "message":"Error loading failed students",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.route("/dashboard",methods=["GET"])
def dashboard():
    connect=None
    cursor=None

    try:
        connect=get_connection()
        cursor=connect.cursor()

        cursor.execute("SELECT COUNT(*) FROM student_details")

        total_students=cursor.fetchone()[0]

        cursor.execute("""
        SELECT student_name,
        maths,
        statistics,
        computer_science,
        english,
        hr_ethics
        FROM student_details
        """)

        rows=cursor.fetchall()

        qualified_students=0
        failed_students=0
        topper="-"
        highest_total=-1

        for row in rows:

            name=row[0]
            maths=row[1]
            statistics=row[2]
            computer_science=row[3]
            english=row[4]
            hr_ethics=row[5]

            total=calculate_total(
                maths,
                statistics,
                computer_science,
                english,
                hr_ethics
            )

            if check_qualified(
                maths,
                statistics,
                computer_science,
                english,
                hr_ethics
            ):
                qualified_students+=1
            else:
                failed_students+=1

            if total>highest_total:
                highest_total=total
                topper=name

        return jsonify({
            "total_students":total_students,
            "qualified_students":qualified_students,
            "failed_students":failed_students,
            "topper":topper
        })

    except Exception as e:
        print("DASHBOARD ERROR:",e)

        return jsonify({
            "message":"Error loading dashboard",
            "error":str(e)
        }),500

    finally:
        if cursor:
            cursor.close()

        if connect:
            connect.close()

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "message":"API endpoint not found"
    }),404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "message":"Internal server error",
        "error":str(error)
    }),500

if __name__=="__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
