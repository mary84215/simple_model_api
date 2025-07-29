import pandas as pd
import joblib
import os

# Get the absolute path of the current .py file
current_file_path = os.path.abspath(__file__)

# Get the folder where the current file is located
current_dir = os.path.dirname(current_file_path)

# Set this folder as the working directory
os.chdir(current_dir)

model = joblib.load('model.pkl')

def predict(df):
    y = model.predict(df)
    df_y = pd.DataFrame(y)
    df_y.columns = ['IF_INTROVERTED']

    return(df_y)
    