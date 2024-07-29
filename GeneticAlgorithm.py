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

# Period time mapping
period_times = {
    0: "M1",  1: "M2",  2: "M3",  3: "M4",  4: "M5",  5: "M6",  6: "M7",  7: "M8",
    8: "T1",  9: "T2", 10: "T3", 11: "T4", 12: "T5", 13: "T6", 14: "T7", 15: "T8",
    16: "W1", 17: "W2", 18: "W3", 19: "W4", 20: "W5", 21: "W6", 22: "W7", 23: "W8",
    24: "Th1", 25: "Th2", 26: "Th3", 27: "Th4", 28: "Th5", 29: "Th6", 30: "Th7", 31: "Th8",
    32: "F1", 33: "F2", 34: "F3", 35: "F4", 36: "F5", 37: "F6", 38: "F7", 39: "F8"
}

#given a class returns its subjects and the respective faculty
def class_courses(Class):
    classes, courses = class_df['classid'], class_df['Course Code']
    courses1 = course_df['Course Code']
    course = course_faculty_df['Course Code']
    faculties = course_faculty_df['facultycode']
    Courses = [courses[_] for _ in range(len(classes)) if classes[_] == Class]
    faculty_with_course = [[course[_], faculties[_]] for _ in range(len(faculties)) if course[_] in Courses]
    overall = []
    for c in faculty_with_course:
        for _ in range(len(courses1)):
            if c[0] == courses1[_]:
                overall.extend([c] * int(hoursPerWeek[_]))
    remainingClass = len(period_times) - len(overall)
    overall.extend(['Free Period'] * int(remainingClass))
    return overall

# Parameters for the genetic algorithm
POPULATION_SIZE = 100
NUM_GENERATIONS = 5
MUTATION_RATE = 0.1
NUM_CLASSES = len(classes)
WORKING_DAYS = 5
NUM_TIMESLOTS = 40  # Example number of time slots per week

# Fitness function
def fitness(timetable):
    # Define a fitness function that evaluates the quality of the timetable
    fitness_score = 0
    total_slots = 0
    for cls, schedule in timetable.items():
        if len(schedule) != NUM_TIMESLOTS:
            fitness_score += 100
        else:
            total_slots += NUM_TIMESLOTS
        expected = class_courses(cls)
        expected_Courses = [x for x in expected if x != "Free Period"]
        obtained_Courses = [x for x in schedule if x != "Free Period"]
        if sorted(expected_Courses) != sorted(obtained_Courses):
            fitness_score += 100
    if total_slots == NUM_TIMESLOTS*len(classes):
        for _ in range(NUM_TIMESLOTS):
            x = [timetable[cls][_][1] for cls in classes if timetable[cls][_] != "Free Period"]
            y = set(x)
            if len(x) != len(y):
                fitness_score += 1
    return fitness_score

#initializing population
def create_individual():
    timetable = {}
    for cls in classes:
        crsList = class_courses(cls)
        timetable[cls] = []
        for _ in range(NUM_TIMESLOTS):
            if crsList:
                randomClass = random.choice(crsList)
                timetable[cls].append(randomClass)
                crsList.remove(randomClass)
            else:
                break
    return timetable

def create_population():
    return [create_individual() for _ in range(POPULATION_SIZE)]

# Crossover
def crossover(parent1, parent2):
    child = {}
    total_slots1 = 0
    for cls, schedule in parent1.items():
        child[cls] = parent1[cls]
        total_slots1 += len(schedule)
    for clss, schedule in parent1.items():
        if total_slots1 == NUM_TIMESLOTS*len(classes):
            for _ in range(NUM_TIMESLOTS):
                x = [parent1[cls][_][1] for cls in classes if parent1[cls][_] != "Free Period"]
                y = set(x)
                if len(x) != len(y):
                    if x.count(parent1[clss][_][1]) > 1:
                        for k in range(_, NUM_TIMESLOTS):
                            if child[clss][k] == parent2[clss][_]:
                                child[clss][k] = child[clss][_]
                                child[clss][_] = parent2[clss][_]
    return child

# Mutation
def mutate(individual):
    total_slots1 = 0
    for schedule in individual.values():
        total_slots1 += len(schedule)
    for cls, schedule in individual.items():
        if total_slots1 == NUM_TIMESLOTS*len(classes):
            for _ in range(NUM_TIMESLOTS):
                x = [individual[clss][_][1] for clss in classes if individual[clss][_] != "Free Period"]
                y = set(x)
                if len(x) != len(y):
                    for i in range(NUM_TIMESLOTS):
                        if individual[cls][i] == "Free Period":
                            individual[cls][i] = individual[cls][_]
                            individual[cls][_] = "Free Period"
                            break
    return individual

# Main genetic algorithm
def genetic_algorithm():
    population = create_population()
    
    for generation in range(NUM_GENERATIONS):
        population = sorted(population, key=fitness, reverse=False)
        
        new_population = population[:10]  # Keep the top 10 individuals
        
        for _ in range(POPULATION_SIZE - 10):
            parent1 = random.choice(new_population)
            parent2 = random.choice(population[:int(0.5 * POPULATION_SIZE)])
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        
        population = new_population
        
        best_timetable = population[0]
        print(f"Generation {generation}: Best Fitness = {fitness(best_timetable)}")
    
    return best_timetable

best_timetable = genetic_algorithm()

# Output the best timetable with period times
for cls, schedule in best_timetable.items():
    print(f"Class {cls}:")
    for timeslot, course_fac in enumerate(schedule):
        period_time = period_times[timeslot]
        print(f"  {period_time}: {course_fac[0]} with {course_fac[1]}") if course_fac != "Free Period" else print(f"  {period_time}: Free Period")