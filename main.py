# Import necessary libraries
import csv
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Function to load tables
def get_tables():
    # Define file paths
    ctg_file = 'ctgstudies_yr.csv'
    mapping_file = 'mapping.csv'
    data_file = 'code.csv'

    # Check if files exist
    if not all(os.path.exists(file) for file in [ctg_file, mapping_file, data_file]):
        raise FileNotFoundError("One or more CSV files are missing.")

    # Load CSVs into pandas DataFrames
    tables = {
        "ctgstudies": pd.read_csv(ctg_file, encoding='latin1'),  # latin1 encoding for special characters
        "mapping": pd.read_csv(mapping_file, encoding='latin1'),
        "data": pd.read_csv(data_file, encoding='latin1')
    }
    print("Tables loaded successfully:", tables.keys())
    return tables  # Return the loaded tables

# Function to test loaded tables
def test_tables(tables):
    print("Testing tables:", tables.keys())
    # Access the tables
    ctgstudies_df = tables["ctgstudies"]
    mapping_df = tables["mapping"]
    data_df = tables["data"]

    # Print the first few rows of each table for verification
    print("CTG Studies Table:")
    print(ctgstudies_df.head())

    print("\nMapping Table:")
    print(mapping_df.head())

    print("\nData Table:")
    print(data_df.head())

# Function to merge DataFrames and calculate percentages
def merge_dataframes(ctgstudies_df, mapping_df, data_df):
    # Standardize column names to lowercase
    ctgstudies_df.columns = ctgstudies_df.columns.str.lower()
    mapping_df.columns = mapping_df.columns.str.lower()
    data_df.columns = data_df.columns.str.lower()

    # Merge the DataFrames
    merged_df = ctgstudies_df.merge(mapping_df, on="nctnumber").merge(data_df, on="conditionsid")

    # Calculate percentages
    total_count = len(merged_df)
    diabetes_percentage = (merged_df['desc'].str.contains('diabetes', case=False, na=False).sum() * 100.0) / total_count
    cancer_percentage = (merged_df['desc'].str.contains('cancer', case=False, na=False).sum() * 100.0) / total_count
    obesity_percentage = (merged_df['desc'].str.contains('obesity', case=False, na=False).sum() * 100.0) / total_count
    hypertension_percentage = (merged_df['desc'].str.contains('hypertension', case=False, na=False).sum() * 100.0) / total_count

    # Print results
    print(f"Diabetes Percentage: {diabetes_percentage:.2f}%")
    print(f"Cancer Percentage: {cancer_percentage:.2f}%")
    print(f"Obesity Percentage: {obesity_percentage:.2f}%")
    print(f"Hypertension Percentage: {hypertension_percentage:.2f}%")
    
    return merged_df

# Function to plot yearly trend
def plot_yearly_trend(yearly_data, year_range=None, show_percentage=False):
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_data['startyear'], yearly_data['yearly_diabetes_percentage'], marker='o', label='Diabetes Percentage')
    plt.xlabel('Year')
    plt.ylabel('Percentage of Studies')
    plt.title('Yearly Diabetes Percentage in Studies')
    plt.grid(True)
    plt.legend()
    if year_range:
        plt.xlim(year_range)
    if show_percentage:
        for x, y in zip(yearly_data['startyear'], yearly_data['yearly_diabetes_percentage']):
            plt.text(x, y, f"{y:.1f}%", fontsize=8, ha='center')
    plt.show()

# Main execution
if __name__ == "__main__":
    # Load tables
    tables = get_tables()

    # Test tables
    test_tables(tables)

    # Extract DataFrames
    ctgstudies_df = tables["ctgstudies"]
    mapping_df = tables["mapping"]
    data_df = tables["data"]

    # Call the merge_dataframes function
    merged_df = merge_dataframes(ctgstudies_df, mapping_df, data_df)

    # Ensure the 'startYear' and 'desc' columns exist
    if "startyear" not in merged_df.columns or "desc" not in merged_df.columns:
        raise ValueError("The required columns 'startYear' or 'desc' are missing in the merged DataFrame.")

    # Filter for diabetes-related studies and group by startYear
    yearly_diabetes_percentage = (
        merged_df.assign(is_diabetes=merged_df['desc'].str.contains('diabetes', case=False, na=False))
        .groupby('startyear')
        .apply(lambda group: group['is_diabetes'].sum() * 100.0 / len(group))
        .reset_index(name='yearly_diabetes_percentage')
    )

    #Filter out years prior to 2000
    yearly_diabetes_percentage = yearly_diabetes_percentage[yearly_diabetes_percentage['startyear'] >= 2000]
    
    # Sort by startYear
    yearly_diabetes_percentage = yearly_diabetes_percentage.sort_values(by='startyear')

    # Print results
    print(yearly_diabetes_percentage)

    # Plot the yearly trend
    plot_yearly_trend(yearly_diabetes_percentage, year_range=(1980, 2025), show_percentage=True)




import pandas as pd
import matplotlib.pyplot as plt

# Load the data
mapping_df = pd.read_csv("mapping.csv", encoding="latin1")
data_df = pd.read_csv("code.csv", encoding="latin1")

# Merge the mapping and data tables to get condition descriptions
merged_df = mapping_df.merge(data_df, on="ConditionsID")

# Define target conditions
target_conditions = ["Diabetes", "Cancer", "Obesity", "Hypertension"]

# Filter and group conditions
def categorize_condition(desc):
    for condition in target_conditions:
        if condition.lower() in desc.lower():
            return condition
    return "Other"

merged_df["FilteredCondition"] = merged_df["Desc"].apply(categorize_condition)

# Calculate percentages
condition_counts = merged_df["FilteredCondition"].value_counts(normalize=True) * 100
condition_counts = condition_counts.reset_index()
condition_counts.columns = ["Condition", "Percentage"]

# Plot the pie chart
plt.figure(figsize=(8, 6))
plt.pie(
    condition_counts["Percentage"],
    labels=condition_counts["Condition"],
    autopct="%1.1f%%",
    startangle=140
)
plt.title("Distribution of Clinical Studies by Condition")
plt.tight_layout()
plt.show()