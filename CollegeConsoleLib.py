import datetime
from enum import Enum
import pickle # for serialization


class Semester(Enum):
    FALL = 0
    WINTER = 1
    SUMMER = 2

class EvaluationType(Enum):
    TEST = 0
    QUIZ = 1
    ASSIGNMENT = 2
    LAB = 3

class FinalGrade(Enum):
    APLUS = 0
    A = 1
    BPLUS = 2
    B = 3
    CPLUS = 4
    C = 5
    DPLUS = 6
    D = 7
    F = 8

class CourseManager(object):
    __courses = []

    @property
    def courses(self):
        return self.__courses

    def add_course(self, course):
        self.courses.append(course)

    def export_courses(self, filename, delimiter):
        f_out = open(filename, 'w')
        record_format = delimiter.join(["{0}", "{1}", "{2}", "{3}\n"])
        for crse in self.courses:
            f_out.write(record_format.format(
                crse.coursecode,
                crse.name,
                crse.description,
                crse.eval_count,
            )
            )
        f_out.close()

    def import_courses(self, filename, delimiter):
        f_in = open(filename, 'r')
        processed = 0
        imported = 0
        for record in f_in:
            fields = record.split(delimiter)
            processed += 1
            try:
                if len(fields) != 4:
                    raise ValueError(
                        "Invalid number of fields in record {0}".format(processed))
                elif not self.is_int(fields[3]):
                    raise TypeError(
                        "Number of evaluations in record {0} is not in correct format".format(processed))
                elif self.is_coursecode_inuse(fields[0]):
                    raise ValueError(
                        "Course code in record {0} is in use".format(processed))
                else:
                    crse = Course()
                    crse.coursecode = fields[0]
                    crse.name = fields[1]
                    crse.description = fields[2]
                    crse.eval_count = int(fields[3])
                    self.courses.append(crse)
                    imported += 1
            except Exception as e:
                print(e)

        print("{0} records processed, {1} courses added".format(
            processed, imported))
        f_in.close()

    def save_schoolinfo(self):
        with open("user.dat", 'wb') as f:
            pickle.dump(self, f)

    def load_school(self, filename):
        crse_mng = CourseManager()
        with open(filename, 'rb') as f:
            crse_mng = pickle.load(f)
        self.__courses = crse_mng.courses

    def is_int(self, s):
        try:
            int(s)
        except:
            return False
        return True

    def is_coursecode_inuse(self, code):
        for crse in self.courses:
            if crse.coursecode == code:
                return True
        return False


class Course(object):

    def __init__(self, **kwarg):
        self.__coursecode = ""
        self.__name = ""
        self.__description = ""
        self.__sections = [None] * 20
        self.__section_count = 0
        self.__eval_count = 0
        has_both_args = True
        for arg in ('coursecode', 'name'):
            has_both_args &= (arg in kwarg)
        if has_both_args:
            self.__coursecode = kwarg['coursecode']
            self.__name = kwarg['name']

    @property
    def coursecode(self):
        return self.__coursecode

    @coursecode.setter
    def coursecode(self, v):
        self.__coursecode = v

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, v):
        self.__name = v

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, v):
        self.__description = v

    @property
    def sections(self):
        return self.__sections

    @sections.setter
    def sections(self, v):
        self.__sections = v

    @property
    def section_count(self):
        return self.__section_count

    @section_count.setter
    def section_count(self, v):
        self.__section_count = v

    @property
    def eval_count(self):
        return self.__eval_count

    @eval_count.setter
    def eval_count(self, v):
        if self.__sections[0] is None:
            self.__eval_count = v
        else:
            raise ValueError(
                "Section is already assigned. Number of evaluations cannot be changed any more")

    def add_section(self, **kwargs):
        if 'section' in kwargs:
            if kwargs['section'].sectionid == "" or kwargs['section'].name == "":
                raise ValueError("Section is not valid")
            else:
                if kwargs['section'].course is None:
                    self.__sections[self.section_count] = kwargs['section']
                    self.__section_count += 1
                    kwargs['section'].course = self
                else:
                    raise ValueError("Section already assigned to {0} course".format(
                        kwargs['section'].course.name))
        else:
            has_three_args = True
            for arg in ('semester', 'id', 'name'):
                has_three_args &= (arg in kwargs)
            if has_three_args:
                section = Section(self, 30, kwargs['semester'])
                section.sectionid = kwargs['id']
                section.name = kwargs['name']
                self.__sections[self.section_count] = section
                self.section_count += 1

    def get_info(self):
        result = ""
        result += "CourseCode: {0}, ".format(self.coursecode)
        result += "Name: {0}, ".format(self.name)
        result += "Description: {0}, ".format(self.description)
        result += "No of Evaluations: {0} \n".format(self.eval_count)
        result += "No of sections: {0}".format(self.section_count)
        for i in range(self.section_count):
            result += "\n\t {0}:{1}".format(
                self.sections[i].course.name, self.sections[i].name)
        return result


class Person(object):

    __regno_generator = 0
    __regnumbers = []

    def __init__(self, **kwargs):
        self.__regnumber = 0
        self.__name = ""
        self.__dob = None
        self.__address = ()
        self.__tel = ""
        has_both_args = True
        for arg in ('name', 'dob'):
            has_both_args &= (arg in kwargs)
        if has_both_args:
            self.__name, self.__dob = kwargs['name'], kwargs['dob']
        Person.__regno_generator += 1
        self.__regnumber = Person.__regno_generator

    def __str__(self):
        return self.__name

    @property
    def regnumber(self):
        return self.__regnumber

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, v):
        self.__name = v

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, v):
        self.__address = v

    @property
    def dob(self):
        return self.__dob

    @dob.setter
    def dob(self, value):
        self.__dob = value

    @property
    def tel(self):
        return self.__tel

    @tel.setter
    def tel(self, v):
        self.__tel = self._is_valid_number(v)

    def get_info(self):
        result = ""
        result += "Reg no: {0}, ".format(self.regnumber)
        result += "Name: {0}, ".format(self.name)
        result += "DOB: {0}, ".format(self.dob.strftime("%Y-%m-%d"))
        result += "\nAddress: Street: {0}, City: {1}, State: {2}, ".format(
            self.address[0], self.address[1], self.address[2])
        result += "Tel:{0}".format(self.tel)
        return result

    def _is_valid_number(self, tel):
        if tel:
            return tel
        else:
            raise ValueError(
                "Telephone number must be 10-digits({0})".format(tel))

    def _validate_uniqueness(self, regno):
        if regno in Person.__regnumbers:
            raise ValueError(
                "Registration number must be unique({0})".format(regno))
        else:
            if (self.__regnumber in Person.__regnumbers):
                del Person.__regnumbers[self.__regnumber]
            Person.__regnumbers[regno] = 1
            return regno


class Section (object):

    def __init__(self, **kwargs):
        self.__sectionid = ""
        self.__name = ""
        self.__course = None
        self.__semester = None
        self.__faculty = None
        self.__max_enrolment_count = 40
        self.__enrolments = None
        self.__enrolment_counter = 0

        has_args = True
        for arg in ("course", "max_enrolment_count", "semester"):
            has_args &= (arg in kwargs)
        if has_args:
            self.__course, self.__semester = kwargs["course"], kwargs["semester"]
            if 'max_enrolment_count' in kwargs:
                self.__max_enrolment_count = kwargs['max_enrolment_count']
                self.__enrolments = [None] * self.__max_enrolment_count

    @property
    def sectionid(self):
        return self.__sectionid

    @sectionid.setter
    def sectionid(self, v):
        self.__sectionid = v

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, v):
        self.__name = v

    @property
    def max_student_count(self):
        return self.__max_enrolment_count

    @max_student_count.setter
    def max_student_count(self, v):
        if self.__enrolments is None:
            self.__max_enrolment_count = v
            self.__enrolments = [None] * v

    @property
    def enrolments(self):
        return self.__enrolments

    @property
    def enrolment_counter(self):
        return self.__enrolment_counter

    @property
    def course(self):
        return self.__course

    @course.setter
    def course(self, v):
        self.__course = v

    @property
    def semester(self):
        return self.__semester

    @semester.setter
    def semester(self, v):
        self.__semester = v

    @property
    def faculty(self):
        return self.__faculty if self.__faculty is not None else ""

    @faculty.setter
    def faculty(self, v):
        self.__faculty = v

    def add_student(self, student):
        if self.course is None:
            raise ValueError(
                "Student can only be assigned to the section that is assigned to the course")
        if self.enrolment_counter >= self.__max_enrolment_count:
            raise ValueError("Student cannot be added. The section is full")
        self.enrolments[self.__enrolment_counter] = Enrolment(
            student, self, self.course.eval_count)
        self.__enrolment_counter += 1

    def define_evaluation(self, orderno, evaltype, maxpts, weight):
        for enrl in self.enrolments:
            if enrl is not None:
                enrl.evaluations[orderno -
                                 1] = Evaluation(evaltype, maxpts, weight)

    def add_studentmark(self, orderno, student, pts):
        for enrl in self.enrolments:
            if enrl:
                if pts > enrl.evaluations[orderno - 1].max_points:
                    raise ValueError(
                        "Points are more than the max number of points for the evaluation")
                if enrl.student is student:
                    enrl.evaluations[orderno - 1].points = pts
                    return
        raise ValueError(
            "Student {0} is not in the section".format(student.name))

    def finalmarkinfo(self):
        result = ""
        if self.enrolments is None:
            return result
        for enrl in self.enrolments:
            if enrl:
                enrl.calculate_finalgrade()
                result += "{0}\t{1}\n".format(enrl.student.name,
                                              enrl.finalgrade.name)
        return result

    def get_evalinfo(self):
        result = ""
        if (self.enrolments is None):
            return "No enrollments in the section"
        for i, ev in enumerate(self.enrolments[0].evaluations):
            if(ev.evaltype is None):
                return result

            result += "\t{0}.{1}[{2}]".format(
                i,
                ev.evaltype.name,
                ev.max_points
            )

        result += "\n"
        for i in range(self.__enrolment_counter):
            result += "{0}\t".format(self.enrolments[i].student.name)
            for ev in self.enrolments[i].evaluations:
                if(ev.max_points == 0):
                    result += "{0}/{1}\t\t".format(0,
                                                   "NaN")
                else:
                    pts_weighted = ev.points / ev.max_points * 100 * ev.evalweight
                    if (pts_weighted - int(pts_weighted) == 0):
                        pts_weighted = int(pts_weighted)
                    result += "{0}/{1}\t\t".format(ev.points,
                                                   pts_weighted)
            result += "\n"

        return result

    def get_info(self):
        result = ""
        result += "Section id: {0}, ".format(self.sectionid)
        result += "Name; {0}, ".format(self.name)
        result += "Max no of students: {0}, ".format(
            self.max_student_count)
        result += "Semester: {0}, \n".format(self.semester.name)
        result += "\tFaculty: {0}\n".format(self.faculty)
        result += "Number of students: {0}".format(self.enrolment_counter)
        for i in range(self.enrolment_counter):
            result += "\n\t {0}".format(self.enrolments[i].student.name)

        return result


class Enrolment(object):
    def __init__(self, student, section, evalnumber):
        self.__student = student
        self.__section = section
        self.__finalgrade = FinalGrade.F
        self.__evaluation_number = evalnumber
        self.__evaluations = [Evaluation()] * self.__evaluation_number

    @property
    def student(self):
        return self.__student

    @student.setter
    def student(self, v):
        self.__student = v

    @property
    def section(self):
        return self.__section

    @section.setter
    def section(self, v):
        self.__section = v

    @property
    def finalgrade(self):
        return self.__finalgrade

    @finalgrade.setter
    def finalgrade(self, v):
        self.__finalgrade = v

    @property
    def evaluations(self):
        return self.__evaluations

    def calculate_finalgrade(self):
        total_weighted_val = 0
        for ev in self.evaluations:
            if ev.max_points != 0:
                total_weighted_val += ev.points / ev.max_points * 100 * ev.evalweight
        percent = int(
            total_weighted_val) if self.__evaluations[0].max_points != 0 else 100
        if percent >= 90:
            grade = FinalGrade.APLUS
        elif percent >= 80:
            grade = FinalGrade.A
        elif percent >= 75:
            grade = FinalGrade.BPLUS
        elif percent >= 70:
            grade = FinalGrade.B
        elif percent >= 65:
            grade = FinalGrade.CPLUS
        elif percent >= 60:
            grade = FinalGrade.C
        elif percent >= 55:
            grade = FinalGrade.DPLUS
        elif percent >= 50:
            grade = FinalGrade.D
        else:
            grade = FinalGrade.F
        self.finalgrade = grade

    def get_info(self):
        result = ""
        result += "Section : {0}\n".format(self.section)
        result += "Student : {0}\n".format(self.student)
        result += "Final Grade : {0}\n".format(self.finalgrade)
        return result


class Evaluation(object):
    def __init__(self, type=EvaluationType.TEST, max=0, weight=0):
        self.__evaltype = type
        self.__max_points = max
        self.__evalweight = weight
        self.__points = 0

    @property
    def evaltype(self):
        return self.__evaltype

    @evaltype.setter
    def evaltype(self, v):
        self.__evaltype = v

    @property
    def evalweight(self):
        return self.__evalweight

    @evalweight.setter
    def evalweight(self, v):
        self.__evalweight = v

    @property
    def max_points(self):
        return self.__max_points

    @max_points.setter
    def max_points(self, v):
        self.__max_points = v

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, v):
        self.__points = v

    def get_info(self):
        result = ""
        result += "Type of Evaluation: {0},".format(self.evaltype.name)
        result += "Evaluation Weight: {0}, ".format(self.evalweight)
        result += "Max Points: {0}, ".format(self.max_points)
        result += "Points: {0}".format(self.points)
        return result
