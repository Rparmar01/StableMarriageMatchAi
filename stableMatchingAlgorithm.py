#To draw pictures ->May replace with graph file code instead
%matplotlib inline 
import matplotlib.pyplot as plt
import seaborn as sns

#For Random input generation
import random


#For Graph generation
import networkx as nx
from networkx import bipartite    

matchedMaleList = [] #Men who have matched with a woman
unmatchedMaleList = [] #Men who are still single
matchedFemaleList = [] #Women who have been matched with a man
matchingList = [] #Matches that are set up, but have not been confirmed as final
rankingsOfMen = [] #Rankings of men made by women
rankingsOfWomen = [] #Rankings of women made by men

def takeInput():
    try:
        menInput = (input("What are the names of all the men being matched?"))
        if not all(x.isalpha or x == "" for x in  menInput):
            raise ValueError("Something other than a list of names was provided") 
        men = menInput.split(",")
        
        womenInput = (input("What are the names of all the women being matched?"))
        if not all(y.isalpha or y == "" for y in  womenInput):
            raise ValueError("Something other than a list of names was provided") 
        women = womenInput.split(",")
     
        print()
        print("Now for rankings.")
        print()
        
        for man in men:
            print("For: ", man)
            preferences = input("Preference ranking: ")
            rankingsOfWomen[man] = preferences.split(",")
            print()
            
        for woman in women:
            print("For: ", woman)
            preferences = input("Preference ranking: ")
            rankingsOfMen[woman] = preferences.split(",")
            print()
                                
        totalPeople = len(men) + len(women)
        print("Then there are {} people total".format(totalPeople))
        
    except TypeError: #ValueError
        print("Invalid input was provided. Please try again")

def match(man):
    for woman in rankingsOfWomen[man]:
        womansMatches = []
        for found in matchingList:
            if woman in found:
                womansMatches.append(found)
        foundMan = womansMatches[0][0]
        if len(womansMatches) != 0:
            foundManRank = rankingsOfMen[woman].index(foundMan)
            for i in rankingsOfMen[woman].index(man):
                if(foundManRank >= i):
                    unmatchedMaleList.append(foundMan)
                    unmatchedMaleList.remove(foundMan)
                    womansMatches[0][0] = foundMan
                    break
        else:
            matchingList.append([foundMan, woman])
            unmatchedMaleList.remove(foundMan)
                
    
#using the lists to make bipartite graphs
B = nx.Graph()
B.add_nodes_from(matchedMaleList, bipartite=0) #List of men Add the node attribute "bipartite"
B.add_nodes_from(matchedFemaleList, bipartite=1) #List of women
B.add_edges_from(matchingList) #List of pairings between men and women

# Separate by group
l, r = nx.bipartite.sets(B)
pos = {}

# Update position for node from each group
pos.update((node, (1, index)) for index, node in enumerate(l))
pos.update((node, (2, index)) for index, node in enumerate(r))

#Setting the figure size
fig=plt.figure(figsize=(10,12))
ax = fig.add_subplot(2,1,1)
ax.set_title("Bipartite Plot")
nx.draw(B, pos=pos, ax=ax,with_labels=True, node_color=['pink','pink','pink','pink','yellow','yellow','yellow'])


plt.show()

def main():
    #Take in user input for names of men, women, and their respective rankings
    takeInput()
    
    #add men to the singles list 
    for man, women in rankingsOfWomen.items():
        unmatchedMaleList.append(man)
    
    #Start matching process for each unmatched man
    while len(unmatchedMaleList) != 0:
        for man in unmatchedMaleList:
            match(man)
    


main()
