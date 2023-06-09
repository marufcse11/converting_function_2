# -*- coding: utf-8 -*-
"""converting_function.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/marufcse11/6f2641db8cce66fc629bfb950bfbb1bf/converting_function.ipynb
"""

from Models.Regression.regression_functions import train_model, split_dataset, get_train_model_results
from Models.Regression import constant

from Models.mlflow_utils import support_mlflow
import mlflow as mlflow
from mlflow import log_param
from Models.utils import mlflow_init_spark_exe
from pycaret.regression import *

metadata = {
    #https://github.com/marufcse11/converting_function_2/blob/main/converting_function%20(1)
    #/Users/maruf/Documents/GitHub/exec-service-python/Models/NewFunctions/ModelTraining/Regression
    'pythonModule': "marufcse11.converting_function_2.converting_function (1)",
    'spark': False,
    'inputs': {
        "target": {'type': 'string'},
        "train_size": {'type': 'string'},
        "estimator_name": {'type': 'string'},
        "regression_train_input_data": {'type': 'pandas-dataframe'}
    },
    'outputs': {
        "regression_train_output_data": {
            'type': 'spark-dataframe',
            'preferredBackend': 'hive'
        },
        "regression_train_metrics_viz": {
            'type': 'pandas-dataframe',
            'preferredBackend': 'artifact-store'
        }
    }
}

# description of  inputs and outputs
"""
inputs:
    target: the field name that the regression model is trying to predict
    train_size: this parameter is used to specify the proportion of data that will be used for training a regression model
    estimator_name: this is the regression algorithm used to train a regression model
    regression_train_input_data: this is a collection of data that is used to train, test, and evaluate a regression model 
outputs:
    regression_train_output_data: this is the output data from the regression model
    regression_train_metrics_viz: this shows the metrics in terms of the performance of the regression model
"""


def run(inputs, context):
    """
    This function is used to train a multiple model
    """
    try:
        #mlflow_init_spark_exe(inputs, context)

        # read dataset
        dataset = inputs['regression_train_input_data']
        # dataset = dataset.toPandas()

        # check params
        if not ('target' in inputs):
            raise ValueError('Missing target column')
        else:
            target = inputs['target']
            #exp_name = setup(data = df_dic,target)
        # assign default value for optional variables
        if not ('train_size' in inputs):
            train_size = constant.REGRESSION_TRAIN_SIZE
        else:
            train_size = float(inputs['train_size'])
        if not ('round_to' in inputs):
            round_to = constant.REGRESSION_ROUND_TO
        else:
            round_to = int(inputs['round_to'])

        if not ('fold' in inputs):
            fold = constant.REGRESSION_FOLD
        else:
            fold = int(inputs['fold'])

        if not ('estimator_name' in inputs):
            estimator_name = constant.REGRESSION_ESTIMATOR_NAME
        else:
            estimator_name = inputs['estimator_name']

        def converting_function(df_dynamic_dic):
            df_dynamic = df_dynamic_dic.copy()
            for c in df_dynamic_dic.columns:
                #print("out c value = ",c)
    
                df_dynamic_dic = df_dynamic_dic.sort_values([c])
                test_str = df_dynamic_dic[c].values[0]
                if isinstance(test_str, str) == True:
                    if df_dynamic_dic[c].dtype == object:
                        df_dynamic_dic[c] = df_dynamic_dic[c].str.capitalize()
                        #print("c value = ",c)
                        df_dynamic_dic[c].fillna('0', inplace=True)
                        d = Counter(df_dynamic_dic[c].astype(str))           
                        keys = list(d)
                        award_df = pd.DataFrame.from_dict(d, orient='index')
                        award_df = award_df.reset_index()
                        award_df.columns = ['Value', 'Count']
                        award_df = award_df.sort_values(['Count'])
                        award_df.insert(0, 'Code', range(0, 0 + len(award_df)))
                        award_df_1 = dict(zip(award_df['Value'], award_df['Code']))
                        df_dynamic[c] = df_dynamic_dic[c].map(award_df_1)
                        len(set(keys)), len(d)
                        sfile = '/content/drive/My Drive/Ass_1/Dictonary.xlsx'
                        mode = 'a' if os.path.exists(sfile) else 'w'
                        mode2 = 'replace' if os.path.exists(sfile) else None              
                        with pd.ExcelWriter(sfile, engine='openpyxl', mode=mode, if_sheet_exists=mode2) as writer:
                            award_df.to_excel(writer, sheet_name = c, index= False)
            return df_dynamic

        df_dic = converting_function(dataset)

        exp_name = setup(data = df_dic,  target)
        best_model = compare_models()
        plot_model(best_model)
        evaluate_model(best_model)
        
        
        # # split data
        # split_dataset(
        #     training_data=df,
        #     target=target,
        #     train_size=train_size
        # )
        # # train model and get metrics and best trained model
        # metrics, trained_model = train_model(
        #     estimator_name=estimator_name,
        #     round_to=round_to,
        #     fold=fold,
        # )
        # metrics, _, model_params_df, predictions = get_train_model_results()

        # mlflow tracking components (e.g. logging parameters, metrics, trained models)
        # TODO (Owner: Felix)

        outputs = {
            'regression_train_output_data': predictions,
            'regression_train_metrics_viz': metrics
        }

        return outputs

    except Exception as inst:
        raise inst


if __name__ == '__main__':
    run()
