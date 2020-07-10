import networkx as nx
import random

class Simulation:

    def __init__(self, graph, seedset, p):
        self.seedset = seedset
        self.graph = graph
        self.num_agents = graph.number_of_nodes()
        # Create a new agent for each node, by creating an 
        #agent_map and then relabeling the nodes in the graph
        agent_map = {}
        a = Simulation.ageList(len(graph))
        for i in range(0, self.num_agents):
            agent_map[i] = Agent(a[i])
        nx.relabel_nodes(self.graph,agent_map,copy=False)

    def ageList(population_size):
        Count_Age65_plus = round(population_size * 25/88)
        Count_Age18_34 = round(population_size *0.5* 63/88)
        Count_Age35_64 = Count_Age18_34
        AgeList = []
        for i in range(0,Count_Age65_plus):
            n = random.randint(65,100)
            AgeList.append(n)
        for i in range(0,Count_Age18_34):
            n = random.randint(18,34)
            AgeList.append(n)
        for i in range(0,Count_Age35_64):
            n = random.randint(35,64)
            AgeList.append(n)
        #Making the list random:
        Random_AgeList = random.sample(AgeList, len(AgeList))
        return Random_AgeList
    
    
    # placeholder to represent a single iteration of the simulation, i.e. each agent selects a neighbour at random
    def tick(self, infected_last_iteration , p):
        new_infected = []
        # for each agent, a, that was infected in the previous round (or the seed set in initial round)
        for a in infected_last_iteration:
            neighbors = a.neighbors
            # for each of a's neighbours
            for n in neighbors:
                rand = random.uniform(0,1)
                if rand < p:
                    if n not in infected_last_iteration and not n.infected:
                        new_infected.append(n)
        for n in new_infected:
            n.infected = True
        return new_infected

class Agent:
    idCounter = 0
    infected = False
    neighbors = None
    age = 0
    

    def __init__(self, start_age):
        # set id and ensure each agent has unique id
        self.id = self.idCounter
        type(self).idCounter += 1
        #set age
        self.age = start_age

    def __str__(self):
        return "agent_" + str(self.id)

    def __repr__(self):
        return "agent_" + str(self.id)

#--------------------------------------------------------
population_size = 1000


#----------------------------------------------------------------
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

#Creating random seedset with k length
k = 10


# new_seedset = random.sample(s.graph.nodes, k)
new_infected = []


p = 0.1 #parameter of system
# s = Simulation(G, new_seedset,p)
s = Simulation(G, [] ,p)



initial_seedset = random.sample(s.graph.nodes, k)


p = 0.1 #parameter of system



# cache each agent's neighbor list - could looked up each time depending what you are doing
for n in s.graph.nodes():
    n.neighbors = [agt for agt in s.graph.neighbors(n)]

# run the simulation for appropriate number of t iterations
t = 1000

# in the first iteration use the seedset as the agents infected last round
previous_infections = initial_seedset
print("seedset size: ", len(previous_infections))
for i in range(0,t):
    new_infections = s.tick(previous_infections, p)
    print("iteration ", i, " number of new infections: ", len(new_infections))
    if not new_infections:
        break
    previous_infections = new_infections
    
