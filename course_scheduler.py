import sys
from collections import namedtuple
import course_dictionary
import warnings; warnings.simplefilter('ignore')

def main(argv):
    test = course_dictionary.create_course_dict()
    Course = namedtuple('Course', 'program, designation')
    goals = Course('CS', 'major')
    #print(test[Course('CS', 'major')])
    init_state = []
    #course_dictionary.print_dict(test)
    srch_alg(test, goals, init_state)
    print('Done')

def scheduler(dictionary, init, goals):
    courses = [goals]
    semesters = [('Frosh', 'Fall'), ('Frosh', 'Spring'), ('Soph', 'Fall'),
                ('Soph', 'Spring'),('Junior', 'Fall'), ('Junior', 'Spring'),
                ('Senior', 'Fall'), ('Senior', 'Spring')]
    semDict = {semester:[0, []] for semester in semesters}

    #starting at given semesters
    #




def srch_alg(dictionary, start, visited):
    #Pushing the goal state on the top of the stack
    stack = [start]
    #While the stack is not empty
    while stack:
        #Sets course = to the top element of the stack
        course = stack.pop()
        #If the course is not in the list "visited" then...
        if course not in visited:
            #Pull the dictionary information regarding the course and set to info
            courseInfo = dictionary[course]
            #Add the course to the list "visited"
            visited.append(course)
            #??if courseInfo.credits is not '0':
            #Print out Course and corresponding information
            print (course, courseInfo)
            #If according to the courseInfo there are any prerequisites for the course...
            if len (courseInfo.prereqs) is not 0:
                #Create an empty list tmpStk
                tmpStk = []
                #Starting at the first prereq for all prereqs of course
                for prereq in courseInfo.prereqs[0]:
                    #If the prereq isnt visited add to the tmpStk
                    if prereq not in visited:
                        tmpStk.append(prereq)
                #while tmpstk isnt empty transfer contents to the main stack
                while tmpStk:
                    stack.append(tmpStk.pop())

if __name__ == "__main__":
    main(sys.argv)