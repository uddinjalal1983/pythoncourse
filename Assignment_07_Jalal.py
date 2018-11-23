# core
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ml
from sklearn import datasets as ds
from sklearn import linear_model as lm
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.model_selection import train_test_split as tts


# infra
import unittest


# ------ Place code below here \/ \/ \/ ------
# import plotly library and enter credential info here

import plotly.plotly as py
import plotly.graph_objs as go
import plotly

plotly.tools.set_credentials_file(username='uddinmdj1983', api_key='ZoiWeNSuPALRFzBa1Fwl')




# ------ Place code above here /\ /\ /\ ------










# ------ Place code below here \/ \/ \/ ------
# Load datasets here once and assign to variables iris and boston


iris = ds.load_iris()
boston = ds.load_boston()


# ------ Place code above here /\ /\ /\ ------








# 10 points
def exercise01():
    '''
        Data set: Iris
        Return the first 5 rows of the data including the feature names as column headings in a DataFrame and a separate Python list containing target names
    '''


    # ------ Place code below here \/ \/ \/ ------

    df_first_five_rows = pd.DataFrame(iris['data'][:5])
    target_names = iris['target_names'][:5]

    # ------ Place code above here /\ /\ /\ ------


    return df_first_five_rows, target_names


# 15 points
def exercise02(new_observations):
    '''
        Data set: Iris
        Fit the Iris dataset into a kNN model with neighbors=5 and predict the category of observations passed in argument new_observations. Return back the target names of each prediction (and not their encoded values,i.e. return setosa instead of 0).
    '''


    # ------ Place code below here \/ \/ \/ ------

    knn = KNN(n_neighbors=5)
    knn.fit(iris['data'],iris['target'])
    iris_predictions = [iris['target_names'][x] for x in knn.predict(new_observations)]

    # ------ Place code above here /\ /\ /\ ------




    return iris_predictions


# 15 points
def exercise03(neighbors,split):
    '''
        Data set: Iris
        Split the Iris dataset into a train / test model with the split ratio between the two established by 
        the function parameter split.
        Fit KNN with the training data with number of neighbors equal to the function parameter neighbors
        Generate and return back an accuracy score using the test data was split out

    '''
    random_state = 12


    


    # ------ Place code below here \/ \/ \/ ------

    X_train, X_test, y_train, y_test = tts(iris['data'], iris['target'], test_size=1-split,random_state=random_state)
    knn = KNN(n_neighbors=neighbors)
    knn.fit(X_train,y_train)
    knn_score = knn.score(X_test,y_test)

    # ------ Place code above here /\ /\ /\ ------



    return knn_score


# 20 points
def exercise04():
    '''
        Data set: Iris
        Generate an overfitting / underfitting curve of kNN each of the testing and training accuracy performance scores series
        for a range of neighbor (k) values from 1 to 30 and plot the curves (number of neighbors is x-axis, performance score is y-axis on the chart)
        Return back the plotly url

    '''
    
    # ------ Place code below here \/ \/ \/ ------
    neighbors = list(range(1,31))
    score = []
    for k in neighbors:
        knn = KNN(n_neighbors=k)
        knn.fit(iris['data'],iris['target'])
        knn_score = knn.score(iris['data'],iris['target'])
        score.append(knn_score)
    data = [go.Scatter(x=neighbors, y=score)]
    plotly_overfit_underfit_curve_url = py.plot(data)

    # ------ Place code above here /\ /\ /\ ------




    return plotly_overfit_underfit_curve_url


# 10 points
def exercise05():
    '''
        Data set: Boston
        Load sklearn's Boston data into a DataFrame (only the data and feature_name as column names)
        Load sklearn's Boston target values into a separate DataFrame
        Return back the average of AGE, average of the target (median value of homes or MEDV), and the target as NumPy values 
    '''


    # ------ Place code below here \/ \/ \/ ------

    df_data = pd.DataFrame(boston['data'],columns=boston['feature_names'])
    df_target = pd.DataFrame(boston['target'])
    average_age = df_data['AGE'].mean()
    average_medv = df_target[0].mean()
    medv_as_numpy_values = np.array(boston['target'])

    # ------ Place code above here /\ /\ /\ ------



    return average_age, average_medv, medv_as_numpy_values


# 10 points
def exercise06():
    '''
        Data set: Boston
        In the Boston dataset, the feature PTRATIO refers to pupil teacher ratio.
        Using a matplotlib scatter plot, plot MEDV median value of homes as y-axis and PTRATIO as x-axis
        Return back PTRATIO as a NumPy array
    '''


    # ------ Place code below here \/ \/ \/ ------

    boston['MEDV'] = boston.target
    df_data = pd.DataFrame(boston['data'],columns=boston['feature_names'])
    X_ptratio = np.array(df_data['PTRATIO'])
    plt.scatter(X_ptratio,boston['MEDV'])
    plt.ylabel('MEDV')
    plt.xlabel('PTRATIO')
    plt.show()

    # ------ Place code above here /\ /\ /\ ------




    return X_ptratio


# 20 points
def exercise07():
    '''
        Data set: Boston
        Create a regression model for MED / PTRATIO and display a chart showing the regression line using matplotlib
        with a backdrop of a scatter plot of MEDV and PTRATIO from exercise06
        Use np.linspace() to generate prediction X values from min to max PTRATIO
        Return back the regression prediction space and regression predicted values
        Make sure to labels axes appropriately
    '''


    # ------ Place code below here \/ \/ \/ ------

    boston['MEDV'] = boston.target
    df_data = pd.DataFrame(boston['data'],columns=boston['feature_names'])
    X_ptratio = np.array(df_data['PTRATIO'])
    plt.scatter(X_ptratio,boston['MEDV'])
    axes = plt.gca()
    m, b = np.polyfit(X_ptratio, boston['MEDV'], 1)
    x = np.linspace(df_data['PTRATIO'].min(),df_data['PTRATIO'].max(),50)
    plt.plot(x, m*x + b, '-')
    plt.ylabel('MEDV')
    plt.xlabel('PTRATIO')
    linreg = lm.LinearRegression()
    x_ = np.array(boston['MEDV']).reshape(-1,1)
    y_ = np.array(X_ptratio).reshape(-1,1)
    linreg.fit(x_,y_)
    prediction_space = x.reshape(-1,1)
    reg_model = linreg.predict(prediction_space)
    plt.show()

    # ------ Place code above here /\ /\ /\ ------


    return reg_model, prediction_space




class TestAssignment7(unittest.TestCase):
    def test_exercise07(self):
        rm, ps = exercise07()
        self.assertEqual(len(rm),50)
        self.assertEqual(len(ps),50)


    def test_exercise06(self):
        ptr = exercise06()
        self.assertTrue(len(ptr),506)


    def test_exercise05(self):
        aa, am, mnpy = exercise05()
        self.assertAlmostEqual(aa,68.57,2)
        self.assertAlmostEqual(am,22.53,2)
        self.assertTrue(len(mnpy),506)
        
    def test_exercise04(self):
        exercise04()
        print('Skipping EX4 tests')     


    def test_exercise03(self):
        score = exercise03(8,.25)
        self.assertAlmostEqual(exercise03(8,.3),.955,2)
        self.assertAlmostEqual(exercise03(8,.25),.947,2)
    def test_exercise02(self):
        pred = exercise02([[6.7,3.1,5.6,2.4],[6.4,1.8,5.6,.2],[5.1,3.8,1.5,.3]])
        self.assertTrue('setosa' in pred)
        self.assertTrue('virginica' in pred)
        self.assertTrue('versicolor' in pred)
        self.assertEqual(len(pred),3)
    def test_exercise01(self):
        df, tn = exercise01()
        self.assertEqual(df.shape,(5,4))
        self.assertEqual(df.iloc[0,1],3.5)
        self.assertEqual(df.iloc[2,3],.2)
        self.assertTrue('setosa' in tn)
        self.assertEqual(len(tn),3)
     


if __name__ == '__main__':
    unittest.main()
