import pandas as pd
import random

# Load the CSV files into DataFrames
faculty_df = pd.read_csv('file1.csv', delimiter=';')
class_df = pd.read_csv('file2.csv', delimiter=';')
course_faculty_df = pd.read_csv('file3.csv', delimiter=';')
course_df = pd.read_csv('file4.csv', delimiter=';')

#print(faculty_df)
#print(class_df)
#print(course_faculty_df)
#print(course_df)
x=list(class_df["classid"])
y=list(course_df["Course Code"])
z=list(faculty_df['facultycode'])
alpha=list(zip(y,z))
beta=list(course_faculty_df["Course Code"])
gamma=list(course_faculty_df["facultycode"])
betagamma=list(zip(beta,gamma))


# Sample data for simplicity, replace with actual data from DataFrames
classes = class_df['classid'].unique()
courses = course_df['Course Code'].unique()
faculty = faculty_df['facultycode'].unique()

# Parameters for the genetic algorithm
POPULATION_SIZE = 100
NUM_GENERATIONS = 5
MUTATION_RATE = 0.1
NUM_CLASSES = len(classes)
NUM_TIMESLOTS = 8  # Example number of time slots per week

# Period time mapping
period_times = {
    0: "08:30 - 09:20",
    1: "09:20 - 10:10",
    2: "10:30 - 11:20",
    3: "11:20 - 12:10",
    4: "01:00 - 01:40",
    5: "01:40 - 02:30",
    6: "02:30 - 03:20",
    7: "03:30 - 04:20",
}

# Fitness function
def fitness(timetable):
    # Define a fitness function that evaluates the quality of the timetable
    return 0

# individual timetable
def ind_timetable(cls):
    ind=[]
    ind1=[]
    ind2=[]
    for j in x:
        if j==cls:
            ind.append(x.index(j))
    for i in ind:
        ind1.append(beta[i])
        ind2.append(gamma[i])
    #print(ind1,ind2)
    return [ind1,ind2]    


# Initialize population
def create_individual():
    timetable = {}
    
    for cls in classes:
        cre=ind_timetable(cls)
        #print(cre[0])
        cre1=cre[0]
        cre2=cre[1]
        for _ in range(NUM_TIMESLOTS):
            #print("hi i am mukil raj")
            if len(cre1)!=0:

                x1=random.choice(cre1)
                x2=random.choice(cre2)
                timetable[cls] = [(x1,x2)]
                cre1.remove(x1)
                cre2.remove(x2)
            
    return timetable

def create_population():
    return [create_individual() for _ in range(POPULATION_SIZE)]

# Crossover
def crossover(parent1, parent2):
    child = {}
    for cls in classes:
        if random.random() > 0.5:
            child[cls] = parent1[cls]
        else:
            child[cls] = parent2[cls]
    return child

# Mutation
def mutate(individual):
    for cls in classes:
        if random.random() < MUTATION_RATE:
            individual[cls] = [(random.choice(courses), random.choice(faculty)) for _ in range(NUM_TIMESLOTS)]
    return individual

# Main genetic algorithm
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
        print(f"Generation {generation}: Best Fitness = {fitness(best_timetable)}")
    
    return best_timetable

best_timetable = genetic_algorithm()

# Output the best timetable with period times
for cls, schedule in best_timetable.items():
    print(f"Class {cls}:")
    for timeslot, (course, fac) in enumerate(schedule):
        period_time = period_times[timeslot]
        print(f"  {period_time}: {course} with {fac}")