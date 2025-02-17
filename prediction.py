import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import os
from flask import Flask, request, render_template

# Load trained models
models = {
    "Ridge": pickle.load(open("models/Ridge.pkl", "rb")),
    "DecisionTree": pickle.load(open("models/DecisionTree.pkl", "rb")),
    "XGBoost": pickle.load(open("models/Xgboost.pkl", "rb")),
    "Linear": pickle.load(open("models/Linear.pkl", "rb")),
    "Ada": pickle.load(open("models/Ada.pkl", "rb"))
}

# Load dataset
df = pd.read_csv("preprocessed_data.csv")  

# Initialize Flask app
app = Flask(__name__)

def predict_sales(features):
    """
    Predict sales using multiple models and return predictions, filtered data, and generated graphs.
    """
    # Convert input features to NumPy array
    input_features = np.array(features, dtype=float).reshape(1, -1)

    # Get predictions from all models
    predictions = {model: models[model].predict(input_features)[0] for model in models}

    # Extract Item_Identifier
    item_identifier = str(int(features[0]))  # Convert to string to match dataset

    # 🔹 Filter dataset for matching Item_Identifier
    df["Item_Identifier"] = df["Item_Identifier"].astype(str)
    filtered_items = df[df["Item_Identifier"] == item_identifier]

    # Paths to save images
    sales_plot_path = "static/sales_plot.png"
    heatmap_path = "static/heatmap.png"
    correlation_plot_path = "static/correlation_plot.png"

    # 🔹 Generate Graphs
    generate_sales_plot(filtered_items, predictions, sales_plot_path)
    generate_heatmap(filtered_items, heatmap_path)
    strong_factors = generate_correlation_plots(filtered_items, correlation_plot_path)

    return predictions, filtered_items, sales_plot_path, heatmap_path, correlation_plot_path, strong_factors



def generate_sales_plot(filtered_items, predictions, plot_path):
    """
    Create and save a bar plot with model prediction lines, labeling them carefully to avoid overlap.
    """
    plt.figure(figsize=(10, 6))

    # Ensure the index is sequential
    sales = filtered_items["Item_Outlet_Sales"].reset_index(drop=True)

    # Create a bar plot with thin width
    plt.bar(range(len(sales)), sales, color="blue", alpha=0.6, label="Actual Sales", width=0.5)

    # Define colors and styles for prediction lines
    colors = ["red", "green", "orange", "purple", "black"]
    linestyles = ["solid", "dashed", "dotted", "dashdot", (0, (3, 5, 1, 5))]

    # Sort predictions by value
    sorted_preds = sorted(predictions.items(), key=lambda x: x[1])

    # Track used Y-positions to avoid overlap
    used_positions = []
    min_spacing = 10  # Minimum vertical spacing

    for i, (model, pred) in enumerate(sorted_preds):
        plt.axhline(pred, color=colors[i], linestyle=linestyles[i], linewidth=2, alpha=0.8, label=f"{model} Prediction")

        # Generate an abbreviation (first 4 letters capitalized)
        short_name = model[:4].upper()

        # Adjust label position dynamically
        text_y = pred

        # Ensure the label does not overlap with existing labels
        while any(abs(text_y - pos) < min_spacing for pos in used_positions):
            text_y += min_spacing  # Move label up

        # Store adjusted position
        used_positions.append(text_y)

        # Place the label on the right side of the plot
        plt.text(len(sales) - 1, text_y, short_name, color=colors[i], fontsize=10, fontweight="bold", verticalalignment='center')

    # Labels and title
    plt.xlabel("Index", fontsize=12)
    plt.ylabel("Item Outlet Sales", fontsize=12)
    plt.title(f"Sales Bar Plot with Model Predictions", fontsize=14, fontweight="bold")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.savefig(plot_path)
    plt.close()


def generate_heatmap(filtered_items, plot_path):
    """
    Create and save a heatmap of feature correlations.
    """
    plt.figure(figsize=(9, 8))
    sns.heatmap(filtered_items.drop(columns=["Item_Identifier"]).corr(), annot=True, cmap="coolwarm", fmt=".2f")

    plt.title("Heatmap of Feature Correlations")
    plt.savefig(plot_path)
    plt.close()


def generate_correlation_plots(filtered_items, plot_path):
    """
    Create scatter plots for features with strong correlation (>0.4) with sales.
    """
    correlation = filtered_items.drop(columns=["Item_Identifier"]).corr()["Item_Outlet_Sales"].abs().sort_values(ascending=False)

    # Select the top factors with correlation > 0.4
    strong_correlations = correlation[correlation > 0.4].sort_values(ascending=False)
    strong_correlations = strong_correlations.drop("Item_Outlet_Sales", errors="ignore")  # Exclude sales itself

    # Get top features
    top_factors = strong_correlations.index.tolist()

    if not top_factors:
        return []

    # Create scatter plots
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(1, len(top_factors), figsize=(18, 5))

    if len(top_factors) == 1:
        axes = [axes]  # Ensure axes is iterable for a single plot

    for i, factor in enumerate(top_factors):
        sns.scatterplot(data=filtered_items, x=factor, y="Item_Outlet_Sales", ax=axes[i], color="blue", alpha=0.6)
        axes[i].set_title(f"{factor} vs. Sales")
        axes[i].set_xlabel(factor)
        axes[i].set_ylabel("Sales")
        axes[i].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    return top_factors  # Return strong correlations for logging or display
