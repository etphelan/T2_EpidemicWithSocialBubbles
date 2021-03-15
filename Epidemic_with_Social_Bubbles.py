# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 13:00:04 2021

@authors: Roseisa Weeraratne and Elise Phelan
"""

import random
from random import uniform
import math
import matplotlib.pyplot as plt 
import csv

#Infection Parameters
inf_inbub = 13         #chance of infection from someone inside bubble
inf_normal = 5         #chance of infection with no social bubbles (population in lockdown)
inf_outbub = 1         #chance of infection from someone outside bubble
gen = 4                #Days spent infected but not contagious
inc = 2                #Days spent contagious with no symptoms
sickperiod = 8         #Days spent sick
chance_recovery = 98.2 #Recovery rate
preimmune = 0
preinfected = 1

probmove = 2
list_percinf = [5]     #Says at what % infected to increase bubble size
numbubs_list = [10]    #Says what to change bubble size to
Runs = 1              #Number of trials
T_end = 80            #Number of days to run

#Define the initial states
dead = 0
immune = 1
naive = 2
infected = 3
contagious = 4
sick = 5
state = naive
daysick = 1
day = daysick
O = 1

#Initialize lists for plotting
max_newinf = []
max_derivativenewinf = []
timmax_derivativenewinf = []
runs = []
       
def createpop ():           #sorts population into bubbles
 bubnum = -1   
 for i in range (numbubs):  #creates a set number of bubbles
   n = 0
   bubnum = bubnum + 1
   bub = bubnum 
   while n < bubsize:       #puts guys into the bubbles
    if len(pop) < popsize:
      n = n + 1
      guy = [state, day, bub]   #definition of a guy
      pop.append(guy)           #adds guy to the population
    else: n = bubsize
     
def bub ():
      bubbles.clear()
      bubnum = 0
      p = 0
      while p < numbubs:
       bub = bubnum
       bubbles.append(bub)
       bubnum = bubnum + 1
       p = p + 1
      return bubbles
      
         
def search (i, num):
        if i == num:
            return True
            
def get_guy(pop, n):    #pulls a guy from the population to look at       
    my_guy = pop[n]
    return (my_guy)

def countinfectious():  #creates a list of all the infectious people in each bubble on a day
    numinf_inbubs = []
    for j in range (numbubs):
        z = 0
        for guy in pop:     #scans through population for contagious/sick
            if guy[2] == j:
                if guy[0] == contagious:
                    z = z + 1
                elif guy[0] == sick:
                    z = z + 1
        numinf_inbubs.append(z)
    return(numinf_inbubs)

def sweep():                                #pulls guys from population to process them and change their states
    global inf_outbub, totinf1
    print("inf_outbub=", inf_outbub)
    print("inf_inbub=", inf_inbub)
    for i in range (len(pop)):
        my_guy = pop[i]                     #when my_guy is updated, he gets updated in the population list too
        if my_guy[0] == immune:             #if immune, increase day counter
                my_guy[1] = my_guy[1] + 1
                
        elif my_guy[0] == infected:        
            if my_guy[1] < gen: 
                my_guy[1] = my_guy[1] + 1   #increase day counter
            else:
                my_guy[0] = contagious      #otherwise guy becomes contagious if past the generation period
                my_guy[1] = 1 
                
        elif my_guy[0] == contagious:
            if my_guy[1] < inc:
                day = my_guy[1]
                my_guy[1] = day + 1         #increase day counter
            else: 
                my_guy[0] = sick            #otherwise guy becomes sick if past the incubation period
                my_guy[1] = 1
                
        elif my_guy[0] == naive:
            NewInfection = False
            bubblenumber = my_guy[2]
            p = 0                                        
            while p < numinf_inbubs[bubblenumber] and NewInfection == False:  #for every contagious person in guy's bubble
                c = 100*random.random()             #roll dice for infection
                p = p + 1
                if c < inf_inbub:                   #if random number c is less than chance of infection, guy becomes infected
                    totinf1 = totinf1 + 1
                    NewInfection = True
                    my_guy[0] = infected
                    my_guy[1] = 1                   #day counter for days spent infected goes to 1
 
            f = 0                                   #initiate counter
            while f < max_contact and NewInfection == False:            #repeats for every person outside of bubble contacted
                c = random.randint(0,len(pop)-1)
                tempguy = pop[c]                    #selects random person from population
                d = 100*random.random()             #roll dice for infection
                if tempguy[0] == contagious:        #checks for infection if random guy selected is contagious or sick
                    if d < inf_outbub:
                        my_guy[0] = infected
                        NewInfection = True         #if random number, d, is less than chance of infection from out of bubble, guy becomes infected
                        my_guy[1] = 1
                if tempguy[0] == sick:
                    if d < inf_outbub:
                        my_guy[0] = infected
                        NewInfection = True
                        my_guy[1] = 1
                f = f + 1
                   
            if NewInfection == False:                #if my_guy is not infected, increase day counter
                my_guy[1] = my_guy[1] + 1
            #else: 
                #print('NewInfection Occurred')
            
        elif my_guy[0] == sick:
            if my_guy[1] < sickperiod: 
                my_guy[1] = my_guy[1] + 1    #increase day counter if less than sickperiod
            else:
               d = 100*random.random()    #roll dice for recovery
               if d > chance_recovery:
                  my_guy[0] = dead
               else:                      #if guy survives, chance state to immune and start immune day counter at 1
                  my_guy[0] = immune
                  my_guy[1] = 1 
          

def move():          #moves guy from bubble to bubble
 global probmove
 try:
  q = numbubs - 1
  e = 100/q
  s = 0
  rangenum = []
  bubbles = bub()
  rangenum.append(s)
  #print (bubbles)
  #print(pop)
  for guy in pop:       
    t = uniform(1, 100) 
    #print("t=", t)
    if t<=probmove:  
        #print(guy[2])
        #print("yes")
        bubbles.remove(guy[2])
        while len(rangenum) < numbubs:
            s = s + e
            rangenum.append(s)
        w = uniform(1,100)
        c = 0
        a = 0
        b = 1
        end1 = rangenum[a] 
        end2 = rangenum[b] 
        while c < q :
          if w >= end1 and w < end2:
           guy[2] = bubbles[c]
           c = q
          else:
           a = a + 1 
           b = b + 1
           c = c + 1
           end1 = rangenum[a]
           end2 = rangenum[b]
    bubbles = bub()
    #print(pop)
 except ZeroDivisionError:
     pass

    
def counting ():
    number_of_guys = []
    for l in bubbles:
        h = 0
        for guy in pop:
              if search(guy[2], l):
                  h = h + 1
        number_of_guys.append(h) 
        #print(number_of_guys)
    return number_of_guys

def avgcounting():
    number_of_guys = counting()
    #print("counting = ", number_of_guys)
    Average = sum(number_of_guys) / len(number_of_guys)
    avgcount.append(Average)
    #print ("avgcount = ", avgcount)
    return avgcount

def reorganize():
    newpop = []
    for i in bubbles:
        for guy in pop:
            if search(guy[2], i):
                newpop.append(guy)
    print ("newpop = ", newpop)
    return (newpop)

def newbub():
  global v, numbubs
  percinf = percentinfected()
  if v < len(list_percinf):
   if percinf >= list_percinf[v]:   
    try:
     while percinf >= list_percinf[v]:  
      newpopbub = reorganize()
      numbubs = numbubs_list[v]
      bubsize = math.ceil(popsize / numbubs)
      bubnum = 0
      b = bubsize
      k = 0
      a = bubsize*k
      b = a + bubsize 
      for s in range (numbubs):
       for o in range (a, b):
         try:  
          guy = newpopbub[o]
          guy[2] = bubnum 
          newpopbub[o] = guy
          print ("updated guy =", guy)
         except IndexError:
             pass
       k = k + 1
       a = bubsize*k
       b = a + bubsize
       bubnum = bubnum + 1
      pop = newpopbub
      print ("newpopbub = ", pop)
      bub()
      v = v + 1 
    except IndexError:
        pass
    
def percentinfected ():             #calculates the percent of the population that is infected for each day
    global totinf
    percinf = (totinf/popsize) *100
    print("percinf =", percinf)
    return(percinf)

def summarize ():                   #totals the number of people in each state for plotting
    global totinf, newlyinfected
    global naive0, dead0
    naive0 = 0
    infected0 = 0
    sick0 = 0
    dead0 = 0
    immune0 = 0
    for guy in pop:                 #scans through population and counts guys in each state
        #my_guy = get_guy(pop, n)
        if guy[0] == 2: naive0 = naive0 + 1
        elif guy[0] == 3:infected0 = infected0 + 1
        elif guy[0] == 4: infected0 = infected0 + 1
        elif guy[0] == 5: sick0 = sick0 + 1
        elif guy[0] == 0: dead0 = dead0 + 1
        elif guy[0] == 1: immune0 = immune0 + 1
        if guy[0] == 3:             #counts the total number of new infections for that day
            if guy[1] == 1: 
                totinf = totinf + 1
                newlyinfected = newlyinfected + 1
    totinf_list.append(totinf)
    print ("totinf list =", totinf_list)
    imm.append(immune0)             #appends the totals to lists for plotting
    inf.append(infected0)
    ded.append(dead0)
    nai.append(naive0)
    tim.append(T)
    newinf.append(newlyinfected)
    newlyinfected = 0
    print('day =', T,'immune =', immune0, 'infected =', infected0, 'dead =', dead0, 'naive =', naive0)
    return imm, inf, ded, nai, tim, totinf_list, newinf

def derivativenewinf ():
    derivativenewinf_list = []
    a = 0
    b = 1
    c = 0
    end1 = newinf[a]
    end2 = newinf[b]
    try:
     while c < len(newinf): 
        derivative = end2 - end1
        derivativenewinf_list.append(derivative)
        a = a + 1
        b = b + 1
        c = c + 1
        end1 = newinf[a]
        end2 = newinf[b]
    except IndexError: 
         pass
    return derivativenewinf_list

f = open('1inf_bubsize_data.csv', 'w', newline='')    #open csv file for data
writer = csv.writer(f,delimiter=',')
writer.writerow(['max_newinf', 'max_derivativenewinf', 'Time of max_derivativenewinf', 'naive', 'dead', 'day']) #make data labels

run = 0                     #initialize run counter

while run < Runs:     #repeats for 'runs' trials
 popsize = 3000       #puts population into bubble sizes of 1 initilially, population in lockdown
 numbubs = 3000
 bubsize = math.ceil(popsize/numbubs)

 imm=[]             #initialize lists
 inf=[]
 ded=[]
 nai=[]
 tim=[]
 rangenum = []
 number_of_guys = []
 pop = []
 bubbles = []
 avgcount = [] 
 totinf_list = []
 bubbles = []
 percinf0 = []
 newinf = []
 
 totinf = 0

 createpop()        #creates the population and sorts them into bubbles
 bub()
 initial_counting = counting()
 print("initial counting =", initial_counting)
 percinf = percentinfected()        #calculates the percent infected
 percinf0.append(percinf)
 
 v = 0
 T = 0
 numinf_inbubs = countinfectious()
 max_contact = 10               #set the number of contacts outside of bubble
 newlyinfected = 1

 for k in range (preinfected):  #for every preinfected person, it pulls a random person from the populatio and infects them
    r = random.randint(0,len(pop)-1)        
    my_guy = get_guy(pop, r)            #draws random number and gets that guy
    my_guy[0] = 3
    pop[r] = my_guy             #puts guy back into the population
    
    
 while T < T_end:               #sets how many days to run
    summarize()
    numinf_inbubs = countinfectious()
    totalinf = sum(numinf_inbubs)
    print(popsize)
    print(numbubs)
    if popsize == numbubs:      #when the population is not in bubbles, use a different infection rate
        inf_outbub = inf_normal
    else:                       #if population is in bubbles, use the infection rates for inside/outside bubbles
        inf_outbub = 1
    sweep()             
    move()
    print ("run=", run,"Time = ",T)
    counting()
    bubbles = bub()
    #print("bubbles = ", bubbles)
    newbub()
    avgcounting()
    percinf = percentinfected()     #calculate % of the population infected and add to the list
    percinf0.append(percinf)
    T = T + 1                       #advance the day counter
 
 
 avgcount = avgcounting()
 imm, inf, ded, nai, tim, totinf_list, newinf = summarize()
 derivativenewinf_list =  derivativenewinf()

 print("newinf=", newinf)
 print("derivativenewinf_list", derivativenewinf_list)
 
 maxnewinf = max(newinf)
 max_newinf.append(maxnewinf)
 maxderivativenewinf = max(derivativenewinf_list)
 print('maxderivativenewinf=', maxderivativenewinf)
 max_derivativenewinf.append(maxderivativenewinf)
 timmaxderivativenewinf = derivativenewinf_list.index(max(derivativenewinf_list))
 timmax_derivativenewinf.append(timmaxderivativenewinf + 2)

 ####Plot the data
 #Plots bubble size and new infections per day as a function of time
 plt.plot (tim, avgcount, color= 'b', label= 'Number of Guys in Each Bubble')
 plt.xlabel("Time (Days)")
 plt.ylabel("Number of Guys")
 plt.plot(tim, newinf, label="Number of New Infections Each Day", color= 'r')
 plt.legend()
 plt.show()

#Plots the number of guys in each state as a function of time
 plt.plot(tim, imm, label='Immune')
 plt.plot(tim, inf, label='Infected')
 plt.plot(tim, ded, label='dead')
 plt.plot(tim, nai, label='naive')
 plt.legend()
 plt.xlabel("Time (Days)")
 plt.ylabel("Number of Guys")
 plt.show()
 
#Plots the infection rate and the derivative of the infection rate
 derivativenewinf_list.append(0)
 #plt.plot(tim, totinf_list, label='Total Infection')
 plt.plot(tim, derivativenewinf_list, label='Rate of New Infections Each Day')
 plt.plot(tim, newinf, label='Infections Each Day')
 plt.legend()
 plt.xlabel("Time (Days)")
 plt.ylabel("Number of Guys")
 plt.show()
 
 runs.append(O)         #advances the run counter
 run = run + 1
                
 writer.writerow([max_newinf[-1], max_derivativenewinf[-1], timmax_derivativenewinf[-1], naive0, dead0, T])  #add data to the csv file

#Prints the data that is recorded on the csv file
print('runs=', runs)
print('max_newinf=', max_newinf)
print('max_derivativenewinf=', max_derivativenewinf)
print('timmax_derivativenewinf =', timmax_derivativenewinf)

f.close()            #closes the csv file