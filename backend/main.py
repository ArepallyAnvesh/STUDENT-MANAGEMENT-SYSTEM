import mysql.connector
from flask import Flask
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

class student_details:
    def __init__(self):
        self.connect=mysql.connector.connect(
            host="localhost",
            user="root",
            password="#########",
            database="student_db")
        self.cusor=self.connect.cursor()
        print(" DATABASE CONNECTED SUCCESSFULLY ")

    def add_student(self):
        while True:
            self.name = input("Enter your name: ").strip()
            if self.name and self.name.replace(" ", "").isalpha():
                break
            print("Invalid name. Please enter alphabets only.")
        while True:
            self.maths=input("enter your Maths Marks : ").strip()
            if not self.maths.isdigit():
                print("Enter numbers only.")
            elif self.maths.isdigit():
                if int(self.maths) <= 0 or int(self.maths) > 100:  #0<=int(self.math)<=100
                    print("Marks should be between 0 and 100.")
                else:
                    self.maths=int(self.maths)
                    break
        
        while True:
            self.statics=input("enter your Statics Marks : ").strip()
            if not self.statics.isdigit():
                print("Enter numbers only.")
            elif self.statics.isdigit():
                if int(self.statics) < 0 or int(self.statics) > 100:
                    print("Marks should be between 0 and 100.")
                else:
                    self.statics=int(self.statics)
                    break

        while True:
            self.computer_science=input("enter your Computer Science Marks : ").strip()
            if not self.computer_science.isdigit():
                print("Enter numbers only.")
            elif self.computer_science.isdigit():
                if int(self.computer_science) < 0 or int(self.computer_science) > 100:
                    print("Marks should be between 0 and 100.")
                else:
                    self.computer_science=int(self.computer_science)
                    break

        while True:
            self.english=input("enter your English Marks : ").strip()
            if not self.english.isdigit():
                print("Enter numbers only.")
            elif self.english.isdigit():
                if int(self.english) < 0 or int(self.english) > 100:
                    print("Marks should be between 0 and 100.")
                else:
                    self.english=int(self.english)
                    break

        while True:
            self.hr_ethics=input("enter your HumanResource&ethics Marks : ").strip()
            if not self.hr_ethics.isdigit():
                print("Enter numbers only.")
            elif self.hr_ethics.isdigit():
                if int(self.hr_ethics) < 0 or int(self.hr_ethics) > 100:
                    print("Marks should be between 0 and 100.")
                else:
                    self.hr_ethics=int(self.hr_ethics)
                    break


        query="""
        insert into student_details (student_name,maths,statistics,computer_science,english,hr_ethics)
        values(%s, %s, %s, %s, %s, %s)
        """
        values=(self.name,self.maths,self.statics,self.computer_science,self.english,self.hr_ethics)
        self.cusor.execute(query,values)
        self.connect.commit()

        student_id = self.cusor.lastrowid

        print("=== STUDENT DETAILS ADDED SUCCESSFULLY ===")
        print("YOUR Student ID Number is :", student_id)
        
		


    def view_details(self):
        query = """
        SELECT * FROM student_details
        """
        self.cusor.execute(query)
        data = self.cusor.fetchall()
        if not data:
            print("Data Not Found")
            return
        for student in data:
            print("Student ID       :", student[0])
            print("Student Name     :", student[1])
            print("Maths            :", student[2])
            print("Statistics       :", student[3])
            print("Computer Science :", student[4])
            print("English          :", student[5])
            print("HR & Ethics      :", student[6])
            print("-" * 40)

    def search_student(self):
        while True:
            print("\n1. Search student by Student ID (2600000--) ")
            print("2. Search student by Student Name ")
            print("3. Exit")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                while True:
                    self.student_id = input("Enter Student Id Number: ").strip()
                    if self.student_id.isdigit():
                        break
                    print("Invalid Student ID(2600000--). Please enter numbers only.")
                query = """
                    SELECT * FROM student_details WHERE student_id = %s
                """
                self.cusor.execute(query, (self.student_id,))
                student = self.cusor.fetchone()
                if not student:
                    print("Data Not Found")
                    continue
                print("-" * 45)
                print("Student ID       :", student[0])
                print("Student Name     :", student[1])
                print("Maths            :", student[2])
                print("Statistics       :", student[3])
                print("Computer Science :", student[4])
                print("English          :", student[5])
                print("HR & Ethics      :", student[6])
                print("-" * 45)
            elif choice == "2":
                while True:
                    self.name = input("Enter Student Name: ").strip()
                    if self.name and self.name.replace(" ", "").isalpha():
                        break
                    print("Invalid name. Please enter alphabets only.")
                query = """
                    SELECT * FROM student_details WHERE student_name LIKE %s
                """
                self.cusor.execute(query, ("%" + self.name + "%",))
                students = self.cusor.fetchall()
                if not students:
                    print("Data Not Found")
                    continue
                for student in students:
                    print("=" * 45)
                    print("Student ID       :", student[0])
                    print("Student Name     :", student[1])
                    print("Maths            :", student[2])
                    print("Statistics       :", student[3])
                    print("Computer Science :", student[4])
                    print("English          :", student[5])
                    print("HR & Ethics      :", student[6])
                    print("=" * 45)
            elif choice == "3":
                print("Search exited.")
                break
            else:
                print("Invalid choice. Please choose 1, 2, or 3.")

    def update_student(self):

        def get_marks(subject):
            while True:
                marks = input(f"Enter {subject} Marks (0-100): ").strip()

                if marks.isdigit() and 0 <= int(marks) <= 100:
                    return marks

                print("Invalid marks. Please enter numbers between 0 and 100.")

        def confirm_update():
            while True:
                confirm = input("Do you want to update? (YES/NO): ").strip().upper()

                if confirm == "YES":
                    return True

                elif confirm == "NO":
                    return False

                else:
                    print("Invalid choice. Please enter YES or NO.")

        # Student ID validation
        while True:
            self.student_id = input("Enter Student Id Number: ").strip()

            if self.student_id and self.student_id.isdigit():
                break

            print("Invalid Student ID. Please enter numbers only.")

        # Check student exists
        query = """
            SELECT * FROM student_details
            WHERE student_id = %s
        """

        self.cusor.execute(query, (self.student_id,))
        student = self.cusor.fetchone()

        if not student:
            print("Data Not Found")
            return

        # Display student details
        print("=" * 45)
        print("Student ID       :", student[0])
        print("Student Name     :", student[1])
        print("Maths            :", student[2])
        print("Statistics       :", student[3])
        print("Computer Science :", student[4])
        print("English          :", student[5])
        print("HR & Ethics      :", student[6])
        print("=" * 45)

        # Update menu
        while True:

            print("\n1. Update Student Name")
            print("2. Update Maths Marks")
            print("3. Update Statistics Marks")
            print("4. Update Computer Science Marks")
            print("5. Update English Marks")
            print("6. Update HR & Ethics Marks")
            print("7. Update All Details")
            print("8. Exit")

            choice = input("Enter your choice: ").strip()

            # Update Student Name
            if choice == "1":

                while True:
                    name = input("Enter new Student Name: ").strip()

                    if name and name.replace(" ", "").isalpha():
                        break

                    print("Invalid name. Please enter alphabets only.")

                if confirm_update():

                    query = """
                        UPDATE student_details
                        SET student_name = %s
                        WHERE student_id = %s
                    """

                    self.cusor.execute(query, (name, self.student_id))
                    self.connect.commit()

                    print("Student Name updated successfully.")

                else:
                    print("Update cancelled.")

            # Update Maths Marks
            elif choice == "2":

                marks = get_marks("Maths")

                if confirm_update():

                    query = """
                        UPDATE student_details
                        SET maths = %s
                        WHERE student_id = %s
                    """

                    self.cusor.execute(query, (marks, self.student_id))
                    self.connect.commit()

                    print("Maths marks updated successfully.")

                else:
                    print("Update cancelled.")

            # Update Statistics Marks
            elif choice == "3":

                marks = get_marks("Statistics")

                if confirm_update():

                    query = """
                        UPDATE student_details
                        SET statistics = %s
                        WHERE student_id = %s
                    """

                    self.cusor.execute(query, (marks, self.student_id))
                    self.connect.commit()

                    print("Statistics marks updated successfully.")

                else:
                    print("Update cancelled.")

            # Update Computer Science Marks
            elif choice == "4":

                marks = get_marks("Computer Science")

                if confirm_update():

                    query = """
                        UPDATE student_details
                        SET computer_science = %s
                        WHERE student_id = %s
                    """

                    self.cusor.execute(query, (marks, self.student_id))
                    self.connect.commit()

                    print("Computer Science marks updated successfully.")

                else:
                    print("Update cancelled.")

            # Update English Marks
            elif choice == "5":

                marks = get_marks("English")

                if confirm_update():

                    query = """
                        UPDATE student_details
                        SET english = %s
                        WHERE student_id = %s
                    """

                    self.cusor.execute(query, (marks, self.student_id))
                    self.connect.commit()

                    print("English marks updated successfully.")

                else:
                    print("Update cancelled.")

            # Update HR & Ethics Marks
            elif choice == "6":

                marks = get_marks("HR & Ethics")

                if confirm_update():

                    query = """
                        UPDATE student_details
                        SET hr_ethics = %s
                        WHERE student_id = %s
                    """

                    self.cusor.execute(query, (marks, self.student_id))
                    self.connect.commit()

                    print("HR & Ethics marks updated successfully.")

                else:
                    print("Update cancelled.")

            # Update All Details
            elif choice == "7":

                while True:
                    name = input("Enter Student Name: ").strip()

                    if name and name.replace(" ", "").isalpha():
                        break

                    print("Invalid name. Please enter alphabets only.")

                maths = get_marks("Maths")
                statistics = get_marks("Statistics")
                computer_science = get_marks("Computer Science")
                english = get_marks("English")
                hr_ethics = get_marks("HR & Ethics")

                if confirm_update():

                    query = """
                        UPDATE student_details
                        SET student_name = %s,
                            maths = %s,
                            statistics = %s,
                            computer_science = %s,
                            english = %s,
                            hr_ethics = %s
                        WHERE student_id = %s
                    """

                    self.cusor.execute(
                        query,
                        (
                            name,
                            maths,
                            statistics,
                            computer_science,
                            english,
                            hr_ethics,
                            self.student_id
                        )
                    )

                    self.connect.commit()
                    print("All student details updated successfully.")
                else:
                    print("Update cancelled.")
            elif choice == "8":
                print("Update exited.")
                break
            else:
                print("Invalid choice. Please choose 1 to 8.")
    def delete_student(self):
        while True:
            self.student_id = input("Enter Student Id Number: ").strip()
            if self.student_id and self.student_id.isdigit():
                break
            print("Invalid number.(2600000--) Please enter numbers only.")
        query = """
            SELECT * FROM student_details
            WHERE student_id = %s
        """
        self.cusor.execute(query, (self.student_id,))
        student = self.cusor.fetchone()
        if not student:
            print("Data Not Found")
            return
        print("=" * 45)
        print("Student ID       :", student[0])
        print("Student Name     :", student[1])
        print("Maths            :", student[2])
        print("Statistics       :", student[3])
        print("Computer Science :", student[4])
        print("English          :", student[5])
        print("HR & Ethics      :", student[6])
        print("=" * 45)
        confirm = input("Enter confirmation to delete student details (YES/NO): ").strip().upper()
        if confirm not in ("YES", "NO"):
            print("Please enter correct answer.")
            return
        elif confirm == "NO":
            print("Delete operation cancelled.")
            return
        else:
            query = """
                DELETE FROM student_details WHERE student_id = %s
            """
            self.cusor.execute(query, (self.student_id,))
            self.connect.commit()
            print("Student details deleted successfully.")

    def total_marks(self):
        while True:
            self.student_id = input("Enter Student Id Number: ").strip()
            if self.student_id and self.student_id.isdigit():
                break
            print("Invalid number.(2600000--) Please enter numbers only.")
        query = """
            SELECT * FROM student_details where student_id =%s
            """
        self.cusor.execute(query, (self.student_id,))
        student = self.cusor.fetchone()
        if not student:
            print("Data Not Found")
            return
        sum_of_total_marks=student[2]+student[3]+student[4]+student[5]+student[6] 
        print("="*40)
        print(f"Maths              : {student[2]}\nStatistics         : {student[3]}\nComputer Science   : {student[4]}\nEnglish            : {student[5]}\nHR & Ethics        : {student[6]}")
        print("="*40)
        print(f"Total Marks      : {sum_of_total_marks} / 500")
        print("="*40)
        return sum_of_total_marks
    def calculate_percentage(self):
        total = self.total_marks() 
        if total is not None: 
            percentage = (total / 500) * 100 
            print("=" * 40) 
            print(f"Percentage : {percentage}%") 
            print("=" * 40)
    def grade_student(self):
        while True:
            self.student_id=input("enter student id :").strip()
            if self.student_id and self.student_id.isdigit(): 
                break
            print("Invalid number.(2600000--) Please enter numbers only.")
        query = """
        SELECT * FROM student_details where student_id =%s
        """
        self.cusor.execute(query, (self.student_id,))
        student = self.cusor.fetchone()
        if not student:
            print("Data Not Found")
            return
        total=student[2]+student[3]+student[4]+student[5]+student[6]
        percentage=(total/500)*100
        if percentage>=90:
            grade="A"
        elif percentage >= 80: 
            grade = "B" 
        elif percentage >= 70: 
            grade = "C" 
        elif percentage >= 60: 
            grade = "D" 
        elif percentage >= 50: 
            grade = "E" 
        else: 
            grade = "F" 
        print("=" * 40) 
        print("Student ID :", student[0]) 
        print("Student Name :", student[1]) 
        print("Total Marks :", total, "/ 500") 
        print("Percentage :", percentage, "%") 
        print("Grade :", grade) 
        print("=" * 40)

    def failed_pass_student(self):

        query = """
            SELECT student_id, student_name, maths, statistics,
                computer_science, english, hr_ethics
            FROM student_details
        """

        self.cusor.execute(query)
        students = self.cusor.fetchall()

        if not students:
            print("Data Not Found")
            return

        total_students = len(students)
        qualified_count = 0
        failed_count = 0

        print("=" * 50)
        print("          QUALIFIED STUDENTS")
        print("=" * 50)

        for student in students:

            if (student[2] >= 35 and
                student[3] >= 35 and
                student[4] >= 35 and
                student[5] >= 35 and
                student[6] >= 35):

                qualified_count += 1

                print("Student ID   :", student[0])
                print("Student Name :", student[1])
                print("-" * 50)

        print("=" * 50)
        print("             FAILED STUDENTS")
        print("=" * 50)

        for student in students:

            if (student[2] < 35 or
                student[3] < 35 or
                student[4] < 35 or
                student[5] < 35 or
                student[6] < 35):

                failed_count += 1

                print("Student ID   :", student[0])
                print("Student Name :", student[1])
                print("-" * 50)

        qualified_percentage = (qualified_count / total_students) * 100
        failed_percentage = (failed_count / total_students) * 100

        print("=" * 50)
        print("                RESULT")
        print("=" * 50)
        print("Total Students       :", total_students)
        print("Qualified Students   :", qualified_count)
        print("Failed Students      :", failed_count)
        print("Qualified Percentage :", qualified_percentage, "%")
        print("Failed Percentage    :", failed_percentage, "%")
        print("=" * 50)

    def display_topper(self):

        query = """
            SELECT student_id, student_name, maths, statistics,
                computer_science, english, hr_ethics,
                (maths + statistics + computer_science + english + hr_ethics) AS total
            FROM student_details
            ORDER BY total DESC
            LIMIT 1
        """

        self.cusor.execute(query)
        topper = self.cusor.fetchone()

        if not topper:
            print("Data Not Found")
            return

        print("=" * 50)
        print("                 TOPPER")
        print("=" * 50)

        print("Student ID       :", topper[0])
        print("Student Name     :", topper[1])
        print("Maths            :", topper[2])
        print("Statistics       :", topper[3])
        print("Computer Science :", topper[4])
        print("English          :", topper[5])
        print("HR & Ethics      :", topper[6])
        print("Total Marks      :", topper[7], "/ 500")

        percentage = (topper[7] / 500) * 100
        print("Percentage       :", percentage, "%")

        print("=" * 50)



def console_menu():
    st=student_details()
    while True:
        print("====WELCOME TO STUDENT MANAGEMENT SYSTEM  =====")
        print("\n 1. Add Student\n 2. View Students\n 3. Search Student\n 4. Update Student\n 5. Delete Student\n 6. Calculate Total Marks\n 7. Calculate Percentage\n 8. Generate Grade\n 9. Display Topper\n 10. Failed & Qualified Students\n 11. Exit\n")
        opt=int(input("ENTER YOUR CHOICES FOR GIVEN DATA: ").strip())
        if opt==1:
            st.add_student()
        elif opt==2:
            st.view_details()
        elif opt==3:
            st.search_student()
        elif opt==4:
            st.update_student()
        elif opt==5:
            st.delete_student()
        elif opt==6:
            st.total_marks()
        elif opt==7:
            st.calculate_percentage()
        elif opt==8:
            st.grade_student()
        elif opt==9:
            st.display_topper()
        elif opt==10:
            st.failed_pass_student()
        elif opt==11:
            print("==THANKYOU==")
            break
        else:
            print("===PLEASE CHOOSE CORRECT CHOICE FOR GIVEN OPTION===")
        







            
