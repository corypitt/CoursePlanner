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
    #'CS', 'major'
    goals = [Course('CS', 'major')]
    semesters = [('Frosh', 'Fall'), ('Frosh', 'Spring'), ('Soph', 'Fall'),
                ('Soph', 'Spring'),('Junior', 'Fall'), ('Junior', 'Spring'),
                ('Senior', 'Fall'), ('Senior', 'Spring')]
    semDict = {semester:[0, []] for semester in semesters}
    print(test[Course('CS', 'major')])
    #initializes the initial state to no courses
    #use form [('MATH', '2810'),xxx
    init_state = [('CS', '1101')]
    schedule = []
    #course_dictionary.print_dict(test)

    search(semesters, semDict, test, goals, init_state, schedule)
    print('Done')

def search(semesters, semDict, dictionary, start, visited, schedule):
    endGoal = start
    while endGoal:
        course = endGoal.pop()
        if course not in visited:
            courseInfo = dictionary[course]
            if courseInfo.credits is '0':
                """
                Higher level
                """
                if (isOwnClass(courseInfo.prereqs)):
                    prereqs = findFirst(visited, courseInfo.prereqs)
                    #Case 1 higher level Prereqs are all met
                    if len(prereqs) is 0:
                        visited.append(course)
                        #scheduler(semesters, semDict, dictionary, course, courseInfo, [])
                    #Case 2 higher level prereqs are not all met
                    else:
                        #this will result in result errors in certain cases
                        #come back to
                        for prereq in prereqs:
                            if prereq not in visited:
                                visited.append(course)
                                prereqA = findPreReq(visited, courseInfo.prereqs)
                                #scheduler(semesters, semDict, dictionary, course, courseInfo, prereqA)
                                endGoal.append(prereq)
                else:
                    #Case 3 Higher level prereqs are completed
                    if preReqsComp(visited, courseInfo.prereqs):
                        prereqsscheduled = findPreReq(visited, courseInfo.prereqs)
                        visited.append(course)
                        #scheduler(semesters, semDict, dictionary, course, courseInfo, prereqsscheduled)
                    #Case 4 Higher level prereqs are not completed
                    else:
                        endGoal.append(course)
                        prereqs = mostSatisfied(visited,courseInfo.prereqs)
                        for prereq in prereqs:
                            if prereq not in visited:
                                endGoal.append(prereq)
            else:
                #Low level case 5 Course with no prereqs unmet
                if len(courseInfo.prereqs) is 0:
                    visited.append(course)
                    scheduler(semesters, semDict, dictionary, course, courseInfo,[])
                else:
                    if preReqsComp(visited, courseInfo.prereqs):
                        toAdd = findPreReq(visited, courseInfo.prereqs)
                        visited.append(course)
                        scheduler(semesters, semDict, dictionary, course, courseInfo, toAdd)
                    #Course with unmet prereqs add the course back to the todo stack
                    else:
                        endGoal.append(course)
                        prereqs = mostSatisfied(visited, courseInfo.prereqs)
                        for prereq in prereqs:
                            if prereq not in visited:
                                endGoal.append(prereq)

    ifEmpty(semesters, semDict, dictionary, visited)

    for each in semDict:
        print (each, semDict[each])

#Tests to see if the length of all prereqs are length 1 (and) and is a edge case class
def isOwnClass(prereqs):
    if all(len(ors) is 1 for ors in prereqs):
        return True
    return False

def ifEmpty(semesters, semDict, test, visited):
    for sem in semesters:
        while semDict[sem][0] < 12:
            for course in test:
                courseInfo = test[course]
                addFormat = (course.program, course.designation)
                if (course not in visited and
                    termOffer(sem, courseInfo, semDict) and len(courseInfo.prereqs) is 0):
                    visited.append(course)
                    semDict[sem][0] += int (courseInfo.credits)
                    semDict[sem][1].append(addFormat)
                    break

#for every semester in semester dictionary
#while semdict[semester][0] < 12
#find the next course in the big dictionary that the course is not already completed
#the semester is in the courseInfo terms and the length of the course prereqs is 0
#append the course and add the credits


def scheduler(semesters, semDict, test, course, courseInfo, prereqs):
    firstAvail = lastPreSem(semesters, prereqs, semDict)
    for sem in range((firstAvail + 1), 8):
        if hoursCheck(semesters[sem], courseInfo, semDict):
            if termOffer(semesters[sem], courseInfo, semDict):
                semDict[semesters[sem]][0] += int (courseInfo.credits)
                semDict[semesters[sem]][1].append(course)
                return

"""
These are the scheduler helper functions
"""

def hoursCheck(semester, courseInfo, semDict):
    if semDict[semester][0] + int (courseInfo.credits) <= 18:
        return True
    return False

def semesterPrecheck(semester, prereqs):
    for prereqs in prereqs:
        if prereqs in semDict[semester][1]:
            return False
    return True

def termOffer(semesters, courseInfo, semDict):
    if semesters[1] in courseInfo.terms:
        return True
    return False

def lastPreSem(semesters, prereqs, semDict):
    maxSem = -1
    for x in range (8):
        for prereq in prereqs:
            if prereq in semDict[semesters[x]][1]:
                maxSem = x
    return maxSem

#find the first available semester
"""
These are the search algorithm helper functions
"""

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
