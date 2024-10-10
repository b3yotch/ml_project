import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifacts',"model_trainer.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        

        try:
            logging.info("split into train and test")
            X_train,y_train,X_test,y_test=(
            train_array[:,:-1],
            train_array[:,-1],
            test_array[:,:-1],
            test_array[:,-1]

            )
            models={
                "Linear Regression":LinearRegression(),
                "Random Forest":RandomForestRegressor(),
                "Decision Tree ":DecisionTreeRegressor(),
                "Ada Boost" : AdaBoostRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "XG Boost":XGBRegressor(),
                "Cat Boost":CatBoostRegressor(verbose=False)

            }

            model_report:dict=evaluate_models(X_train=X_train , X_test=X_test,y_train=y_train,y_test=y_test,
            models=models)

            best_model_score=max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model=models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("no model is suitable")
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)
            return (r2_score(y_test,predicted))
            
        except Exception as e:
            raise CustomException(e,sys)
            
