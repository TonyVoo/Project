from flask import Flask, request, render_template
import numpy as np
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import os
import prediction

# Load all models
models = {
    "Best_Gradient_Boosting": pickle.load(open("models/Best_Gradient_Boosting.pkl", "rb")),
    "Best_Random_Forest": pickle.load(open("models/Best_Random_Forest.pkl", "rb")),
    "Decision_Tree": pickle.load(open("models/Decision_Tree.pkl", "rb")),
    "Gradient_Boosting": pickle.load(open("models/Gradient_Boosting.pkl", "rb")),
    "Linear_Regression": pickle.load(open("models/Linear_Regression.pkl", "rb")),
    "Random_Forest": pickle.load(open("models/Random_Forest.pkl", "rb")),
    "XGBoost": pickle.load(open("models/XGBoost.pkl", "rb"))
}

# Load dataset
preprocessed_data = pd.read_csv("preprocessed_data.csv")  # Update with actual file
raw_data = pd.read_csv("train.csv")


# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get input values from form
            features = [
                float(request.form["Item_Identifier"]),
                float(request.form["Item_weight"]),
                float(request.form["Item_Fat_Content"]),
                float(request.form["Item_visibility"]),
                float(request.form["Item_Type"]),
                float(request.form["Item_MPR"]),
                float(request.form["Outlet_identifier"]),
                float(request.form["Outlet_established_year"]),
                float(request.form["Outlet_size"]),
                float(request.form["Outlet_location_type"]),
                float(request.form["Outlet_type"])
            ]

            # 🔹 Call prediction function
            predictions, filtered_items, sales_plot, heatmap, correlation_plot, strong_factors = prediction.predict_sales(features)

            # Return results to frontend
            return render_template(
                'predict.html', 
                predictions=predictions, 
                sales_plot=sales_plot,
                filtered_items=filtered_items.to_html(classes="table table-striped"),
                heatmap=heatmap,
                correlation_plot=correlation_plot,
                strong_factors=strong_factors
            )

        except Exception as e:
            return render_template('predict.html', error=f"Error: {str(e)}")
    
    return render_template('predict.html')

@app.route("/view_csv")
def view_csv():
    return render_template(
        "view_csv.html", 
        preprocessed_table=preprocessed_data.head(10).to_html(classes="table table-striped"), 
        raw_table=raw_data.head(10).to_html(classes="table table-striped")
    )


@app.route("/dataset_insight")
def dataset_insight():
    # Read mapping file
    with open("label_mappings.txt", "r") as file:
        label_mappings = file.read()

    return render_template(
        "dataset_insight.html", 
        data_summary= preprocessed_data.describe().to_html(classes="table"), 
        label_mappings=label_mappings
    )

@app.route("/analysis")
def analysis():
    return render_template("analysis.html", 
                           img_paths=["static/MAE_RMSE_Comparison.png", "static/MSEComparison.png", "static/R2Comparison.png"])

if __name__ == "__main__":
    app.run(debug=True)
