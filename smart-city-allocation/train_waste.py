import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

def main():
    # Load data
    df = pd.read_csv('data/waste_clean.csv')
    
    # Features and Target based on PRD
    # Columns: area, day_of_week, population_density, last_collection_days, bin_fill_pct, overflow_risk
    features = ['area', 'day_of_week', 'population_density', 'last_collection_days', 'bin_fill_pct']
    target = 'overflow_risk'
    
    X = df[features]
    y = df[target]
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model: RandomForest
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    print("Classification Report:")
    report = classification_report(y_test, y_pred)
    print(report)
    
    # Save the model
    joblib.dump(clf, 'waste_model.pkl')
    print("Model successfully saved as waste_model.pkl")

if __name__ == "__main__":
    main()
