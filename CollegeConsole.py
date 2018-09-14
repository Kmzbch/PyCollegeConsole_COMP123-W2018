from CollegeConsoleLib import *

def new_blockmessage(message):
    print(
        "\n---------------{0}-------------".format(message))

if __name__ == '__main__':

    course_mng = CourseManager()

    new_blockmessage("Creating course Prog1")
    prog1 = Course()
    print(prog1.get_info())
    print()

    new_blockmessage("Setting the values for Prog1")
    prog1.coursecode = "COMP100"
    prog1.name = "Programming 1"
    prog1.description = "Programming1 description"
    prog1.eval_count = 3
    print(prog1.get_info())

    new_blockmessage("Creating course Prog2")
    prog2 = Course(coursecode="COMP123", name="Programming2")
    prog2.description = "prog 2 desc"
    prog2.eval_count = 2
    print(prog2.get_info())

    new_blockmessage("Creating course manager and export courses")
    course_mng.add_course(prog1)
    course_mng.add_course(prog2)

    try:
        course_mng.export_courses("ExportCourses.txt", "|")
    except Exception as e:
        print(e)

    new_blockmessage("Creating person Student1")
    student1 = Person()
    student1.name = "Bob"
    student1.dob = datetime.date(1990, 1, 1)
    student1.address = ("35 Elm St", "Toronto", "ON")
    student1.tel = 4161111111
    print(student1.get_info())

    new_blockmessage("Creating another person Student2")
    student2 = Person()
    student2.name = "John"
    student2.dob = datetime.date(1991, 12, 31)
    student2.address = ("35 Ontario St", "Toronto", "ON")
    student2.tel = 4162222222
    print(student2.get_info())

    new_blockmessage("Creating another person Student3")
    student3 = Person()
    student3.name = "Ann"
    student3.dob = datetime.date(1993, 3, 3)
    student3.address = ("3 Queen St", "Toronto", "ON")
    student3.tel = 4163333333
    print(student3.get_info())

    new_blockmessage("Creating another person Student4")
    student4 = Person()
    student4.name = "Wes"
    student4.dob = datetime.date(1994, 4, 4)
    student4.address = ("44 Bayview St", "Toronto", "ON")
    student4.tel = 4164444444
    print(student4.get_info())

    new_blockmessage("Creating person Faculty")
    aFaculty = Person(name="Ann", dob=datetime.date(1960, 1, 1))
    aFaculty.address = ("1 King St W", "Toronto", "ON")
    aFaculty.tel = 4167654321
    print(aFaculty.get_info())

    new_blockmessage("Creating section Section 1")
    aSec1 = Section()
    aSec1.sectionid = "F01"
    aSec1.name = "Section 1"
    aSec1.semester = Semester.FALL
    aSec1.faculty = aFaculty
    print(aSec1.get_info())

    new_blockmessage("Creating section Section 2")
    aSec2 = Section(course=prog1, max_enrolment_count=50,
                    semester=Semester.WINTER)
    aSec2.sectionid = "W02"
    aSec2.name = "Section 2"
    aSec2.faculty = aFaculty
    print(aSec2.get_info())

    new_blockmessage("Adding Sections")
    new_blockmessage("Adding invalid section (Section 3) to course prog1")
    aSec3 = Section()
    try:
        prog1.add_section(section=aSec3)
    except Exception as e:
        print(e)
    print(prog1.get_info())

    new_blockmessage("Adding valid section to course prog1")
    aSec3.name = "Section 3"
    aSec3.sectionid = "F03"
    aSec3.max_student_count = 10
    aSec3.semester = Semester.FALL

    try:
        prog1.add_section(section=aSec3)
    except Exception as e:
        print(e)
    print(prog1.get_info())

    new_blockmessage(
        "Trying to change number of evaluations for the course that already has sescion assigned")
    try:
        prog1.eval_count = 4
    except Exception as e:
        print(e)

    new_blockmessage(
        "Trying to change number of evaluations for the course that does not have sescion assigned")
    try:
        prog2.eval_count = 10
    except Exception as e:
        print(e)
    print(prog2.get_info())

    new_blockmessage("Adding valid section already assigned to course prog2")
    try:
        prog2.add_section(section=aSec3)
    except Exception as e:
        print(e)
    print(prog2.get_info())

    new_blockmessage(
        "Trying to change number of evaluations for the course that already has section assigned")
    try:
        prog2.add_section(section=aSec1)
    except Exception as e:
        print(e)
    print(prog1.get_info())

    new_blockmessage("Adding Students")

    new_blockmessage(
        "Creating new section Section 4 with max number of students 1")
    aSec4 = Section()
    aSec4.sectionid = "F04"
    aSec4.name = "Section 4"
    aSec4.max_student_count = 1
    aSec4.semester = Semester.FALL
    aSec4.faculty = aFaculty
    print(aSec4.get_info())

    new_blockmessage(
        "Adding Student to Section 4. Section is not added to a course")
    try:
        aSec4.add_student(student1)
    except Exception as e:
        print(e)
    print(aSec4.get_info())

    new_blockmessage("Adding section 4 to a course prog 1")
    try:
        prog1.add_section(section=aSec4)
    except Exception as e:
        print(e)
    print(prog1.get_info())

    new_blockmessage(
        "Adding Student1 to Section 4. Section is added to a course")
    try:
        aSec4.add_student(student1)
    except Exception as e:
        print(e)
    print(aSec4.get_info())

    new_blockmessage("Adding Student2 to Section 4. Section is full")
    try:
        aSec4.add_student(student2)
    except Exception as e:
        print(e)
    print(aSec4.get_info())

    new_blockmessage("Adding three students to Section 3. ")
    try:
        aSec3.add_student(student2)
        aSec3.add_student(student3)
        aSec3.add_student(student4)
    except Exception as e:
        print(e)
    print(aSec3.get_info())

    new_blockmessage("Defining evaluations for Section 3. ")
    aSec3.define_evaluation(1, EvaluationType.TEST, 100, 0.5)
    aSec3.define_evaluation(2, EvaluationType.LAB, 80, 0.3)
    aSec3.define_evaluation(3, EvaluationType.QUIZ, 20, 0.2)

    print(aSec3.get_evalinfo())

    new_blockmessage("Adding marks for the evaluations to Section 3. ")
    new_blockmessage("Adding mark for a student not enrolled in the section.")
    try:
        aSec3.add_studentmark(1, student1, 90)
    except Exception as e:
        print(e)

    new_blockmessage(
        "Adding mark for a student higher than max points for the evaluation.")
    try:
        aSec3.add_studentmark(2, student2, 90)
    except Exception as e:
        print(e)

    new_blockmessage("Adding marks for students ")
    try:
        aSec3.add_studentmark(1, student2, 90)
        aSec3.add_studentmark(1, student3, 40)
        aSec3.add_studentmark(1, student4, 100)
        aSec3.add_studentmark(2, student2, 70)
        aSec3.add_studentmark(2, student4, 80)
        aSec3.add_studentmark(3, student2, 15)
        aSec3.add_studentmark(3, student3, 16)
        aSec3.add_studentmark(3, student4, 20)
    except Exception as e:
        print(e)

    print(aSec3.get_evalinfo())

    new_blockmessage("Calculate final marks")
    print(aSec3.finalmarkinfo())
    print()

    new_blockmessage("Saving the school info")
    try:
        course_mng.save_schoolinfo()
    except Exception as e:
        print(e)

    new_blockmessage("Loading the school info")
    new_course_mng = CourseManager()
    try:
        new_course_mng.load_school("user.dat")
    except Exception as e:
        print(e)

    new_blockmessage("Display loaded courses")
    a_course = Course()
    a_section = Section()
    for crse in new_course_mng.courses:
        a_course = crse
        print(crse.get_info())
        print("Course section with students")
        for sec in a_course.sections:
            if sec is None:
                break
            a_section = sec
            print(a_section.get_info())
            print()
            print("...And Marks:")
            print(a_section.get_evalinfo())
            print("...And Final Marks:")
            print(a_section.finalmarkinfo())
        print()

    new_blockmessage("Importing additional courses")
    try:
        new_course_mng.import_courses("AdditionalCourses.txt", ",")
    except Exception as e:
        print(e)

    for crse in new_course_mng.courses:
        a_course = crse
        print(crse.get_info())
