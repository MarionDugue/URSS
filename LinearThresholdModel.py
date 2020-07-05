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
    def tick(self, graph, seed , p):
            new_infected = []
            for b in seed:
                for a in graph.nodes():
                    if a.id == b:
                        n = G.neighbors(a)
                        i = 0
                        n_id = []
                        for f in n:
                            n_id.append(f.id)
                            i = i+1
                        len_n = i
                        def weight(n):
                            '''creates list of n weights where n is the # of 
                            neighbors of the node in the seed set'''
                            k = len_n
                            p = np.random.dirichlet(np.ones(k), size=1)
                            return p[0]
                        weight_list = weight(n)
                        j = 0 
                        activated_weight = []
                        while j < len_n:
                            if n_id[j] in seed:
                                activated_weight.append(weight_list[j])
                            j = j +1
                        L_sum = sum(activated_weight)
                        if a.th <= L_sum :
                            for c in n_id:
                                switch = 1
                                for x in seed:
                                    if x == c:
                                        switch = 0
                                if switch == 1:
                                    new_infected.append(c)
                                    seed.append(c)


            seed = new_infected + seed
            return len(new_infected)
                        
    
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
        return 'self.id'



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
k = 300
seedset = random.sample(G.nodes,k )
new_infected = []

p = 0.1 #parameter of system
s = Simulation(G, seedset,p)

# cache each agent's neighbor list - could looked up each time depending what you are doing
for n in s.graph.nodes():
    n.neighbors = [agt for agt in s.graph.neighbors(n)]
#    print(n.neighbors)
#
# run the simulation for appropriate number of iterations
#t iterations
t = 1000
j = 1
i = 0
while j == 1 and  i < t:
        LNI = s.tick(G, seedset, p)
        print(LNI)
        if LNI == 0:
            print("Number of iterations is:", i)
            j = 0  
        i = i +1


