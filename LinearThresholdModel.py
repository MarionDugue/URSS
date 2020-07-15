import networkx as nx
import random
import scipy.stats as stats
from collections import Counter
import matplotlib.pyplot as plt

class Simulation:
    

    def __init__(self, graph, seedset, p):
        self.seedset = seedset
        self.graph = graph
        self.num_agents = graph.number_of_nodes()
        # Create a new agent for each node, by creating an 
        #agent_map and then relabeling the nodes in the graph
        agent_map = {}
        age = Simulation.ageList(len(graph))
        house = Simulation.Household(len(graph))
        friend = Simulation.Friendships(len(graph))
        for i in range(0, self.num_agents):
            agent_map[i] = Agent(age[i], house[i], friend[i])
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
                    
    def ageList(population_size):
        Count_Age65_plus = round(population_size * 25/85)
        Count_Age18_34 = round(population_size *0.5* (46*63/48)/85)
        Count_Age35_64 = Count_Age18_34
        AgeList = []
        
        for i in range(0,Count_Age18_34):
            n = random.randint(18,34)
            AgeList.append(n)
        for i in range(0,Count_Age35_64):
            n = random.randint(35,64)
            AgeList.append(n)
        for i in range(0,Count_Age65_plus):
            n = random.randint(65,100)
            AgeList.append(n)
        return AgeList
    
    def Household(population_size):
        Household_List = []
        #For 18 to 34 years old, mu = 1.54
        Count_Age18_34 = round(population_size *0.5* (46*63/48)/85)
        House18_to_34 =  stats.poisson.rvs( 1.54, loc = 0, size=Count_Age18_34)
        for i in range(0,Count_Age18_34):
            Household_List.append(House18_to_34[i])
        #For 35 to 64 years old, mu = 1.69
        Count_Age35_64 = Count_Age18_34
        House35_to_64 =  stats.poisson.rvs( 1.69, loc = 0, size=Count_Age35_64)
        for i in range(0,Count_Age35_64):
            Household_List.append(House35_to_64[i])
        #For 65+ years old, mu = 0.49
        Count_Age65_plus = round(population_size * 25/85)
        House64_plus =  stats.poisson.rvs( 0.49, loc = 0, size=Count_Age65_plus)
        for i in range(0,Count_Age65_plus):
            Household_List.append(House64_plus[i])
        
        #Because the values are decimals, we want exactly length of population_size:
        Household_List = Household_List[:population_size]
        
        
        
        
        #------------------------CHECKING WHICH VALUE IS SENSIBLE------------
        #--Counts each value in Household_List and creates a dictionary---------------------
        
        Household_Dict = dict(Counter(Household_List))
        
        
        #--Checking for multiples--------------------------------------------  
             
        Checking_multiples = []
        Not_sensible = {}
        Sensible = {}
        for size in Household_Dict:
            if size == 0:
                Sensible[size] = Household_Dict[size]
            else:
                if size == 1:
                    if Household_Dict[size] % 2 == 0:
                        Checking_multiples.append('1_is_sensible')
                        Sensible[size] = Household_Dict[size]
                    else:
                        Not_sensible[size] = Household_Dict[size]
                else:
                    if Household_Dict[size] == 1:
                        Not_sensible[size] = Household_Dict[size]
                    else:
                        if Household_Dict[size] % (size+1) == 0:
                            b = (size, "is sensible")
                            Checking_multiples.append(b)
                            Sensible[size] = Household_Dict[size]
                        else:
                            Not_sensible[size] = Household_Dict[size]
        
        #--Sorting values of Not_sensible & Sensible dictionary-------------------------------------            
        SNot_List = sorted(Not_sensible.items(), key=lambda x: x[0], reverse=True)
        #Take the 1st not sensible key
        Sorted_Household =  sorted(Household_Dict.items(), key=lambda x: x[0])
        
        #--If pair is not sensible, its count will be carried out to the next one-----------------
        credit = 0
        newpairs = []
        
        for pair in SNot_List:
            key = pair[0]
            
            if credit != 0:
                value = pair[1] + credit 
                credit = 0
                
            else:
                value = pair[1]
            if key == 1:
                    value = value + credit
                    if value % 2 != 0:
                        value = value - 1
                        Value_0 = Sorted_Household[0][1] + 1
                        newpairs.append((Sorted_Household[0][0], Value_0))
                        newpairs.append((Sorted_Household[1][0], value))
                    else:
                        newpairs.append((key, value))
            else:
                if value == 1:
                        value = 0
                        credit += 1
                        newpairs.append((key, value))
                if value == 0:
                    newpairs.append((key, value))
                else:
                    if value % (key+1) != 0:
                        #for the pair with the largest value, deduce value until satisfy divisibility condition
                        while value % (key+1) != 0:
                            value = value - 1
                            credit += 1
                        if value == 1:
                             value = 0
                             credit += 1
                        newpairs.append((key, value))
                        if SNot_List[-1] == pair:
                            for pair in Sorted_Household:
                                if pair[0] == 1:
                                    value = pair[1] + credit
                                    if value % 2 != 0:
                                        value = value - 1
                                        Value_0 = Sorted_Household[0][1] + 1
                                        newpairs.append((Sorted_Household[1][0], value))
                                        newpairs.append((Sorted_Household[0][0], Value_0))
                                    else:
                                        newpairs.append((Sorted_Household[1][0], value))
                        
                    else:
                        newpairs.append((key, value))
        
        
        
        
        #--Appending sensible pairs to the new list------------------------------------    
        
        i = 0
        while i < len(Sorted_Household):
            a = Sorted_Household[i][0]
            j = 0
            for x in newpairs:
                m = x[0]
                if a == m :
                    j = 1
            if j == 0:
                newpairs.append(Sorted_Household[i])
            i += 1
        
        #--Removing all pairs with a count = 0-----------------------------------------
            
        Cleaned_newpairs=[]
        for n in range(0,len(newpairs)):
            if newpairs[n][1] != 0:
                Cleaned_newpairs.append(newpairs[n])
           
        #--Transforming List of pairs into list of integers---------------------------      
        
        New_Householdlist = []
        for pair in Cleaned_newpairs:
            i = 0
            while i < pair[1]:
                New_Householdlist.append(pair[0])
                i += 1
        print(Cleaned_newpairs)
        return New_Householdlist

    def Friendships(population_size):
        Friends_List = []
        #(we assume at first) that everyone has 0 to 20 friends with an average at 3-5
        Friends_List =  stats.poisson.rvs( 4, loc = 0, size=population_size)
        Friends_Dict = dict(Counter(Friends_List))
        print(Friends_Dict)
        return Friends_List
            
class Agent:
    idCounter = 0
    threshold = random.uniform(0,1)
    infected = False  
    age = 0
    housesize = 0
    housefull = False
    friends = 0
    friendshipfull = False


    def __init__(self, start_age, start_household, start_friends):
        # set id and ensure each agent has unique id
        self.id = self.idCounter
        type(self).idCounter += 1
        # set threshold and ensure each agent has unique threshold
        self.th = self.threshold
        type(self).threshold = random.uniform(0,1)
        #set age
        self.age = start_age
        #set houselhold size
        self.housesize = start_household
        #set number of friends
        self.friends = start_friends

    def __str__(self):
        return "agent_" + str(self.id)

    def __repr__(self):
        return "agent_" + str(self.id)



#--------------------------------------------------------------
population_size = 10

#-------------------------------------------------
G = nx.Graph()
for i in range(0,population_size):
    G.add_node(i)

#-----------------------------------------------------------------------

#Creating random seedset with k length
k = 10
new_infected = []


#Parameter of system
p = 0.1 
s = Simulation(G, [], p)
initial_seedset = random.sample(s.graph.nodes, k)

#-----------------------------------------------------------
#Creation of network for households

for agt in G.nodes:
    if agt.housesize != 0:
        for neighbr in G.nodes:
            if agt.id != neighbr.id:
                  if agt.housesize == neighbr.housesize:
                      if agt.housefull == False and neighbr.housefull == False:
                          G.add_edge(agt,neighbr,color='b', weight=3)
                          if G.degree(agt, weight=3) == agt.housesize:
                              agt.housefull = True
                          if G.degree(neighbr) == neighbr.housesize:
                              neighbr.housefull = True

#Creation of network for friendships:
for agt in G.nodes:
    for neighbr in G.nodes:
            if agt.id != neighbr.id:
                if agt.friendshipfull == False and neighbr.friendshipfull == False:
                    if G.has_edge(agt, neighbr) == False:
                          G.add_edge(agt,neighbr,color='r', weight=1)
                          if G.degree(agt, weight=1) == agt.friends:
                              agt.friendshipfull = True
                          if G.degree(neighbr) == neighbr.friends:
                              neighbr.friendshipfull = True
 
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
weights = [G[u][v]['weight'] for u,v in edges]
pos = nx.circular_layout(G)
nx.draw(G,pos,  edges=edges, edge_color=colors, width=weights)                               
plt.legend(['Agents', 'Household'])

      
#----------------------------------------------------------------- 
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

#---------------------------
