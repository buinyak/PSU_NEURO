# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:24:56 2021

@author: AM4
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# загружаем и подготавляваем данные
df = pd.read_csv('data.csv')

df = df.iloc[np.random.permutation(len(df))]
y = df.iloc[0:100, 4].values
y = np.where(y == "Iris-setosa", 1, -1)
X = df.iloc[0:100, [0, 2]].values


inputSize = X.shape[1] # количество входных сигналов равно количеству признаков задачи 
hiddenSizes = 10 # задаем число нейронов скрытого (А) слоя 
outputSize = 1 if len(y.shape) else y.shape[1] # количество выходных сигналов равно количеству классов задачи


# создаем матрицу весов скрытого слоя
Win = np.zeros((1+inputSize,hiddenSizes)) 
# пороги w0 задаем случайными числами
Win[0,:] = (np.random.randint(0, 3, size = (hiddenSizes))) 
# остальные веса  задаем случайно -1, 0 или 1 
Win[1:,:] = (np.random.randint(-1, 2, size = (inputSize,hiddenSizes))) 

#Wout = np.zeros((1+hiddenSizes,outputSize))

# случайно инициализируем веса выходного слоя
Wout = np.random.randint(0, 2, size = (1+hiddenSizes,outputSize)).astype(np.float64)
   
# функция прямого прохода (предсказания) 
def predict(Xp):
    # выходы первого слоя = входные сигналы * веса первого слоя
    hidden_predict = np.where((np.dot(Xp, Win[1:,:]) + Win[0,:]) >= 0.0, 1, -1).astype(np.float64)
    # выходы второго слоя = выходы первого слоя * веса второго слоя
    out = np.where((np.dot(hidden_predict, Wout[1:,:]) + Wout[0,:]) >= 0.0, 1, -1).astype(np.float64)
    return out, hidden_predict


# обучение
# у перцептрона Розенблатта обучаются только веса выходного слоя 
# как и раньше обучаем подавая по одному примеру и корректируем веса в случае ошибки
eta = 0.01
WoutOld =  np.random.randint(0, 2, size = (1+hiddenSizes,outputSize)).astype(np.float64)
while True:
    for xi, target, j in zip(X, y, range(X.shape[0])):
        pr, hidden = predict(xi) 
        Wout[1:] += ((eta * (target - pr)) * hidden).reshape(-1, 1)
        Wout[0] += eta * (target - pr)
    y = df.iloc[:, 4].values
    y = np.where(y == "Iris-setosa", 1, -1)
    X = df.iloc[:, [0, 2]].values
    pr, hidden = predict(X)
    result1 = sum(pr-y.reshape(-1, 1))
    result2 = sum(Wout-WoutOld.reshape(-1,1))
    if(result1 == 0 or result2 == 0):
        break
    WoutOld = Wout
    
    
        
# посчитаем сколько ошибок делаем на всей выборке


# далее оформляем все это в виде отдельного класса neural.py
