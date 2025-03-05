# Installation and Usage Guide

This chapter provides step-by-step instructions for installing and running the BigMart Sales Prediction web application from the GitHub repository.

## Prerequisites

Before proceeding, ensure that the following prerequisites are met:

- **Python Installed:** Verify that Python (version 3.6 or higher) is installed on your system. You can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Git Installed:** Ensure that Git is installed to clone the repository. Download it from: [https://git-scm.com/downloads](https://git-scm.com/downloads)

## Cloning the Repository

To obtain the latest version of the application, clone the GitHub repository using the following command:

```sh
git clone https://github.com/TonyVoo/Project.git
```

## Setting Up the Virtual Environment

It is recommended to use a virtual environment to manage the project's dependencies. Follow these steps:

1. **Navigate to the Project Directory:**

   ```sh
   cd Project
   ```

2. **Create a Virtual Environment:**

   ```sh
   python -m venv env
   ```

3. **Activate the Virtual Environment:**

   - **On Windows:**

     ```sh
     .\env\Scripts\activate
     ```

   - **On macOS and Linux:**

     ```sh
     source env/bin/activate
     ```

## Installing Dependencies

With the virtual environment activated, install the required dependencies using the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Running the Application

After installing the dependencies, start the Flask application with the following command:

```sh
python app.py
```

By default, the application will run on [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Accessing the Application

Open a web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to interact with the BigMart Sales Prediction web application.

## Deactivating the Virtual Environment

After using the application, you can deactivate the virtual environment by executing:

```sh
deactivate
```

By following these steps, you will have the BigMart Sales Prediction web application up and running on your local machine.

