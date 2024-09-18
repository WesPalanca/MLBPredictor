import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
import joblib

# Load the dataset
games = pd.read_csv("baseball_stats.csv", index_col=0)

# Convert date column to datetime
games["Date"] = pd.to_datetime(games["Date"])

# Feature Engineering: Home/Away indicator, Team and Opponent categories
games["h/a"] = (games["Unnamed: 4"] == "@").astype("int")
games["Opp"] = games["Opp"].astype("category").cat.codes
games["Tm"] = games["Tm"].astype("category").cat.codes

# Extract wins and losses
games["Wins"] = pd.to_numeric(games["W-L"].str.split('-').str[0], errors='coerce')
games["Losses"] = pd.to_numeric(games["W-L"].str.split('-').str[1], errors='coerce')
games["Rank"] = pd.to_numeric(games["Rank"], errors='coerce')


# Drop rows with missing data
games = games.dropna(subset=["Tm", "Rank", "h/a", "Opp", "Wins", "Losses"])

# Define the target column
games["target"] = (games["W/L"] == "W").astype("int")

# Predictors including the new features
predictors = ["Tm", "Rank", "h/a", "Opp", "Wins", "Losses"]

# Split the data into training and testing sets
train = games[games["Date"] < '2022-04-01']
test = games[games["Date"] > '2022-04-01']

# Address class imbalance by upsampling the minority class
train_majority = train[train["target"] == 0]
train_minority = train[train["target"] == 1]

train_minority_upsampled = resample(train_minority, 
                                    replace=True,     # sample with replacement
                                    n_samples=len(train_majority),    # to match majority class
                                    random_state=1)  # reproducible results

train_balanced = pd.concat([train_majority, train_minority_upsampled])

# Feature scaling: Normalize continuous variables
scaler = StandardScaler()
train_balanced[predictors] = scaler.fit_transform(train_balanced[predictors])
test[predictors] = scaler.transform(test[predictors])

# Define parameter grid for GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300, 500],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'class_weight': ['balanced', None]
}

# Initialize GridSearchCV
grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=1),
                           param_grid=param_grid,
                           scoring='accuracy',
                           cv=5,
                           verbose=2,
                           n_jobs=-1)

# Fit GridSearchCV
grid_search.fit(train_balanced[predictors], train_balanced["target"])

# Print best parameters and best score
print("Best parameters found: ", grid_search.best_params_)
print("Best cross-validation score: ", grid_search.best_score_)

# Use the best estimator
best_rf = grid_search.best_estimator_

# Evaluate the best model on the test set
preds_best = best_rf.predict(test[predictors])
acc_best = accuracy_score(test["target"], preds_best)
print("Best model accuracy:", acc_best)
print("Classification Report:\n", classification_report(test["target"], preds_best))
print("Confusion Matrix:\n", confusion_matrix(test["target"], preds_best))

# Save the trained model
joblib.dump(best_rf, 'best_game_predictor.pkl')
