import os
import pandas as pd

# Get the absolute path of the current .py file
current_file_path = os.path.abspath(__file__)

# Get the folder where the current file is located
current_dir = os.path.dirname(current_file_path)

# Set this folder as the working directory
os.chdir(current_dir)
print(os.getcwd())

# Test
import main
input1 = pd.read_csv('test/input/input1.csv')
print(main.predict(input1))