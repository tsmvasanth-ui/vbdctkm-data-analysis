import pandas as pd
import os

# Set the folder path where your Excel files are stored
folder_path = "C:\\Vasanth\\Fever"

# Column you want to filter
target_column = "Name of the Block"

# Value to filter by (optional)
filter_value = "Thirukkazhukundram"

# Create an empty DataFrame to store results
combined_data = pd.DataFrame()

# Loop through all Excel files in the folder
for file in os.listdir(folder_path):
    if file.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file)
        df = pd.read_excel(file_path)

        # Filter the column (optional: use condition)
        filtered_df = df[[target_column]]
        # If you want to filter by value:
        # filtered_df = df[df[target_column] == filter_value]

        # Append to combined DataFrame
        combined_data = pd.concat([combined_data, filtered_df], ignore_index=True)

# Save the combined data to a new Excel file
combined_data.to_excel("filtered_output.xlsx", index=False)