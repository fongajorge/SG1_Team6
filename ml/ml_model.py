import numpy as np

class linear_regression:
    """
    A custom implementation of Multiple Linear Regression using Gradient Descent.
    """
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.lr = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = None
        self.cost_history = [] # Useful for visualizing the training process later

    def fit(self, X, y):
        """
        Trains the model using the provided features (X) and target (y).
        X: numpy array of shape (n_samples, n_features) - e.g., Temp, Humidity, Clouds
        y: numpy array of shape (n_samples,) - e.g., Solar Generation kW
        """
        n_samples, n_features = X.shape
        
        # Initialize weights and bias to zero
        self.weights = np.zeros(n_features)
        self.bias = 0

        # Gradient Descent Loop
        for i in range(self.iterations):
            # 1. Hypothesis: Calculate predictions with current weights
            y_predicted = np.dot(X, self.weights) + self.bias
            
            # 2. Calculate the gradients (derivatives)
            # dw = (1/n) * X.T * (y_predicted - y)
            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / n_samples) * np.sum(y_predicted - y)
            
            # 3. Update the weights and bias
            self.weights -= self.lr * dw
            self.bias -= self.lr * db
            
            # 4. Track the cost for the report deliverables
            if i % 100 == 0:
                cost = (1 / (2 * n_samples)) * np.sum((y_predicted - y) ** 2)
                self.cost_history.append(cost)

    def predict(self, X):
        """
        Predicts the output for new input data.
        X: numpy array of shape (n_samples, n_features)
        """
        return np.dot(X, self.weights) + self.bias

class scaler:
    """
    A custom implementation of Z-score normalization (Standardization).
    Brings all features to a mean of 0 and standard deviation of 1.
    """
    def __init__(self):
        self.mean = None
        self.std = None

    def fit_transform(self, X):
        """
        Calculates the mean and standard deviation, then scales the data.
        Use this on your TRAINING data.
        """
        # Calculate mean and standard deviation for each column (feature)
        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)
        
        # Prevent division by zero just in case a feature never changes
        self.std[self.std == 0] = 1e-8 
        
        # Standardize: (X - mean) / std
        return (X - self.mean) / self.std

    def transform(self, X):
        """
        Scales new incoming data using the already calculated mean and std.
        Use this in your SIMULATION when predicting new hours.
        """
        if self.mean is None or self.std is None:
            raise ValueError("Scaler has not been fitted yet!")
        
        return (X - self.mean) / self.std
    

