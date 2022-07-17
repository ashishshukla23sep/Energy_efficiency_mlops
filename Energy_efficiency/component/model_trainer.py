
from Energy_efficiency.exception import EnergyException
import sys
from Energy_efficiency.logger import logging
from typing import List
import numpy as np

from Energy_efficiency.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from Energy_efficiency.entity.config_entity import ModelTrainerConfig
from Energy_efficiency.util.util import load_numpy_array_data,save_object,load_object
from Energy_efficiency.entity.model_factory import MetricInfoArtifact, ModelFactory,GridSearchedBestModel
from Energy_efficiency.entity.model_factory import evaluate_regression_model



class EnergyEstimatorModel:
    def __init__(self, preprocessing_object, trained_model_object,trained_model_object1):
        """
        TrainedModel constructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
        self.trained_model_object1 = trained_model_object1

    def predict(self, X):
        """
        function accepts raw inputs and then transformed raw input using preprocessing_object
        which gurantees that the inputs are in the same format as the training data
        At last it perform prediction on transformed features
        """
        transformed_feature = self.preprocessing_object.transform(X)

        heating_load= self.trained_model_object.predict(transformed_feature)

        #logging.info(f"transformed_features shape are {transformed_feature.shape,type(transformed_feature)} and X is {X.shape} and heating load is {heating_load.shape,type(heating_load)}")
        #logging.info(f"Input for for Cooling load {np.concatenate((transformed_feature,heating_load.reshape(len(heating_load),1)),axis=1)}")
        
        cooling_load = self.trained_model_object1.predict(np.concatenate((transformed_feature,heating_load.reshape(len(heating_load),1)),axis=1))
        return heating_load,cooling_load

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"




class ModelTrainer:

    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info(f"{'>>' * 30}Model trainer log started.{'<<' * 30} ")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise EnergyException(e, sys) from e

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info(f"Loading transformed training dataset")
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            transformed_train_file_path1 = self.data_transformation_artifact.transformed_train_file_path1
            train_array = load_numpy_array_data(file_path=transformed_train_file_path)
            train_array1 = load_numpy_array_data(file_path=transformed_train_file_path1)

            logging.info(f"Loading transformed testing dataset")
            transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
            transformed_test_file_path1 = self.data_transformation_artifact.transformed_test_file_path1
            test_array = load_numpy_array_data(file_path=transformed_test_file_path)
            test_array1 = load_numpy_array_data(file_path=transformed_test_file_path1)

            logging.info(f"Splitting training and testing input and target feature")
            x_train,y_train,x_test,y_test = train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1]
            x_train1,y_train1,x_test1,y_test1 = train_array1[:,:-1],train_array1[:,-1],test_array1[:,:-1],test_array1[:,-1]
            logging.info(f"2nd data shape is {x_train1.shape,y_train1.shape}")
            logging.info(f"Extracting model config file path")
            model_config_file_path = self.model_trainer_config.model_config_file_path

            logging.info(f"Initializing model factory class using above model config file: {model_config_file_path}")
            model_factory = ModelFactory(model_config_path=model_config_file_path)
            model_factory1 = ModelFactory(model_config_path=model_config_file_path)
            
            
            base_accuracy = self.model_trainer_config.base_accuracy
            logging.info(f"Expected accuracy: {base_accuracy}")

            logging.info(f"Initiating operation model selecttion")
            best_model = model_factory.get_best_model(X=x_train,y=y_train,base_accuracy=base_accuracy)
            best_model1 = model_factory1.get_best_model(X=x_train1,y=y_train1,base_accuracy=base_accuracy)
            
            logging.info(f"Best model found on training dataset: for Heating Load is {best_model} and for Cooling Load is {best_model1}")
            
            logging.info(f"Extracting trained model list.")
            grid_searched_best_model_list:List[GridSearchedBestModel]=model_factory.grid_searched_best_model_list
            grid_searched_best_model_list1:List[GridSearchedBestModel]=model_factory1.grid_searched_best_model_list

            model_list = [model.best_model for model in grid_searched_best_model_list ]
            
            model_list1 = [model.best_model for model in grid_searched_best_model_list1 ]
            #logging.info(f"Model 1 info {model_list} model 2 info {model_list1}")
            logging.info(f"Evaluation all trained model on training and testing dataset both")
            metric_info:MetricInfoArtifact = evaluate_regression_model(model_list=model_list,X_train=x_train,y_train=y_train,X_test=x_test,y_test=y_test,base_accuracy=base_accuracy)
            metric_info1:MetricInfoArtifact = evaluate_regression_model(model_list=model_list1,X_train=x_train1,y_train=y_train1,X_test=x_test1,y_test=y_test1,base_accuracy=base_accuracy)


            logging.info(f"Best found model on both training and testing dataset.")
            
            preprocessing_obj=  load_object(file_path=self.data_transformation_artifact.preprocessed_object_file_path)
            model_object = metric_info.model_object
            logging.info(f"model object 1 is {model_object}")
            model_object1 = metric_info1.model_object
            logging.info(f"model object 2 is {model_object1}")



            trained_model_file_path=self.model_trainer_config.trained_model_file_path
            #trained_model_file_path1=self.model_trainer_config.trained_model_file_path1
            housing_model = EnergyEstimatorModel(preprocessing_object=preprocessing_obj,trained_model_object=model_object,trained_model_object1=model_object1)
            
            

            logging.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=housing_model)


            model_trainer_artifact=  ModelTrainerArtifact(is_trained=True,message="Model Trained successfully",
            trained_model_file_path=trained_model_file_path,
            train_rmse=metric_info.train_rmse,
            train_rmse1=metric_info1.train_rmse,
            test_rmse=metric_info.test_rmse,
            test_rmse1=metric_info1.test_rmse,
            train_accuracy=metric_info.train_accuracy,
            train_accuracy1=metric_info1.train_accuracy,
            test_accuracy=metric_info.test_accuracy,
            test_accuracy1=metric_info1.test_accuracy,
            model_accuracy=metric_info.model_accuracy,
            model_accuracy1=metric_info1.model_accuracy
            
            )

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise EnergyException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 30}Model trainer log completed.{'<<' * 30} ")



#loading transformed training and testing datset
#reading model config file 
#getting best model on training datset
#evaludation models on both training & testing datset -->model object
#loading preprocessing pbject
#custom model object by combining both preprocessing obj and model obj
#saving custom model object
#return model_trainer_artifact
