import pandas as pd
import random

# Load the CSV files into DataFrames
faculty_df = pd.read_csv('file1.csv', delimiter=';')
class_df = pd.read_csv('file2.csv', delimiter=';')
course_faculty_df = pd.read_csv('file3.csv', delimiter=';')
course_df = pd.read_csv('file4.csv', delimiter=';')

# Sample data for simplicity, replace with actual data from DataFrames
classes = class_df['classid'].unique()
courses = course_df['Course Code'].unique()
faculty = faculty_df['facultycode'].unique()
hoursPerWeek = course_df['hours per week']

#given a class returns its subjects and the respective faculty
def class_courses(Class):
    classes, courses = class_df['classid'], class_df['Course Code']
    courses1 = course_df['Course Code']
    course = course_faculty_df['Course Code']
    faculties = course_faculty_df['facultycode']
    Courses = [courses[_] for _ in range(len(classes)) if classes[_] == Class]
    faculty_with_course = [[course[_],faculties[_]] for _ in range(len(faculties)) if course[_] in Courses]
    overall = []
    for c in faculty_with_course:
        for _ in range(len(courses1)):
            if c[0] == courses1[_]:
                overall.extend([c]*int(hoursPerWeek[_]))
    return overall

# Parameters for the genetic algorithm
POPULATION_SIZE = 100
NUM_GENERATIONS = 10
MUTATION_RATE = 0.1
NUM_CLASSES = len(classes)
NUM_TIMESLOTS = 40  # Example number of time slots per week

# Period time mapping
period_times = {
    0: "M1",  1: "M2",  2: "M3",  3: "M4",  4: "M5",  5: "M6",  6: "M7",  7: "M8",
    8: "T1",  9: "T2", 10: "T3", 11: "T4", 12: "T5", 13: "T6", 14: "T7", 15: "T8",
    16: "W1", 17: "W2", 18: "W3", 19: "W4", 20: "W5", 21: "W6", 22: "W7", 23: "W8",
    24: "Th1", 25: "Th2", 26: "Th3", 27: "Th4", 28: "Th5", 29: "Th6", 30: "Th7", 31: "Th8",
    32: "F1", 33: "F2", 34: "F3", 35: "F4", 36: "F5", 37: "F6", 38: "F7", 39: "F8"
}


# Fitness function
def fitness(timetable):
    # Define a fitness function that evaluates the quality of the timetable
    score = 0
        
    
    #faculty_schedule = {fac: [0] * NUM_TIMESLOTS for fac in faculty}
    #to check if the faculty is assigned multiple classes in a single time slot 
    # Initialize a dictionary to track faculty assignments
    faculty_timeslot_tracker = {fac: [0] * NUM_TIMESLOTS for fac in faculty}
    course_distribution = {course: [0] * NUM_TIMESLOTS for course in courses}


# To check if the faculty is assigned multiple classes in a single time slot 
    for cls, schedule in timetable.items():
        for timeslot, periods in enumerate(schedule):
            if periods != "free":
                course, fac = periods
                # nothing is done if it is correct
                faculty_timeslot_tracker[fac][timeslot] += 0

                # Check if the faculty is assigned to more than one class at the same timeslot
                if faculty_timeslot_tracker[fac][timeslot] > 1:
                    score -= 1  # Penalize for multiple assignments



                    
        
    #for work load distribution 
    for fac, schedule in faculty_timeslot_tracker.items():
        if any(slot > 1 for slot in schedule):
            score -= 1  #pnalised for irrgular distribution 
    for course, distribution in course_distribution.items():
        total_slots = sum(1 for slot in distribution if slot > 0)
        expected_slots = NUM_TIMESLOTS / len(courses)  # Simplified expected distribution
        
        if total_slots > expected_slots - 1 and total_slots < expected_slots + 1:
            score += 0  # Reward for good distribution
        else:
            score -= 1  # Penalize for poor distribution    
   
    return score
    
    
   
    


# Initialize population
def create_individual():
    timetable = {}
    for cls in classes:
        crsList = class_courses(cls)
        timetable[cls] = ["free" for i in range(NUM_TIMESLOTS)]
        #timeslotcopy=dict(timeslot)
        #timetable[cls].append(timeslotcopy)
        numslot=[x for x in range(NUM_TIMESLOTS)]
        for _ in range(NUM_TIMESLOTS):
            if crsList:
                randomClass = random.choice(crsList)
                randomslot=random.choice(numslot)
                timetable[cls][randomslot]=randomClass
                crsList.remove(randomClass)
                numslot.remove(randomslot)
            else:
    
                break
    #print(timetable)
    return timetable#time table is a dict with key value as the class name and values as a nasted list of course and the respective faculty member of the course

def create_population():
    return [create_individual() for _ in range(POPULATION_SIZE)]

# Crossover
def crossover(parent1, parent2):
    child = {}
    for cls in classes:
        child[cls] = ["free" for _ in range(NUM_TIMESLOTS)]
        
        for timeslot in range(NUM_TIMESLOTS):
            if random.random() > 0.5:
                selected_parent = parent1
            else:
                selected_parent = parent2
            
            for attempt in range(NUM_TIMESLOTS):  # Limiting the number of attempts to NUM_TIMESLOTS
                if timeslot >= len(selected_parent[cls]):
                    break  # Prevent out-of-range access
                child[cls][timeslot] = selected_parent[cls][timeslot]
                if child[cls][timeslot] == "free":
                    break
                teacher = child[cls][timeslot][1]
    
                # Check if the slot is already occupied by the same faculty member for another class
                for other_cls in classes:
                    if other_cls != cls:
                        if timeslot < NUM_TIMESLOTS and timeslot < len(child.get(other_cls, [])) and timeslot < len(selected_parent.get(other_cls, [])):
                            
                            if child.get(other_cls, [])[timeslot] == (selected_parent.get(other_cls, [])[timeslot][0], teacher):
                                conflict = True
                                break
                        else:
                            conflict = False

                if not conflict:
                    break  # No conflict, exit the loop
                else:
                    timeslot = (timeslot + 1) % NUM_TIMESLOTS  # Move to the next timeslot
    return child




# Mutation
def mutate(individual):
    for cls in classes:
        if random.random() < MUTATION_RATE:
            crsList = class_courses(cls)
            indtimeslot = [x for x in range(NUM_TIMESLOTS)]
            random.shuffle(indtimeslot)  # Shuffle timeslots to introduce randomness
            
            for _ in range(NUM_TIMESLOTS):
                if crsList:
                    randomClass = random.choice(crsList)
                    faculty_of_class = randomClass[1]
                    
                    # Select a random slot until a suitable one is found
                    for attempt in range(NUM_TIMESLOTS):  # Limiting the number of attempts to NUM_TIMESLOTS
                        randomslot = indtimeslot[attempt]
                        if individual[cls][randomslot] == "free" or (
                            individual[cls][randomslot] != "free" and individual[cls][randomslot][1] != faculty_of_class
                        ):
                            individual[cls][randomslot] = randomClass
                            crsList.remove(randomClass)
                            break
                else:
                    break
    return individual





# Main genetic algorithm
gen=[]
def genetic_algorithm():
    population = create_population()
    
    for generation in range(NUM_GENERATIONS):
        population = sorted(population, key=fitness, reverse=True)
        
        new_population = population[:10]  # Keep the top 10 individuals
        
        for _ in range(POPULATION_SIZE - 10):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        
        population = new_population
        
        best_timetable = population[0]
        gen.clear()
        gen.append(f"Generation {generation}: Best Fitness = {fitness(best_timetable)}")
        #gen.extend(generation,":BEST FITNESS=",fitness(best_timetable))
    return best_timetable

best_timetable = genetic_algorithm()
#print(best_timetable["20PC"])
 #this prints the total number of classes for a particular course for the class 20PC as a nested list
'''
# Output the best timetable with period times
for cls, schedule in best_timetable.items():
    print(f"Class {cls}:")
    for timeslot, timeper in enumerate(schedule):
        if timeper!="free":
            period_time = period_times[timeslot]
            print(f"  {period_time}: {timeper[0]} with {timeper[1]}")
        else:
            period_time=period_times[timeslot]
            print(f"{period_time}:{timeper}")

#To create a individual time table for each faculty
'''

faculty_timetable = {fac: [] for fac in faculty}

for cls, schedule in best_timetable.items():
    for timeslot, timeper in enumerate(schedule):
        if timeper!="free":
            period_time = period_times[timeslot]
            faculty_timetable[timeper[1]].append((period_time, cls, timeper[0]))
#print(faculty_timetable["C6161"])
'''
# Output the individual faculty timetables
for fac, schedule in faculty_timetable.items():
    print(f"Faculty {fac}:")
    for period_time, cls, course in schedule:
        print(f"  {period_time}: Class {cls}, Course {course}")
    print()
'''
#to check that every class is assigned correctly as per the number of hours
z=[]
al=[]
for cls in classes:
    x=class_courses(cls)
    #print(x,len(x))
   
    y=list(best_timetable[cls])
    
    z.append(len(x))
    al.append(40-(y.count("free")))
print(z)
print(al)




#to check the faculty is assigned a single class in the given time slot



for fac, periods in faculty_timetable.items():
    timeslot_dict = {}
    for period in periods:
        period_time, cls, subject = period
        if period_time not in timeslot_dict:
            timeslot_dict[period_time] = []
        timeslot_dict[period_time].append(cls)
    
    # Print conflicts
    for period_time, classes in timeslot_dict.items():
        if len(classes) > 1:
            #print(f"Faculty {fac} is assigned to multiple classes {classes} at {period_time}")
            #print("so initiallising the genetic algorithm again")
            genetic_algorithm()
#print(best_timetable["20PC"])    
# Output the best timetable with period times
print(gen)
for cls, schedule in best_timetable.items():
    print(f"Class {cls}:")
    for timeslot, timeper in enumerate(schedule):
        if timeper!="free":
            period_time = period_times[timeslot]
            print(f"  {period_time}: {timeper[0]} with {timeper[1]}")
        else:
            period_time=period_times[timeslot]
            print(f"{period_time}:{timeper}")




      
        
        
              

