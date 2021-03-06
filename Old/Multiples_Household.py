import matplotlib.pyplot as plt
import scipy.stats as stats
from collections import Counter

#---------------------------------PARAMETERS--------------------



#--------------------------------DEFINING INITIAL HOUSEHOLD LIST----
def HouseholdList(population_size):
        Household_List = []
        Household_List_18_to_34 = []
        Household_List_34_to_64 = []
        Household_List_65_plus = []
        #For 18 to 34 years old, mu = 1.54
        Count_Age18_34 = round(population_size *0.26)
        House18_to_34 =  stats.poisson.rvs( 1.54, loc = 0, size=Count_Age18_34)
        for i in range(0,Count_Age18_34):
            Household_List_18_to_34.append(House18_to_34[i])
        #For 35 to 64 years old, mu = 1.69
        Count_Age35_64 = round(population_size *0.49)
        House35_to_64 =  stats.poisson.rvs( 1.69, loc = 0, size=Count_Age35_64)
        for i in range(0,Count_Age35_64):
            Household_List_34_to_64.append(House35_to_64[i])
        #For 65+ years old, mu = 0.49
        Count_Age65_plus = round(population_size * 0.25)
        House65_plus =  stats.poisson.rvs( 0.49, loc = 0, size=Count_Age65_plus)
        for i in range(0,Count_Age65_plus):
            Household_List_65_plus.append(House65_plus[i])
        Distribution_List = Household_List_18_to_34  + Household_List_34_to_64 + Household_List_65_plus
        Sensible_18_to_34 = SensibleHouseholds(Household_List_18_to_34)
        Sensible_34_to_64 = SensibleHouseholds(Household_List_34_to_64)
        Sensible_65_plus = SensibleHouseholds(Household_List_65_plus)
        Household_List = Sensible_18_to_34 + Sensible_34_to_64 + Sensible_65_plus
        #Because the values are decimals, we want exactly length of population_size:
        #The UK population is ageing so we remove values from the 18-34 section
        Reversed_Household_List = Household_List[::-1]
        Truncated_Reversed_Household_List = Reversed_Household_List[:population_size]
        Household_List = Truncated_Reversed_Household_List[::-1]
        #Defining Averages to be compared:
        Average_18_to_34 = sum(Sensible_18_to_34)/len(Sensible_18_to_34)
        Average_35_to_64 = sum(Sensible_34_to_64)/len(Sensible_34_to_64)
        Average_65_plus = sum(Sensible_65_plus)/len(Sensible_65_plus)
        # plt.hist(Distribution_List, bins = 20)
        # plt.hist(Household_List, bins = 20)
        return Average_18_to_34, Average_35_to_64, Average_65_plus
        

def SensibleHouseholds(Household_List_depending_on_age):
    #------------------------CHECKING WHICH VALUE IS SENSIBLE------------
    #--Counts each value in Household_List and creates a dictionary---------------------
    
    Household_Dict = dict(Counter(Household_List_depending_on_age))
    
    
    #--Checking for multiples--------------------------------------------  
         
    Not_sensible = {}
    for size in Household_Dict:
        if size != 0:
            if size == 1:
                if Household_Dict[size] % 2 != 0:
                    Not_sensible[size] = Household_Dict[size]
            else:
                if Household_Dict[size] == 1:
                    Not_sensible[size] = Household_Dict[size]
                else:
                    if Household_Dict[size] % (size+1) != 0:
                        Not_sensible[size] = Household_Dict[size]
    
    #--Sorting values of Not_sensible & Household dictionary-------------------------------------            
    SNot_List = sorted(Not_sensible.items(), key=lambda x: x[0], reverse=True)
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
                    while value % (key+1) != 0:
                        value = value - 1
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
    return New_Householdlist

#--Difference between the averages of each age bin and the theoretical one as a function of iterations
population_size_List = [100,1000,10000, 100000]
Diff_18_to_34_List = []
Diff_34_to_64_List = []
Diff_65_plus_List = []
for population_size in population_size_List:
    Average_18_to_34, Average_35_to_64, Average_65_plus = HouseholdList(population_size)
    Diff_18_to_34_List.append(abs(1.54 - Average_18_to_34))
    Diff_34_to_64_List.append(abs(1.69 - Average_35_to_64))
    Diff_65_plus_List.append(abs(0.49 - Average_65_plus))
plt.plot(population_size_List, Diff_18_to_34_List)
plt.plot(population_size_List, Diff_34_to_64_List)
plt.plot(population_size_List, Diff_65_plus_List)
plt.yscale("log")
plt.xscale("log")
plt.legend(['Diff_18_to_34', 'Diff_34_to_64', 'Diff_65_plus'], loc='best')
plt.xlabel('Population size')
plt.ylabel('Difference')
plt.title('Difference between the averages of each age bin and the theoretical one as a function of population size')
plt.show()

#--Trends of Poisson distribution and Edited Household_List:
#--Need to un-comment lines45 and 46
# population_size = 10000
# HouseholdList(population_size)
# plt.legend(['Poisson distribution', 'Adjusted Household'], loc='best')
# plt.xlabel('Household size')
# plt.ylabel('Count')
# plt.title('Comparaison of the Poisson distribution and the adjusted household list')
