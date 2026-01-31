import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
class RegressionPipeline():
    '''
    Docstring for add_models
    regressionpipeline allows users to try different models on a data set to determine the best one.

---Functions---
add_models:
add_models allows the user to give the regressionpipeline a list of regressors

---------------
add_data:
add_data allows the user to pass the data set to the pipeline
---------------
try_models:
try_models runs each regressor and returns the model with the highest r^2 value




        
    '''
    def __init__(self):
        
        from sklearn.ensemble import RandomForestRegressor as rfr
        from sklearn.linear_model import LinearRegression as lr
        from sklearn.linear_model import Lasso,Ridge
        from xgboost import XGBRegressor as xgbr
        from sklearn.svm import SVR as svr
        self.default_regressors=[rfr,lr,xgbr,svr,Lasso,Ridge]
        self.regressors=[]
        self.modelnum=0
        self.model_names=[]

    def add_models(self,models,names=None):
        '''
        add_models passes a list of regressors to the pipeline. These must have the functions "fit" and "predict"
        
        
        :param models: a list of regressors: These must have the functions fit and predict
        :param names: optionally, give a particular name string to each regressor
        '''
        for i,model in enumerate(models):
            name=None
            if not names is None:
                name=names[i]
            self.add_model(model,name)
    def add_model(self,model,name=None):
        
        if hasattr(model,"fit") and hasattr(model,"predict"):
            self.regressors.append(model)
            if name is None:
                name="model"+str(self.modelnum)
                self.modelnum+=1
                self.model_names.append(name)
            return
        print("Functions not found")

    def add_data(self,X,y="hjk"):
        '''
        add_data passes the data to the pipeline
        
        
        :param X: X is assumed to be a dataframe with no missing values. 
        X may or may not include the response based on the value of y
        :param y: y is the response variable for the regressor.
        if y is a string, it is assumed to be the column name of the response in X
        Otherwise, the response is assumed to be the last column
        '''
        

        if not isinstance(y,str) and np.shape(X)[0]!=len(y):
            raise ValueError(f"X has dimension {np.shape(X)[0]} but y has length {len(y)}.")
        self.X=pd.get_dummies(X,drop_first=True)
        self.y=y
        if isinstance(y,str):
            if y in self.X.columns:
                self.y=self.X[y]
                self.X=self.X.drop(columns=[y])
            else:
                
                self.y=X.iloc[:,-1]
                print(f"y assumed to be column {X.columns[-1]}")
                self.X=self.X.drop(X.columns[-1],axis=1)
                

    def try_models(self,method="CV",default=True,cv=5):
        '''
        try_models fits the different models on the data and returns the model with highest r^2
        
        
        :param method: method of cross-validation
        :param default: if Default is True,the builtin list of regressors is tried.
        This includes linear regression,random forest, XGboost, and support vector machine
        :param cv: number of cross-validation folds
        '''
        from sklearn.model_selection import cross_val_score
        if method=="CV":
            pass
        scorelist=[]
        modellist=[]
        regressors=self.regressors
        if default:
            regressors=self.default_regressors
        for regressor in regressors:
            model=regressor()
            print(f"Trying out {model}")
            modellist.append(model)
            scores = cross_val_score(
                model,
                self.X,
                self.y,
                cv=cv,
                scoring="r2"
            )
            scorelist.append(scores.mean())
        for regressor,score in zip(regressors,scorelist):
            print(f"{str(regressor())} had R^2 {score:.2f}")
        
        best = modellist[np.argmax(scorelist)]
        print(f"Best Regressor was {best}.")
        return best
    def lazy_regression(self,data,y=None):
        '''
        Docstring for lazy_regression
        
        :param self: 
        :param data: Description
        '''
        from sklearn.preprocessing import StandardScaler
        SS=StandardScaler()
        
        self.add_data(data,y)
        self.X=SS.fit_transform(self.X)
        return self.try_models()


