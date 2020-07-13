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
#--Transforms the Household_list in a dictionary---------------------

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

#Sorting values of Not_sensible dictionary              
Max_value = max(Not_sensible.items(), key=operator.itemgetter(0))[0] 
SNot_List = sorted(Not_sensible.items(), key=lambda x: x[0], reverse=True)
#Take the 1st not snesible key
print("TO TWEAK", SNot_List)
Sorted_Household =  sorted(Household_Dict.items(), key=lambda x: x[0])
print("SORTED ALL LIST", Sorted_Household)
Sensible_List = sorted(Sensible)
print("SENSIBLE DICT", Sensible)
print("SENSIBKE IS ", Sensible_List)


# SNot_List = [(3, 2), (2, 3)]
# SHousehold = [(0, 4), (1, 2), (2, 3), (3, 2)]
# print("SORTED ALL LIST", SHousehold)
# print("TO TWEAK", SNot_List)

credit = 0
newpairs = []
i = 1
for pair in SNot_List:
    
    key = pair[0]
    value = pair[1]
    
    #for the pair with the largest value, deduce value until satisfy divisibility condition
    #If houselhold size none sensible is 1 then deduce 1 to value and give it to 0's value
    if key == 1:
        value = value + credit
        print("HELLO")
        if value % 2 != 0:
            print("HELLO2")
            print("MY VALUE IS", value)
            value = value - 1
            Value_0 = Sorted_Household[0][1] + 1
            newpairs.append((Sorted_Household[0][0], Value_0))
            newpairs.append((Sorted_Household[1][0], value))
            print("3!",newpairs)
        else:
            newpairs.append((key, value))
            print("!2",newpairs)

    else:

        #For maximum value of key, get credit 
        if pair == SNot_List[0]:
            while value % key != 0:
                if value < key:
                    value = value-1
                    print("Value is", value)
                    credit = key * i
                    i += 1

            print("THE FIRST PAIR BECOMES", key, value)
            newpairs.append((key, value))
            print("NEWLIST", newpairs)
            if credit != 0:
                for pair in Sorted_Household:
                    if pair[0] == 1:
                        value = pair[1] + credit
                        if value % 2 != 0:
                            print("HELLO2")
                            print("MY VALUE IS", value)
                            value = value - 1
                            Value_0 = Sorted_Household[0][1] + 1
                            # newpairs.append((SHousehold[0][0], Value_0))
                            # newpairs.append((SHousehold[1][0], value))
                            print("!1",newpairs)
                        else:
                            newpairs.append((Sorted_Household[0][0], Sorted_Household[0][1]))
                            newpairs.append((Sorted_Household[1][0], value))
                            print("!",newpairs)
                            
            print("FINISH HERE?")
        else:    
            #for second value 
            if key != SNot_List[0][0]:
                value = value + credit
                credit = 0
                while value % key != 0:
                    if value < key:
                        value = value-1
                        credit += 1

                print("THE SECOND PAIR BECOME", key, value)
                newpairs.append((key, value))
                print("NEWLIST", newpairs)
                print("OR HERE?")
    

print("Sorted Household", Sorted_Household)

i = 0
while i < len(Sorted_Household):
    a = Sorted_Household[i][0]
    print(a)
    j = 0
    for x in newpairs:
        m = x[0]
        if a == m :
            j = 1
    if j == 0:
        newpairs.append(Sorted_Household[i])
    i += 1
    

            
print("NEWPAIRS ARE", newpairs)







































