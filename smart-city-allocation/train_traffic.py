import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

def main():
    # Load data
    df = pd.read_csv('data/traffic_clean.csv')
    
    # Rename columns to match the specific names the user requested
    df = df.rename(columns={
        'day_of_week': 'day_enc',
        'junction': 'junction_enc',
        'weather': 'weather_enc'
    })
    
    # Features and Target
    features = ['hour', 'day_enc', 'junction_enc', 'weather_enc', 'vehicles']
    target = 'high_congestion'
    
    X = df[features]
    y = df[target]
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model: RandomForest n_estimators=100, random_state=42
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    print("Classification Report:")
    report = classification_report(y_test, y_pred)
    print(report)
    
    # Save the model
    joblib.dump(clf, 'traffic_model.pkl')
    print("Model successfully saved as traffic_model.pkl")

if __name__ == "__main__":
    main()
