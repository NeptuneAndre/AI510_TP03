import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from joblib import dump

# Load processed data (assuming you've stored it back into Blob Storage or locally)
data = pd.read_csv('path/to/processed/data.csv')

# Split the data into features (X) and target (y)
X = data.drop(['downtime'], axis=1)
y = data['downtime']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train a model (RandomForest in this case)
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save the model
dump(model, 'models/downtime_prediction_model.pkl')
