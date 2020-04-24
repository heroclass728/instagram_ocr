# InstagramOCR

## Overview

This project is to extract the necessary information from the Instagram Profile image using Google Vision API.

## Structure

- input

    The profile images to extract

- src

    The source code to extract the necessary information

- utils

    * The credential key of Google Vision API
    * The source code to communicate with Google Vision API and manage the folders and files in this project

- app

    The main execution file
    
- requirements

    All the dependencies for this project
    
- settings

    Several settings for this project
    
## Installation

- Environment

    Ubuntu 18.04, Window 10, Python 3.6

- Dependency Installation

    Please go ahead to the directory of this project and run the following command
    
    ```
    pip3 install -r requirements.txt
    ```

## Execution

- Please copy the profile images to extract into the input folder in this project directory.

- Please run the following command

    ```
    python3 app.py
    ``` 

- The result excel files are made in the output folder in this project directory
