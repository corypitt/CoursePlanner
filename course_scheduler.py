import sys
from collections import namedtuple
import course_dictionary
import warnings; warnings.simplefilter('ignore')

def main(argv):
    #Creates a dictionary to use for testing
    test = course_dictionary.create_course_dict()
    #Creates an object course
    Course = namedtuple('Course', 'program, designation')
    #initializes a course(state) to be the end goal of the schedule
    goals = Course('CS', 'major')
    #print(test[Course('CS', 'major')])
    #initializes the initial state to no courses
    init_state = []
    schedule = []
    #course_dictionary.print_dict(test)
    #test_most_satisfied_mans(test)
    search(test, goals, init_state, schedule)
    goals = Course ('ECON', '3020')
    search(test, goals, init_state, schedule)
    print('Done')


def test_most_satisfied_mans(dictionary):
    Course = namedtuple('Course', 'program, designation')
    CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
    courseInfo = dictionary[Course('CS', '3259')]
    completed = [Course('MATH', '2400')]
    print(courseInfo.prereqs)
    print(mostSatisfied(courseInfo.prereqs, completed))


def search(dictionary, start, visited, schedule):
    endGoal = [start]
    while endGoal:
        course = endGoal.pop()
        if course not in visited:
            courseInfo = dictionary[course]
            #Checks if the course is a higher level
            if courseInfo.credits is '0':
                #runHighLevel
                #if credits = 0 and the largest prereq set = 1
                if (isOwnClass(courseInfo.prereqs)):
                    prereqs = findFirst(visited, courseInfo.prereqs)
                    if len(prereqs) is 0:
                        print (course, ' scheduled')
                        visited.append(course)
                    else:
                        for prereq in prereqs:
                            if prereq not in visited:
                                visited.append(course)
                                endGoal.append(prereq)
                else:
                    #if courseInfo.prereqs == 1
                    #if all are equal to one then the higher level essentially just a course
                    if preReqsComp(visited, courseInfo.prereqs):
                        print (course, ' scheduled')
                        visited.append(course)
                    else:
                        #add course to the stack of courses that need there prereqs completed
                        endGoal.append(course)
                        #find the most satisfied prereq set
                        prereqs = mostSatisfied(visited,courseInfo.prereqs)
                        #in the most satisfied set for each prereq not already
                        #in scheduled append to the to be scheduled stack
                        for prereq in prereqs:
                            if prereq not in schedule:
                                endGoal.append(prereq)

            else:
                #checks if the course is one with no prereqs
                if len(courseInfo.prereqs) is 0:
                    #print("Low")
                    print(course, ' scheduled')
                    visited.append(course)
                    #course has credits but no prereqs do SOMETHING
                else:
                    if preReqsComp(visited, courseInfo.prereqs):
                        #newl
                        print(course, ' scheduled')
                        visited.append(course)
                        #course has credits & prereqs but theyve been completed
                    else:
                        #add course to the stack of courses that need there prereqs completed
                        endGoal.append(course)
                        #find the most satisfied prereq set
                        prereqs = mostSatisfied(visited, courseInfo.prereqs)
                        #in the most satisfied set for each prereq not already
                        #in scheduled append to the to be scheduled stack
                        for prereq in prereqs:
                            if prereq not in schedule:
                                endGoal.append(prereq)


#Tests to see if the length of all prereqs are length 1 (and) and is a edge case class
def isOwnClass(prereqs):
    if all(len(ors) is 1 for ors in prereqs):
        return True
    return False

#incompleted
def scheduler(dictionary, init, goals):
    courses = [goals]
    semesters = [('Frosh', 'Fall'), ('Frosh', 'Spring'), ('Soph', 'Fall'),
                ('Soph', 'Spring'),('Junior', 'Fall'), ('Junior', 'Spring'),
                ('Senior', 'Fall'), ('Senior', 'Spring')]
    semDict = {semester:[0, []] for semester in semesters}

#if all of the conjunction terms have been visited than return that specific
#set of ands (in the form of 1 or) else return an empty list
def findPreReq(scheduled, prereqs):
    for ors in prereqs:
        if all (ands in scheduled for ands in ors):
            return ors
    return []

def findFirst(scheduled, prereqs):
    for ors in prereqs:
        for ands in ors:
            if ands not in scheduled:
                return ors
    return []

#checks to see if there is an or that has all prerequisites scheduled
def preReqsComp(scheduled, prereqs):
    for ors in prereqs:
        if all (ands in scheduled for ands in ors):
            return True
    return False

#counts how many prereqs have been satisfied in the current set
def count(scheduled, prereqs):
    count = 0
    for prereq in prereqs:
        if prereqs in scheduled:
            count += 1
    return count

#returns the prereq set that has the most satisfied prereqs
def mostSatisfied(completed, prereqs):
    goal = []
    maxSat = -1
    for ors in prereqs:
        cur = 0
        for ands in ors:
            if ands in completed:
                cur = cur + 1
        if cur > maxSat:
            maxSat = cur
            goal = ors
    return goal


if __name__ == "__main__":
    main(sys.argv)
