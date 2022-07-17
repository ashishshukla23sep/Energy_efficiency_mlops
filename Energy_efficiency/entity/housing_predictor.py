import os
import sys

from Energy_efficiency.exception import EnergyException
from Energy_efficiency.util.util import load_object

import pandas as pd


class Energy_efficiency_Data:

    def __init__(self,
                 X1: float,
                 X2: float,
                 X3: float,
                 X4: float,
                 X5: float,
                 X6: float,
                 X7: float,
                 X8: float,
                 ):
        try:
            self.X1 = X1
            self.X2 = X2
            self.X3 = X3
            self.X4 = X4
            self.X5 = X5
            self.X6 = X6
            self.X7 = X7
            self.X8 = X8
            
        except Exception as e:
            raise EnergyException(e, sys) from e

    def get_housing_input_data_frame(self):

        try:
            housing_input_dict = self.get_housing_data_as_dict()
            return pd.DataFrame(housing_input_dict)
        except Exception as e:
            raise EnergyException(e, sys) from e

    def get_housing_data_as_dict(self):
        try:
            input_data = {
                "X1": [self.X1],
                "X2": [self.X2],
                "X3": [self.X3],
                "X4": [self.X4],
                "X5": [self.X5],
                "X6": [self.X6],
                "X7": [self.X7],
                "X8": [self.X8],
            }
            return input_data
        except Exception as e:
            raise EnergyException(e, sys)


class EnergyPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise EnergyException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise EnergyException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            Heating_Load,Cooling_load = model.predict(X)
            return Heating_Load,Cooling_load
        except Exception as e:
            raise EnergyException(e, sys) from e