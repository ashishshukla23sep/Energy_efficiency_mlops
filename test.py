from Energy_efficiency.pipeline.pipeline import Pipeline
from Energy_efficiency.exception import EnergyException
from Energy_efficiency.logger import logging
from Energy_efficiency.config.configuration import Configuartion
from Energy_efficiency.component.data_transformation import DataTransformationArtifact
import os

def main():
    try:
        config_path = os.path.join("yaml_files","config.yaml")
        pipeline = Pipeline(Configuartion(config_file_path=config_path))
        pipeline.run_pipeline()
        #print(Configuartion().get_data_transformation_config())
        # schema_file_path=r"C:\Users\1672040\Desktop\project\Energy efficiency\yaml_files\schema.yaml"
        # file_path=r"C:\Users\1672040\Desktop\project\Energy efficiency\Energy_efficiency\artifact\data_ingestion\2022-07-15-14-12-24\ingested_data\train\cleaned_data.csv"
        # DataTransformation().
    except Exception as e:
        logging.info(f'{e}')


if __name__=="__main__":
    main()


