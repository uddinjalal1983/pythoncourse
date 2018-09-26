
# coding: utf-8

# In[1]:

import math
import unittest
import numpy as np
import requests as r


# In[2]:

def exercise01():
    # Create a list called animals containing the following animals: cat, dog, crouching tiger, hidden dragon, manta ray

    # ------ Place code below here \/ \/ \/ ------
    
    animals = ["cat", "dog", "crouching tiger", "hidden dragon", "manta ray"]

    # ------ Place code above here /\ /\ /\ ------

    return animals


# In[3]:

def exercise02():
    # Repeat exercise 1 and loop through and print each item in the animal list by iterating through an index number and using range(). 
    #Set the variable len_animals to the length of the animal list.

    # ------ Place code below here \/ \/ \/ ------
    
    animals = ["cat", "dog", "crouching tiger", "hidden dragon", "manta ray"]
    len_animals = len(animals)
    for i in range(len_animals):
        print(animals[i])
    
    # ------ Place code above here /\ /\ /\ ------

    return animals, len_animals


# In[4]:

def exercise03():
    # Reorganize the countdown list below in descending order and return the value of the 5th element in the countdown list
    countdown = [9, 8, 7, 5, 4, 2, 1, 6, 10, 3, 0, -5]
    the_fifth_element = -999

    # ------ Place code below here \/ \/ \/ ------
    
    countdown = sorted(countdown, reverse=True)
    countdown[4] = -999


    # ------ Place code above here /\ /\ /\ ------

    return countdown, the_fifth_element


# In[5]:

def exercise05(n):
    # This function will find n factorial using recursion (calling itself) and return the solution. For example exercise05(5) will return 120. No Python functions are to be used.

    # ------ Place code below here \/ \/ \/ ------
    
    factorial=1
    while(n>0):
        factorial=factorial*n
        n=n-1
    print(factorial)
  
    # ------ Place code above here /\ /\ /\ ------


# In[6]:

def exercise07(n):
    # This function looks for duplicates in list n. If there is a duplicate False is returned. If there are no duplicates True is returned.

    # ------ Place code below here \/ \/ \/ ------
    result = []    
    if len(n) == len(set(n)):
        return True
    return False

    # ------ Place code above here /\ /\ /\ ------


# In[ ]:



