
import scipy.stats as stats
from collections import Counter

#---------------------------------PARAMETERS--------------------
population_size = 100

#--------------------------------DEFINING INITIAL HOUSEHOLD LIST----
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

# SNot_List = [(4, 2), (2, 2), (1, 3)]
# print("TO TWEAK", SNot_List)
# Sorted_Household = [(0, 3), (1, 3), (2, 2), (4, 2)]
# print("SORTED IS ", Sorted_Household)

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

for n in newpairs:
    if n[1] == 0:
        newpairs.remove(n)
    

#--Transforming List of pairs into list of integers---------------------------      

New_Householdlist = []
for pair in newpairs:
    i = 0
    while i < pair[1]:
        New_Householdlist.append(pair[0])
        i += 1


print(newpairs)
