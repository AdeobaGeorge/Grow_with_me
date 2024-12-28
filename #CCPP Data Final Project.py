#CCPP Data Final Project 
# Import libraries
# #This is a regression task (predicting a continuous target variable)I'm gonna name that PE
#Linear Regression and random forest regressor will help compare performance (algorithms i'm going to use)
#CROSS VALIDATION!!!!!!
#The evaluation metrics will be Mean absolute error and root mean squared error.
#END GOAL is to calculate MAE and RMSE to evaluate performance
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

print("Files in the directory:", os.listdir())
data = pd.read_excel("CCPP_data.xlsx")  # Replace with the actual file name

#ran into a bit of a problem, I didn't realize that there were 3 sheets lol. Will specify sheets
data = pd.read_excel("CCPP_data.xlsx", sheet_name= 'CCPP_data')
print(data.head())  # Quick check of the data
print(data.columns) #quick check to get the naming right 



# Step 1: Preprocessing
# Checking for missing values
print("Missing values per column:\n", data.isnull().sum())

# Splitting features and target
X = data[['AT', 'AP', 'RH', 'V']]  #T is temperature, AP: Ambient pressure, RH: Relative humidity, V: Vacuum
y = data['PE']  # Net hourly electrical output (the target)

# Feature scaling (Standardizing the features)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Splitting data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 2: Model Building and Validation
# Initialize models
lr_model = LinearRegression()  # Linear Regression
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)  # Random Forest Regressor

# 5-Fold Cross-Validation for Linear Regression
lr_cv_scores = cross_val_score(lr_model, X_train, y_train, scoring='neg_mean_absolute_error', cv=5)
lr_mean_cv_score = -np.mean(lr_cv_scores)

# 5-Fold Cross-Validation for Random Forest
rf_cv_scores = cross_val_score(rf_model, X_train, y_train, scoring='neg_mean_absolute_error', cv=5)
rf_mean_cv_score = -np.mean(rf_cv_scores)

# Display Cross-Validation Results
print(f"Linear Regression CV MAE: {lr_mean_cv_score:.3f}")
print(f"Random Forest CV MAE: {rf_mean_cv_score:.3f}")

# Step 3: Train Final Model on Full Training Set
best_model = rf_model if rf_mean_cv_score < lr_mean_cv_score else lr_model
best_model.fit(X_train, y_train)

# Step 4: Evaluate Final Model
y_pred = best_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Display Final Evaluation
print("\nFinal Model Evaluation:")
print(f"Mean Absolute Error (MAE): {mae:.3f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.3f}")

# Step 5: Feature Importance (for Random Forest)
if isinstance(best_model, RandomForestRegressor):
    feature_importances = best_model.feature_importances_
    features = X.columns
    plt.barh(features, feature_importances, color='skyblue')
    plt.xlabel("Feature Importance")
    plt.ylabel("Feature")
    plt.title("Feature Importance in Random Forest Model")
    plt.show()

# Step 6: Save Results and Prepare for Presentation
# Save predictions to an Excel file because why not
predictions = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
predictions.to_excel("predictions.xlsx", index=False)
print("Predictions saved to 'predictions.xlsx'")

#When runniong the code make sure that your excel file is the in the same directory as whatever you are using to run python
#Completed at 12:04AM on 12/27/2024
