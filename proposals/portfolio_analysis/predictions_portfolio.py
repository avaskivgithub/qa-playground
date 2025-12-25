from setup_portfolio import *
from excel_portfolio_data_from_yfinance import read_yfinanace_or_cached_csv
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR

'''
Class to try out different scikit-learn models by:
1. training them on one date range of the stock's prices
2. then predicting on the other date range
3. and then comparing predicted prices with the actual prices for the same date range 
'''
class Predictions():

    def __init__(self, symbol,
                 start_date_train, end_date_train,
                 start_date_prediction, end_date_prediction,
                 interval='1d'):
        
        self.symbol = symbol
        self.data = read_yfinanace_or_cached_csv(symbol, start_date_train, end_date_train, interval)
        self.data_real = read_yfinanace_or_cached_csv(symbol, start_date_prediction, end_date_prediction, interval)

        self.X, self.y = self.normalize_date_column_toordinal_return_X_Y(self.data)
        self.X_real, self.y_real = self.normalize_date_column_toordinal_return_X_Y(self.data_real)

    def normalize_date_column_toordinal_return_X_Y(self, data, y_column_name='Open'):
        # Convert Date to datetime and to numeric (ordinal)
        data['Date'] = pd.to_datetime(data['Date'])
        data['Date_ordinal'] = data['Date'].map(lambda x: x.toordinal())
        X = data[['Date_ordinal']]
        Y = data[y_column_name]

        return(X, Y)
    
    def prediction_vs_real_visualization(self, model_name, y_pred):
        
        X_test_dates = self.data_real['Date']

        # Plot
        plt.figure()
        plt.scatter(self.data_real['Date'], y_pred, s=20, edgecolor="black", c="darkorange", label="data")
        plt.xticks(rotation=90)
        plt.plot(X_test_dates, y_pred, color="cornflowerblue", label=model_name.replace(' ', ''), linewidth=2)
        plt.plot(X_test_dates, self.y_real, color="red", label="RealData", linewidth=2)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title(f"{model_name} vs Real Data")
        plt.legend()
        plt.show()

    def prediction_with_model(self, model_name, model_object):

        # Train model
        model = model_object
        model.fit(self.X, self.y)

        # Predictions
        y_pred = model.predict(self.X_real)

        # Plot
        self.prediction_vs_real_visualization(model_name, y_pred)        

    """
    https://scikit-learn.org/stable/modules/tree.html#tree
    """
    def prediction_with_decissiontree(self):
        self.prediction_with_model(model_name="Decision Tree Regression", 
                                   model_object=DecisionTreeRegressor(max_depth=3))

    """
    https://scikit-learn.org/stable/modules/kernel_ridge.html
    """
    def prediction_with_kernel_ridge(self):
        
        model = KernelRidge(kernel="rbf", alpha=1.0, gamma=1e-6)
        self.prediction_with_model(model_name="Kernel Ridge", 
                                   model_object=model)

    """
    https://scikit-learn.org/stable/modules/svm.html
    """
    def prediction_with_vector_machine(self):
        
        model = SVR(kernel="rbf", C=100, epsilon=0.1, gamma=1e-6)
        self.prediction_with_model(model_name="Vector Machine", 
                                   model_object=model)


def real_data_vizualiztion(symbol, start_date, end_date):

    data_real = read_yfinanace_or_cached_csv(symbol, start_date, end_date)
    X_real = data_real['Date'] 
    y_real = data_real['Open']

    print(X_real)
    print(y_real)

    # Plot
    plt.figure()
    plt.scatter(data_real['Date'], y_real, s=10, edgecolor="black", c="darkorange", label="data")
    plt.plot(X_real, y_real, color="red", label="real", linewidth=2)
    plt.xticks(rotation=90)
    plt.xlabel("Date")
    plt.ylabel("Open Price")
    plt.title(f"Real Data for the date range {start_date} - {end_date}")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    
    # Read data from yfinance api (or from cvs cache) and make predictions
    for symbol in portfolio_list[:1]:

        # cache data into cvs
        read_yfinanace_or_cached_csv(symbol, start, end, interval)
        read_yfinanace_or_cached_csv(symbol, start_future, end_future, interval)

        # use model to predict
        my_prediction = Predictions(symbol, 
                                    start, end, 
                                    start_future, end_future)
        my_prediction.prediction_with_decissiontree()
        my_prediction.prediction_with_kernel_ridge()
        my_prediction.prediction_with_vector_machine()

        # real_data_vizualiztion(symbol, start_future, end_future)
        # real_data_vizualiztion(symbol, start, end)