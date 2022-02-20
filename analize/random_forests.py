"""
Скрипт классифицирует данные по котировкам на основе случайного леса
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
from sklearn.model_selection import train_test_split
import scipy as sp
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn import metrics
from matplotlib.legend_handler import HandlerLine2D
from sklearn.tree import export_graphviz
import graphviz

