from collections import namedtuple



DataIngestionArtifact = namedtuple("DataIngestionArtifact",
[ "train_file_path", "test_file_path", "is_ingested", "message"])


DataValidationArtifact = namedtuple("DataValidationArtifact",
["schema_file_path","report_file_path","report_page_file_path","is_validated","message"])


DataTransformationArtifact = namedtuple("DataTransformationArtifact",
 ["is_transformed", "message", "transformed_train_file_path","transformed_train_file_path1","transformed_test_file_path",
     "transformed_test_file_path1","preprocessed_object_file_path"])

ModelTrainerArtifact = namedtuple("ModelTrainerArtifact", ["is_trained", "message", "trained_model_file_path",
                                                           "train_rmse","train_rmse1", "test_rmse","test_rmse1", "train_accuracy","train_accuracy1","test_accuracy","test_accuracy1",
                                                           "model_accuracy","model_accuracy1"])

ModelEvaluationArtifact = namedtuple("ModelEvaluationArtifact", ["is_model_accepted", "evaluated_model_path"])

ModelPusherArtifact = namedtuple("ModelPusherArtifact", ["is_model_pusher", "export_model_file_path"])
