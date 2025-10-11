import pandas as pd
import joblib
import os

# Get the absolute path of the current .py file
current_file_path = os.path.abspath(__file__)

# Get the folder where the current file is located
current_dir = os.path.dirname(current_file_path)

# Construct the absolute path to the model file
model_path = os.path.join(current_dir, 'model.pkl')
model = joblib.load(model_path)

def predict(df):
    y = model.predict(df)
    df_y = pd.DataFrame(y)
    df_y.columns = ['IF_INTROVERTED']

    return(df_y)
    
if __name__ =='__main__':
    main()