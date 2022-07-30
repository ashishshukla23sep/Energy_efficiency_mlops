from Energy_efficiency.pipeline.pipeline import Pipeline
from Energy_efficiency.exception import EnergyException
from Energy_efficiency.logger import logging,LOG_FILE_PATH,upload_log_to_db
from Energy_efficiency.config.configuration import Configuartion
from Energy_efficiency.component.data_transformation import DataTransformationArtifact
from Energy_efficiency.constant import ROOT_DIR
import os

def main():
    try:
        config_path = os.path.join("yaml_files","config.yaml")
        pipeline = Pipeline(Configuartion(config_file_path=config_path))
        pipeline.start()
        logging.info("main function execution completed.")
        #print(Configuartion().get_data_transformation_config())
        # schema_file_path=r"C:\Users\1672040\Desktop\project\Energy efficiency\yaml_files\schema.yaml"
        # file_path=r"C:\Users\1672040\Desktop\project\Energy efficiency\Energy_efficiency\artifact\data_ingestion\2022-07-15-14-12-24\ingested_data\train\cleaned_data.csv"
        # DataTransformation().
        
    except Exception as e:
        logging.info(f'{e}')


if __name__=="__main__":
    main()