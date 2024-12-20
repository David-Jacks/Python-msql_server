# this is where our python server code will be at
import mysql.connector
import csv
import plotly.express as ploter

def connect_my_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password = "Login@mysql1"
    )

    return mydb


# creating my database
def create_db_tables(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS OstrichfillHighSchool")
    cursor.execute("USE OstrichfillHighSchool")

    # creating admin_staff table
    cursor.execute("CREATE TABLE IF NOT EXISTS AdminStaff (staffID INT, name VARCHAR(225), staffEmail VARCHAR(225), staffdepartment VARCHAR(225), PRIMARY KEY (staffID))")

    cursor.execute("CREATE TABLE IF NOT EXISTS Student (studentID INT, name VARCHAR(225), studentEmail VARCHAR(225), studentDOB DATE, staffID INT, PRIMARY KEY (studentID), FOREIGN KEY (staffID) REFERENCES AdminStaff(staffID))")

    # creating table for courses
    cursor.execute("CREATE TABLE IF NOT EXISTS Courses (courseID INT, name VARCHAR(225), PRIMARY KEY (courseID))")

    # creating lecturer table
    cursor.execute("CREATE TABLE IF NOT EXISTS Lecturer (lecturerID INT, name VARCHAR(225), lecturerEmail VARCHAR(225), courseID INT, PRIMARY KEY (lecturerID), FOREIGN KEY (courseID) REFERENCES Courses(courseID))")

    # enrollment 
    cursor.execute("CREATE TABLE IF NOT EXISTS Enrollment (courseID INT, studentID INT, enrollmentDate DATE, PRIMARY KEY (courseID, studentID), FOREIGN KEY (courseID) REFERENCES Courses(courseID), FOREIGN KEY (studentID) REFERENCES Student(studentID))")

    # creating a phone_lecturer table to ensure the db is in 3NF and the multivalued attribute is dealt with.
    cursor.execute("CREATE TABLE IF NOT EXISTS Phone_Lecturer (phoneID INT AUTO_INCREMENT, lecturerID INT, phoneNumber VARCHAR(225), PRIMARY KEY (phoneID), FOREIGN KEY (lecturerID) REFERENCES Lecturer(lecturerID))")

# making queries to store data into my tables
def pop_data_into_table(db, csv_file, table, cursor):
    with open(csv_file, "r") as file:
        read = csv.reader(file)
        next(read)

        if table == "Student":
            insertion_query = """
INSERT INTO Student (studentID, name, studentEmail, studentDOB, staffID) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE studentID = VALUES(studentID), name = VALUES(name), studentEmail = VALUES(studentEmail), studentDOB = VALUES(studentDOB), staffID = VALUES(staffID);
"""
        elif table == "Lecturer":
            insertion_query = """
INSERT INTO Lecturer (lecturerID, name, lecturerEmail, courseID) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE lecturerID = VALUES(lecturerID), name = VALUES(name), lecturerEmail = VALUES(lecturerEmail), courseID = VALUES(courseID);
"""
        elif table == "AdminStaff":
            insertion_query = """
INSERT INTO AdminStaff (staffID, name, staffEmail, staffDepartment) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE staffID = VALUES(staffID), name = VALUES(name), staffEmail = VALUES(staffEmail), staffDepartment = VALUES(staffDepartment);
"""
        elif table == "Courses":
            insertion_query = """
INSERT INTO Courses (courseID, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE courseID = VALUES(courseID), name = VALUES(name);
"""
        elif table == "Enrollment":
            insertion_query = """
INSERT INTO Enrollment (courseID, studentID, enrollmentDate) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE courseID = VALUES(courseID), studentID = VALUES(studentID), enrollmentDate = VALUES(enrollmentDate);
"""
        elif table == "Phone_Lecturer":
            insertion_query = """
INSERT INTO Phone_Lecturer (lecturerID, phoneNumber) VALUES (%s, %s) ON DUPLICATE KEY UPDATE lecturerID = VALUES(lecturerID), phoneNumber = VALUES(phoneNumber);
"""
        else:
            print("Table does not exist")

        # perfom the insertion using the insertion query
        for entity in read:
            cursor.execute(insertion_query, entity)

        # commit the changes after the populating
        db.commit()

# writting Queries to extract and print to the user using the python plotly library
def print_queries(query, cursor):
    data = {}
    for my_query in query:
        print("printing query......")
        print()
        # unpacking
        title, req_query, tablehead = my_query

        cursor.execute(req_query)
        query_res = cursor.fetchall()

        
        col, row = tablehead
        # using list comprehension to seperate the query response into col and row data
        data[col] = [x[0] for x in query_res]
        data[row] = [x[1] for x in query_res]
    
     
        # printing a bar chart using plotly library
        chart = ploter.bar(data, x = col, y = row, title=title, labels = {col:col, row:row})

        chart.show()
        # setting the dictionary data back to empty in order to avoid duplication in the values associated to the keys
        data = {}
        

# this will be my main function
def main():
    # connect to my db
    my_db_connection = connect_my_db()
    if my_db_connection:
        try:
            print("connection to MySQL is successfull!!")
            # creating my cursor to use in managing communication to my database
            my_control = my_db_connection.cursor()

            # Create database and associated tables
            create_db_tables(my_control)

            # populate my tables
            pop_data_into_table(my_db_connection, "adminStaff.csv", "AdminStaff", my_control)
            pop_data_into_table(my_db_connection, "student.csv", "Student", my_control)
            pop_data_into_table(my_db_connection, "courses.csv", "Courses", my_control)
            pop_data_into_table(my_db_connection, "lecture.csv", "Lecturer", my_control)
            pop_data_into_table(my_db_connection, "enrollment.csv", "Enrollment", my_control)
            pop_data_into_table(my_db_connection, "phonenumber.csv", "Phone_Lecturer", my_control)

            # making queries
            # printing courses and the number of students that are enrolled in them
            tablehead1 = ("name","no_student")
            title1 = "All courses currently available at Ostrichfill and the number of students enrolled"
            query1 = """
            SELECT c.name, COUNT(e.studentID) AS  no_student FROM Enrollment e JOIN Courses c ON c.courseID = e.courseID GROUP BY c.name ORDER BY no_student;
            """
            # printing all Admin staff and the number of students they monitor.
            tablehead2 = ("name","no_student")
            title2 = "Admin staff and the number of students they monitor"
            query2 = """
            SELECT a.name, COUNT(s.studentID) as no_student FROM AdminStaff a LEFT JOIN Student s ON s.staffID = a.staffID GROUP BY a.name ORDER BY no_student DESC;
            """
            # printing Student and the number of courses they are doing
            tablehead3 = ("name","no_courses")
            title3 = "Student and the number of courses they are doing"
            query3 = """
            SELECT s.name, COUNT(e.courseID) AS no_courses FROM Student s LEFT JOIN Enrollment e ON e.studentID = s.studentID GROUP BY s.name ORDER BY no_courses;
            """
            # Printing Courses and the number of enlisted lecturers
            tablehead4 = ("name","no_lecturers")
            title4 = "Courses and the number of enlisted Lecturers"
            query4 = """
            SELECT c.name, COUNT(l.lecturerID) AS no_lecturers FROM Courses c JOIN Lecturer l ON l.courseID = c.courseID GROUP BY c.name ORDER BY no_lecturers; 
            """
            # Get all the lectures that teaches Cyber Security
            tablehead5 = ("name","lecturerID")
            title5 = "Lectures that teaches Cyber Security"
            query5 = """
            SELECT l.name, l.lecturerID FROM Lecturer l JOIN Courses c ON c.courseID = l.courseID WHERE c.name = "Cyber Security";
            """
            # making five queires
            # would have gone ahead to apply open close software priciple in my code, but 5 is okay for computation
            query_data = [(title1, query1, tablehead1), (title2, query2, tablehead2), (title3, query3, tablehead3),(title4, query4, tablehead4),(title5, query5, tablehead5)]

            # run queries on my tables and print them
            print_queries(query_data, my_control)

        finally:
            my_control.close()
            my_db_connection.close()
            print("MySQL connection ended!!")
    else:
        print("Cennection to MySQL failed")
        

# running my main function
if __name__ == "__main__":
    main()