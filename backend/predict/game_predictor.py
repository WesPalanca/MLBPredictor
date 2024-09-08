import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Load the dataset
games = pd.read_csv("baseball_stats.csv", index_col=0)

# Convert date column to datetime
games["Date"] = pd.to_datetime(games["Date"])

# Process features
games["h/a"] = (games["Unnamed: 4"] == "@").astype("int")  # Home/Away indicator
games["Opp"] = games["Opp"].astype("category").cat.codes  # Opponent as a category


# Convert 'R' and 'RA' to numeric, setting errors='coerce' to handle non-numeric values
games["R"] = pd.to_numeric(games["R"], errors='coerce')
games["RA"] = pd.to_numeric(games["RA"], errors='coerce')

# Drop rows with NaNs in 'R' or 'RA'
games = games.dropna(subset=["R", "RA", "h/a", "Opp"])

# Define the target column
games["target"] = (games["W/L"] == "W").astype("int")

# Define predictors
predictors = ["h/a", "Opp", "R", "RA"]

# Split the data into training and testing sets
train = games[games["Date"] < '2022-01-01']
test = games[games["Date"] > '2022-01-01']

# Initialize and train the model
rf = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)
rf.fit(train[predictors], train["target"])

# Make predictions
preds = rf.predict(test[predictors])

# Evaluate the model
acc = accuracy_score(test["target"], preds)
print("Accuracy:", acc)

# Display detailed metrics
print("Classification Report:\n", classification_report(test["target"], preds))
print("Confusion Matrix:\n", confusion_matrix(test["target"], preds))

# Display prediction results
combined = pd.DataFrame(dict(actual=test["target"], prediction=preds))
print(combined)

joblib.dump(rf, 'game_predictor.pk1')
