#-*- coding: utf-8 -*-
"""
Created on Sun Dec 12 19:27:17 2021

@author: tmdej
"""

import matplotlib.pyplot as plt



data_f = open("JejuTrafficAccident.csv", 'r', encoding="UTF-8")
conditions = []
accidents = []

for line in data_f: 
    (condition, accident) = line.split(',')       
    conditions.append(str(condition))
    accidents.append(int(accident))

print(years)
data_f.close() 
