# from Energy_efficiency.constant import *
# from Energy_efficiency.util.util import read_yaml_file
# from Energy_efficiency.entity.energy_predictor import  Energy_efficiency_Data,EnergyPredictor
# from flask import Flask, request
# from flasgger import Swagger
# from Energy_efficiency.logger import get_log_dataframe

# config_info = read_yaml_file(file_path=CONFIG_FILE_PATH)
# model_pusher_config_info = config_info[MODEL_PUSHER_CONFIG_KEY]
# saved_dir_path = os.path.join(ROOT_DIR, model_pusher_config_info[MODEL_PUSHER_MODEL_EXPORT_DIR_KEY])

# app = Flask(__name__)
# swagger = Swagger(app)

# @app.route('/')
# def predict():
#     Relative_Compactness = request.args.get("Relative_Compactness")
#     Surface_Area = request.args.get("Surface_Area")
#     Wall_Area = request.args.get('Wall_Area')
#     Roof_Area = request.args.get('Roof_Area')
#     Overall_Height = request.args.get('Overall_Height')
#     Orientation = request.args.get('Orientation')
#     Glazing_Area = request.args.get('Glazing_Area')
#     Glazing_Area_Distribution = request.args.get('Glazing_Area_Distribution')

#     data = Energy_efficiency_Data(Relative_Compactness,Surface_Area,Wall_Area,Roof_Area,Overall_Height,Orientation,Glazing_Area,Glazing_Area_Distribution).get_energy_input_data_frame()
#     Heating_Load,Cooling_load = EnergyPredictor(saved_dir_path).predict(data)

#     return f"Heating load is {str(Heating_Load[0])} and Cooling load is {str(Cooling_load[0])}"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0',debug=True)

from flask import Flask, request
import sys

import pip
from Energy_efficiency.util.util import read_yaml_file, write_yaml_file
from matplotlib.style import context
from Energy_efficiency.logger import logging
from Energy_efficiency.exception import EnergyException
import os, sys
import json
from Energy_efficiency.config.configuration import Configuartion
from Energy_efficiency.constant import CONFIG_DIR, get_current_time_stamp
from Energy_efficiency.pipeline.pipeline import Pipeline
from Energy_efficiency.entity.energy_predictor import Energy_efficiency_Data, EnergyPredictor
from flask import send_file, abort, render_template


ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "Energy_efficiency"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


from Energy_efficiency.logger import get_log_dataframe

ENERGY_DATA_KEY = "energy_data"
HEATING_LOAD_VALUE_KEY = "heating_load_value"
COOLING_LOAD_VALUE_KEY = "cooling_load_value"

app = Flask(__name__)


@app.route('/artifact', defaults={'req_path': 'Energy_efficiency'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("Energy_efficiency", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=Configuartion(current_time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        ENERGY_DATA_KEY: None,
        HEATING_LOAD_VALUE_KEY : None,
        COOLING_LOAD_VALUE_KEY : None
    }

    if request.method == 'POST':


        Relative_Compactness = float(request.form["Relative_Compactness"])
        Surface_Area = float(request.form["Surface_Area"])
        Wall_Area = float(request.form['Wall_Area'])
        Roof_Area = float(request.form['Roof_Area'])
        Overall_Height = float(request.form['Overall_Height'])
        Orientation = float(request.form['Orientation'])
        Glazing_Area = float(request.form['Glazing_Area'])
        Glazing_Area_Distribution = float(request.form['Glazing_Area_Distribution'])
        

        energy_efficiency_data = Energy_efficiency_Data(X1=Relative_Compactness,
                                                        X2=Surface_Area,
                                                        X3=Wall_Area,
                                                        X4=Roof_Area,
                                                        X5=Overall_Height,
                                                        X6=Orientation,
                                                        X7=Glazing_Area,
                                                        X8=Glazing_Area_Distribution)
        energy_df = energy_efficiency_data.get_energy_input_data_frame()
        energy_predictor = EnergyPredictor(model_dir=MODEL_DIR)
        heating_load_value,cooling_load_value = energy_predictor.predict(X=energy_df)
        context = {
            ENERGY_DATA_KEY: energy_efficiency_data.get_energy_input_data_frame(),
            HEATING_LOAD_VALUE_KEY : heating_load_value,
            COOLING_LOAD_VALUE_KEY : cooling_load_value
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)


@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)
