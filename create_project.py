import os
import json

# 1. Name of the Main Project Directory
PROJECT_NAME = "Real_Time_Strategy_Tracker"

# 2. Folder Structure (Folders to be created)
folders = [
    "01_Data/01_Raw",           # Raw scraped data
    "01_Data/02_Cleaned",       # Cleaned data for modeling
    "02_Notebooks",             # Jupyter Notebooks for EDA
    "03_Scripts",               # Core Python scripts (Scraping, Cleaning, Models)
    "04_Models",                # Trained model files
    "05_Results_and_Reports",   # Forecasts, sentiment summaries
    "06_App/frontend"           # Frontend files for the web application
]

# 3. Initial Files (Initial files to be created)
files = [
    "requirements.txt",
    "README.md",
    ".gitignore",
    
    # Scripts
    "03_Scripts/1_data_scraper.py",    
    "03_Scripts/2_data_cleaner.py",     
    "03_Scripts/3_forecasting_model.py", 
    "03_Scripts/4_sentiment_analysis.py", 
    
    # Notebook for EDA
    "02_Notebooks/EDA_and_Initial_Viz.ipynb",
    
    # Application File
    "06_App/api.py"
]

def create_structure():
    """This function creates the folders and files for the project."""
    print(f"--- Starting project structure creation for '{PROJECT_NAME}' ---")

    # Creating the main folder
    if not os.path.exists(PROJECT_NAME):
        os.makedirs(PROJECT_NAME)
        print(f"Main folder created: {PROJECT_NAME}")
    else:
        print(f"Main folder already exists: {PROJECT_NAME}")

    # Moving into the project directory
    os.chdir(PROJECT_NAME)

    # Creating sub-folders and the .gitkeep file
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Folder created: {folder}")
        
        # Create .gitkeep file to ensure empty folders are tracked by Git
        gitkeep_path = os.path.join(folder, '.gitkeep')
        with open(gitkeep_path, 'w') as f:
            pass # Create an empty .gitkeep file
        print(f"File created: {gitkeep_path}")

    # Creating initial files
    for file_path in files:
        # Ensure parent directories exist before creating the file
        parent_dir = os.path.dirname(file_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
            
        # Handle Jupyter Notebook files (.ipynb)
        if file_path.endswith(".ipynb"):
            # Write a minimal JSON structure for a valid .ipynb file
            notebook_content = {
                "cells": [],
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
                "nbformat": 4,
                "nbformat_minor": 5
            }
            with open(file_path, 'w') as f:
                json.dump(notebook_content, f, indent=4)
        else:
            with open(file_path, 'w') as f:
                pass # Create an empty file
        print(f"File created: {file_path}")

    # Populating the .gitignore file to exclude unwanted files from Git
    with open(".gitignore", 'w') as f:
        f.write("# Ignore virtual environment\n")
        f.write("venv/\n")
        f.write("__pycache__/\n")
        f.write("*.pyc\n")
        f.write("\n# Ignore large data and model files\n")
        f.write("01_Data/01_Raw/*\n")
        f.write("01_Data/02_Cleaned/*\n")
        f.write("04_Models/*\n")

    print("--- Structure successfully created! ---")

if __name__ == "__main__":
    create_structure()