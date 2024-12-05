from faker import Faker
import csv
import random

fakeData = Faker()

# generating staff data
with open("adminStaff.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["staffID", "name", "staffEmail", "staffDepartment"])

    for staff_id in range(101, 122):
        writer.writerow([staff_id, fakeData.name(), fakeData.email(), fakeData.job()])

# generating student data
with open("student.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["studentID", "name", "studentEmail", "studentDOB", "staffID"])

    for stu_id in range(1001, 1022):
        writer.writerow([stu_id, fakeData.name(), fakeData.email(), fakeData.date_of_birth(minimum_age=13, maximum_age=18), random.randint(101, 121)])

# generating courses data
with open("courses.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["courseID", "name"])
    courses = ["Data Engineering", "Computer Networks", "AI", "Cyber Security", "Advance Programming", "Project Management", "Mathematics"]

    for cours_id, course_name in enumerate(courses, 1):
        writer.writerow([cours_id, course_name])

# generating lecturer data
with open("lecture.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["lecturerD", "name", "lecturerEmail", "courseID"])

    for lec_id in range(2001, 2022):
        writer.writerow([lec_id, fakeData.name(), fakeData.email(), random.randint(1, 7)])

# Generate Enrollment data
with open("enrollment.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["courseID", "studentID", "enrollmentDate"])
    for _ in range(1, 22):  # Generate 30 enrollments
        writer.writerow([random.randint(1, 7), random.randint(1001, 1021), fakeData.date()])  # Random courseID and studentID

# generating phoneNumber data
with open("phonenumber.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["lecturerID", "phoneNumber"])
    for _ in range(1, 22):
        writer.writerow([random.randint(2001, 2021), fakeData.phone_number()])
    