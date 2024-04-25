import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path):
    """Load data from a CSV file and remove the last column."""
    data = pd.read_csv(file_path)
    # data = data.iloc[:, :-1]  # Remove the last column
    return data

def preprocess_data(data):
    """Preprocess the data."""
    # Encode categorical labels into integers
    label_encoder = LabelEncoder()
    # data['label'] = label_encoder.fit_transform(data['label'])
    
    # Split features and target variable
    print(data)
    drop_cols = [f"gyro-{i+1}" for i in range(6)] + ['label']
    X = data.drop(drop_cols, axis=1)
    y = data['label']
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test

def train_logistic_regression(X_train, y_train):
    """Train logistic regression model."""
    from sklearn.ensemble import GradientBoostingClassifier
    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate the trained model."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("Classification Report:")
    print(report)

def main():
    # Load data
    file_path = "data.csv"
    data = load_data(file_path)
    
    # Preprocess data
    X_train, X_test, y_train, y_test = preprocess_data(data)
    
    # Train logistic regression model
    model = train_logistic_regression(X_train, y_train)
    
    # Evaluate model
    evaluate_model(model, X_test, y_test)
    
    # Print class labels
    print("Class Labels:", "[0, 1, 2]")

if __name__ == "__main__":
    main()
