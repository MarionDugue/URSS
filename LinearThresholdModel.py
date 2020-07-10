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
    def tick(self, graph, infected_last_iteration , p):
        
        new_infected = []
        for a in graph.nodes():
            if a not in infected_last_iteration and not a.infected:
                neighbour = list(graph.neighbors(a))
                ActivatedWeights = []
                for n in neighbour:
                    if n in infected_last_iteration:
                        ActivatedWeights.append(graph[n][a]['weight'])
                SUM = sum(ActivatedWeights)
                if a.th < SUM :
                    new_infected.append(a)
        for a in new_infected:
            a.infected = True
        return new_infected
                    
    
class Agent:
    idCounter = 0
    threshold = random.uniform(0,1)
    infected = False


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
new_infected = []


#Parameter of system
p = 0.1 
s = Simulation(G, [], p)
initial_seedset = random.sample(s.graph.nodes, k)


# cache each agent's neighbor list - could looked up each time depending what you are doing
for n in s.graph.nodes():
    n.neighbors = [agt for agt in s.graph.neighbors(n)]
    #print(n.neighbors)

    
    
#Assigning weights
for u in G.nodes():
    neighbour = list(G.neighbors(u))
    Edge_list = []
    for n in neighbour:
        #Generating x weights for x neighbours of node n 
        G[u][n]['weight'] = random.uniform(0,10)
        Edge_list.append(G[u][n]['weight'])
    #Sum edges to get total
    Sum_Edges= sum(Edge_list)
    for n in neighbour: 
        G[u][n]['weight'] = (G[u][n]['weight'])/Sum_Edges

    
    
    

# run the simulation for appropriate number of iterations
#t iterations
t = 1000
previous_infections = initial_seedset
for i in range(0,t):
    new_infections = s.tick(G, previous_infections, p)
    print("iteration ", i, " number of new infections: ", len(new_infections))
    if not new_infections:
        break
    previous_infections = new_infections
