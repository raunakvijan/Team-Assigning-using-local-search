#!/usr/bin/env python3
# put your group assignment problem here!
#!/bin/python
# put your group assignment problem here!

'''
Sample space: 
This will be all possible combinations of students in all possible team sizes. 
The team sizes can be 1, 2 or 3.

Initial state: 
For our search problem we just start with a state where all the students are alone.

Cost function:
It is the total time taken for grading. It can be found out by multipying the k, m and n 
values by team size, no of students assigned not requested teammate, no of students not
assigned their requested friends.  

Successor function: 
In our search problem we consider only N neighbours.(This parameter is currently set to 100)
A neighbour is any team combination where either one member is swapped between the teams or 
one member is removed from a team and added to another team.

Search strategy: 

The first though that came into mind when I saw this problem was that the sample space
would be huge. 
Which is true. I tried to generate all the possible permutations and then result the one 
with minimum cost. However, even though the its guaranteed to return the best solution 
it is very very slow. The code was taking forever even for a class size of 15. 

When looking for a solution for batch size like that of C551 (around 130) this kind of 
approach is not at all practical (We will probably finish our assignment 1 in the time 
taken for this algorithm to return the result :P)

Hence, it is clear that a optimal solution won't be possible in this case. 

We have to use a local search technique. It is not guaranteed to return a optimal return 
however it tries to get as close as the optimal result.

Local search technique used: 

In order to solve this problem we used gradient descent inspired search technique.
The algorithm looks for the neighbours and then selects the one with the least cost function
After this it selects that state and performs the same steps. 

At each step the search moves to a more promising solution. 

The end condition is until a fixed number of iterations are completed.
This number of iterations can only be determined experimentally.

There are two hyperparameters in our case. no_of_nodes_expand and no_of_iterations. 
The higher the values for these parameters the longer it will take for the code to run. 
Setting these values is a trade off between the optimallity of the solution and time taken. 

Based on our experiments we got the following results.
For values
k = 30, m = 5, n = 20
(The algorithm uses some randomness. So the answer will not always be zero)

node_expand  = 50 iterations = 50
minimum cost = 1284 time taken to run = 1.5s 

node_expand  = 100 iterations = 50
minimum cost = 1284 time taken to run = 2.2s

node_expand  = 100 iterations = 50
minimum cost = 1272 time taken to run = 2.2s

nodes_expand = 100 iterations = 100
minimum cost = 1250 time taken to run = 4.5s

nodes_expand = 100 iterations = 500
minimum cost = 1250 time taken to run = 4.5s

nodes_expand = 100 iterations = 1000
minimum cost = 1105 time taken to run = 92.3s

nodes_expand = 100 iterations = 2000
minimum cost = 1101 time taken to run = 366.7s

nodes_expand = 500 iterations = 2000
minimum cost = 1108 time taken to run = 285.2s

We observe that nodes_expand = 100 iterations = 1000
gives the best result based on time vs optimality and is the best parameter for this data set.
After certain value of number of iterations the solution does not seem to improve even
though there may exist a better solution. This is because the gradient descent may get 
stuck in local minima. The cost function graph for this problem is not like the the cost
function for the least square error (U shaped which doesn't suffer for local minima).

We researched at lot about this on the internet and saw various solutions possible for this
problem like genetic algorithm, Monte Carlo and simulated annealing. However, due to time 
contraint we couldn't do the coding of these algorithm and hence we stick to the gradient descent 
method.
'''

import random
import csv
import pandas as pd
from queue import PriorityQueue
import copy
import math
from random import shuffle
import sys

students = {}

# read input from file and store in a dictionary
def read(input_file):
	with open(input_file,"r") as f:
		for line in f.readlines():
			data = line.split()
			students[data[0]] = int(data[1]), data[2], data[3]
	return students

# this function calculates the total time taken based on the k, m, n values
def cost_function(teams):
	not_size = 0
	not_requested = 0
	not_assigned_prefer = 0
	for team in teams:
		for member in team:
			student_list = students[member]
			student_satisfied[member] = True
			if(len(team) != student_list[0] and student_list[0] != 0):
				not_size += 1
				
			
			for team_member in student_list[1].split(','):
				if(team_member not in team and team_member != '_'):
					not_assigned_prefer += 1

			for not_req in student_list[2].split(','):
				if(not_req in team):
					not_requested+= 1
				
	return k*len(teams) + not_size + n*not_assigned_prefer + m*not_requested


# this function 
def gradient_search(state):
	team = copy.deepcopy(state)
	fringe = PriorityQueue()
	for i in range(no_of_nodes_expand):
		team = copy.deepcopy(state)
		length = len(team)
		operation = random.randint(0, 1)
		
		# select random teams and random members from those teams.
		team_a = random.randint(0, length - 1)
		team_b = random.randint(0, length - 1)

		pos_a = random.randint(0, len(team[team_a]) - 1 )
		pos_b = random.randint(0, len(team[team_b]) - 1 )

		# get neighbour through operations  	
		if(operation == 0):
			# swap elements
			team[team_a][pos_a], team[team_b][pos_b] = team[team_b][pos_b], team[team_a][pos_a]

		elif(operation == 1):
			# remove from a and add in b
			flag = True
			loops = 0

			while(flag and loops < 10):
				loops += 1
				team_a = random.randint(0, len(team) - 1)
				team_b = random.randint(0, len(team) - 1)
				shuffle(team[team_a])
				shuffle(team[team_b])

				pos_a = random.randint(0, len(team[team_a]) - 1 )
				if(len(team[team_b]) >= 3):
					continue

				if(len(team[team_a]) == 1):
					if(len(team) == 1):
						team_b = 0
					else:
						team_b = random.randint(0, len(team) - 2)
					if(len(team[team_b]) < 3):
						element_to_add = team[team_a].pop(pos_a)

						team.pop(team_a)
					else:
						continue
				else:
					element_to_add = team[team_a].pop(pos_a)
				
				# for the add from a team and add to another team we check if 
				# the team size is already 3 and if it then we don't add the 
				# new member to satisfy the condition that team size cannot exceed 3.

				if(len(team[team_b]) == 3):
					team.append([element_to_add])
					continue
				team[team_b].append(element_to_add)
				flag = False
				
		cost_team = cost_function(team)
		global minimum_cost
		global minimum_cost_team
			
		if (cost_team < minimum_cost):
			
			minimum_cost = cost_team
			minimum_cost_team = team

file_name = "ex-assign50.txt"
file_name = str(sys.argv[1])
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])


student_satisfied = {}
students = read(file_name)
teams = []

for i in  list(students.keys()):
	teams.append([i])
time = 0
minimum_cost = math.inf
minimum_cost = cost_function(teams)
minimum_cost_team = teams

no_of_iterations = 100
no_of_nodes_expand = 100

for i in range(no_of_iterations):
	shuffle(minimum_cost_team)
	gradient_search(minimum_cost_team)

for i in minimum_cost_team:
	for j in i: 
		print(j,end=" ")
	print("\n",end="")
print(minimum_cost)