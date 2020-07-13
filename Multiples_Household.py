import networkx as nx
import random
import scipy.stats as stats
import operator
#---------------------------------PARAMETERS--------------------
population_size = 10

#--------------------------------DEFINING INITIAL HOUSELHOLD LIST----
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
    
#------------------------CHECKING WHICH VALUE IS SENSIBLE------------
#--Transforms the Household_list as a dictionary---------------------

Unique_elements = []
Household_Dict = {}
for size in Household_List:
    if size not in Unique_elements:
        Unique_elements.append(i)
        Count = 0
        for value_to_check in Household_List:
            if size == value_to_check:
                Count += 1
        Household_Dict[size] = Count
        
print(Household_Dict)

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
            if Household_Dict[size] % size == 0:
                b = (size, "is sensible")
                Checking_multiples.append(b)
                Sensible[size] = Household_Dict[size]
            else:
                Not_sensible[size] = Household_Dict[size]

#Sorting values of Not_sensible & Sensible dictionary              
SNot_List = sorted(Not_sensible.items(), key=lambda x: x[0], reverse=True)
Sorted_Household =  sorted(Household_Dict.items(), key=lambda x: x[0])



credit = 0
newpairs = []
i = 1

for pair in SNot_List:
    key = pair[0]
    value = pair[1] + credit
    credit = 0
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
        if value % key != 0:
            #for the pair with the largest value, deduce value until satisfy divisibility condition
            #If houselhold size none sensible is 1 then deduce 1 to value and give it to 0's value
            #For maximum value of key, get credit 
            i = 1
            while value % key != 0:
                value = value-1
                credit = key * i
                i += 1
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
           
 
    

#-----------Adding sensible pairs-------------------------------------
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
    

            
print("NEWPAIRS ARE", sorted(newpairs))
