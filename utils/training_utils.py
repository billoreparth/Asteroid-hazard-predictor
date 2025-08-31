import sys
import pandas as pd 
import numpy as np 
from logging_.logger import setup_logging
from exception.custom_astroid_exc import custom_exception
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error,root_mean_squared_error,accuracy_score,f1_score,recall_score,roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingClassifier,AdaBoostClassifier,RandomForestClassifier,GradientBoostingRegressor,RandomForestRegressor
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn.svm import SVC,SVR
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import RandomizedSearchCV


def split_data(df:pd.DataFrame,target_col:str,test_size:float=0.25,random_state:str=42):
    '''random state default 42 \n
    test size default 0.25'''
    try:
        x = df.drop(columns=target_col)
        y = df[target_col]
        x_train , x_test , y_train , y_test = train_test_split(x,y,test_size=test_size,random_state=random_state)
        return x_train,x_test,y_train,y_test
    except Exception as e : 
        raise custom_exception(e,sys)

def evaluate_regressor_models(X_train, y_train,X_test,y_test,models):
    try:
        r2_score_ = {}
        mse = {}
        rmse = {}
        mae = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
      

            model.fit(X_train, y_train)  # Train model

            y_test_pred = model.predict(X_test)

            model_r2_score = r2_score(y_test, y_test_pred)
            rmse_score = root_mean_squared_error(y_test, y_test_pred)
            mae_score = mean_absolute_error(y_test, y_test_pred)
            mse_score = mean_squared_error(y_test, y_test_pred)

            r2_score_[list(models.keys())[i]] = model_r2_score
            rmse[list(models.keys())[i]] = rmse_score
            mae[list(models.keys())[i]] = mae_score
            mse[list(models.keys())[i]] = mse_score


        return r2_score_ , rmse , mae , mse 
    except Exception as e : 
        raise custom_exception(e,sys)



def evaluate_classification_models(X_train, y_train,X_test,y_test,models):
    try:
        accuracy = {}
        f1 = {}
        recall = {}
        roc_auc = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]

            model.fit(X_train, y_train)  # Train model

            y_test_pred = model.predict(X_test)


            accuracy_s = accuracy_score(y_test, y_test_pred)
            f1_s = f1_score(y_test, y_test_pred)
            recall_s = recall_score(y_test, y_test_pred)
            roc_auc_s = roc_auc_score(y_test, y_test_pred)

            accuracy[list(models.keys())[i]] = accuracy_s
            f1[list(models.keys())[i]] = f1_s
            recall[list(models.keys())[i]] = recall_s
            roc_auc[list(models.keys())[i]] = roc_auc_s


        return accuracy , f1 , recall , roc_auc
    except Exception as e : 
        raise custom_exception(e,sys)



def give_training_report(x_train,x_test,y_train,y_test,algo:str=None):
    '''algo : str , give 'classifier' for classification algorithms or leave for regression algorithm '''
    try:
        setup_logging("trying different models")
        if algo == 'classifier':
            models = {
                        "Random Forest": RandomForestClassifier(verbose=1),
                        "Decision Tree": DecisionTreeClassifier(),
                        "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                        "AdaBoost": AdaBoostClassifier(),
                        # "Guassian Naive Byes": GaussianNB(),
                        "Support Vector Classifier":SVC(),
                        "KNN classifier": KNeighborsClassifier()
                    }
        else:
            models={
                "Linear Regression" : LinearRegression(),
                "Decision Tree Regressor ": DecisionTreeRegressor(),
                "Random Forest Regressor ": RandomForestRegressor(),
                "Gradient Boosting Regressor":GradientBoostingRegressor(),
                "Support Vector Regressor" : SVR(),
                "KNN regressor": KNeighborsRegressor(),
                "Logistic Regression": LogisticRegression(verbose=1)            
            }

        
        if algo == 'classifier':
            accuracy , f1 , recall , roc_auc = evaluate_classification_models(x_train,y_train,x_test,y_test,models)

            data = {"accuracy":accuracy,"f1":f1,"recall":recall,"roc_auc":roc_auc}
            data_set = pd.DataFrame(data)
            data_set = data_set.reset_index().rename(columns={"index":"key"})
            data_set.to_csv("training_report.csv",index=False)
        else:
            r2 , rmse , mae , mse = evaluate_regressor_models(x_train,y_train,x_test,y_test,models)

            data = {"r2_score":r2 , "root mean square":rmse , "mean absolute error":mae , "mean squred error":mse}
            data_set = pd.DataFrame(data)
            data_set = data_set.reset_index().rename(columns={"index":"key"})
            data_set.to_csv("training_report.csv",index=False)

        # print("Report Submitted Successfully")
        
    except Exception as e : 
        raise custom_exception(e,sys)

def give_best_model(x, y,  cv=5, n_iter=50, random_state=42, n_jobs=-1,model=None):
    param_dist = {
        "n_estimators": [100, 200, 300, 500, 800, 1000],
        "max_depth": [None, 5, 10, 20, 30, 50],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["auto", "sqrt", "log2"],
        "bootstrap": [True, False]
    }
    
    search = RandomizedSearchCV(
        estimator=model,
        param_distributions=param_dist,
        n_iter=n_iter,
        cv=cv,
        verbose=1,
        random_state=random_state,
        n_jobs=n_jobs
    )
    search.fit(x,y)

    best_model = search.best_estimator_
    best_params = search.best_params_
    score = search.best_score_
    return best_model , best_params , score

def train_model(df:pd.DataFrame):
    x_train = df.drop(['is_potentially_hazardous'],axis=1)
    y_train = df['is_potentially_hazardous']
    rfc = RandomForestClassifier()
    best_model ,params,best_score = give_best_model(x=x_train,y=y_train,model=rfc)
    return best_model , params , best_score

