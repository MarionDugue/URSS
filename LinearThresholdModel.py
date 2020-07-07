import networkx as nx
import random
import numpy as np, numpy.random

class Simulation:
    

    def __init__(self, graph, seedset, p):
        self.seedset = seedset
        self.graph = graph
        self.num_agents = graph.number_of_nodes()
        # Create a new agent for each node, by creating an 
        #agent_map and then relabeling the nodes in the graph
        agent_map = {}
        for i in range(0, self.num_agents):
            agent_map[i] = Agent()
        nx.relabel_nodes(self.graph,agent_map,copy=False)


    # placeholder to represent a single iteration of the simulation, i.e. each agent selects a neighbour at random
    def tick(self, graph, seedset , p):
        
        new_infected = []
        for a in graph.nodes():
            if a.id not in seedset:
                #Finding neighbours
                neighbour = list(graph.neighbors(a))
                #Defining ID of neighbours in a list. Not used: it's a way to check the neighbour list makes sense
                IDNeighbours = []
                i = 0
                while i< len(neighbour):
                    IDNeighbours.append(neighbour[i].id)
                    i = i+1
                #Finding activated neighbours => putting their edge weight in a list
                ActivatedWeights = []
                for n in neighbour:
                    if n.id in seedset:
                        ActivatedWeights.append(graph[n][a]['weight'])
                    #Summing that list
                    SUM = sum(ActivatedWeights)
                    #Checking condition
                    if a.th < SUM :
                        new_infected.append(a.id)
                        seedset.append(a.id)
        return len(new_infected), seedset
                    
    
class Agent:
    idCounter = 0
    threshold = random.uniform(0,1)

    def __init__(self):
        # set id and ensure each agent has unique id
        self.id = self.idCounter
        type(self).idCounter += 1
        # set threshold and ensure each agent has unique threshold
        self.th = self.threshold
        type(self).threshold = random.uniform(0,1)


    def __str__(self):
        return "agent_" + str(self.id)

    def __repr__(self):
        return "agent_" + str(self.id)



#--------------------------------------------------------------
population_size = 1000

# Example topologies - see networkX docs for more details
# Note the parameters below are NOT SENSIBLE VALUES - they are just to illustrate
# https://networkx.github.io/documentation/stable/reference/generators.html

# fully connected
# G = nx.complete_graph(population_size)

# regular random graph
# degree = 3
# G = nx.random_regular_graph(degree, population_size)

# small-world
# t_k = 10
# t_p = 0.3
# G = nx.connected_watts_strogatz_graph(population_size, t_k, t_p)

# Barabasi_albert scale-free
t_p = 0.1
t_q = 0.1
t_m = 3
G = nx.extended_barabasi_albert_graph(population_size, t_m, t_p, t_q)

print(nx.info(G))
#-----------------------------------------------------------------------

#Creating random seedset with k length
k = 10
seedset = random.sample(G.nodes,k )
new_infected = []


p = 0.1 #parameter of system

s = Simulation(G, seedset,p)

# cache each agent's neighbor list - could looked up each time depending what you are doing
for n in s.graph.nodes():
    n.neighbors = [agt for agt in s.graph.neighbors(n)]
    #print(n.neighbors)

    
    
#Assigning weights


for u in G.nodes():
    neighbour = list(G.neighbors(u))
    IDNeighbours = []
    i = 0
    while i< len(neighbour):
        IDNeighbours.append(neighbour[i].id)
        i = i+1
    length = len(IDNeighbours)
    k = len(list(G.neighbors(u)))
    p = np.random.dirichlet(np.ones(k), size=1) 
    p = p[0]
    i = 0
    for n in neighbour:
        G[u][n]['weight'] = p[i]
        i = i+1

    
    
    

# run the simulation for appropriate number of iterations
#t iterations
t = 1000
j = 1
i = 0
while j == 1 and  i < t:
        LNI, seedset = s.tick(G, seedset, p)
        if LNI == 0:
            print("Number of iterations is:", i)
            j = 0  
        i = i +1
        
#--------------------------------------













