#CCPP Data Final Project 
# Import libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# Load the dataset
#To check file path
import os

file_path = "CCPP_data.xlsx"  # Update to your actual file path
if os.path.exists(file_path):
    print("File found!")
else:
    print(f"File not found at: {file_path}")
print(os.getcwd())
print("Current Directory:", os.getcwd())
print("Files in the directory:", os.listdir())
