import pandas as pd
import os
from rapidfuzz import process

# Folder path
folder_path = r"C:\Vasanth\Fever\Aug"

# Column to filter
target_column = "Name of the Block"

# Value to filter
filter_value = "Thirukkazhukundram"

# Minimum similarity for fuzzy matching
SIMILARITY_THRESHOLD = 80

# DataFrame to store all results
combined_data = pd.DataFrame()

for file in os.listdir(folder_path):
    if file.endswith(".xlsx") and not file.startswith("~$"):
        file_path = os.path.join(folder_path, file)
        try:
            # Header is in row 3 (index 2)
            df = pd.read_excel(file_path, header=2)

            # Standardize column names
            columns = [str(col).strip() for col in df.columns]

            # Fuzzy match to find closest column
            match_tuple = process.extractOne(target_column, columns, score_cutoff=SIMILARITY_THRESHOLD)
            
            if match_tuple:
                match_column = match_tuple[0]
                print(f"✅ Matched column '{match_column}' in file: {file}")

                # Filter complete rows where the column equals the value
                filtered_df = df[df[match_column] == filter_value]
                combined_data = pd.concat([combined_data, filtered_df], ignore_index=True)
            else:
                print(f"⚠️ Column similar to '{target_column}' not found in file: {file}")

        except Exception as e:
            print(f"❌ Could not process file {file}: {e}")

# Save combined filtered data
output_path = os.path.join(folder_path, "filtered_output_Aug.xlsx")
combined_data.to_excel(output_path, index=False)
print(f"✅ Filtered data saved to: {output_path}")
