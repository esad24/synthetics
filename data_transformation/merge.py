import pandas as pd

csv1 = "image_metadata.csv"
csv2 = "artifact_annotations.csv"
csv3 = "images_artifacts.csv"


def merge_csvs(file1_path, file2_path, output_path):
    try:
        # 1. Load the CSV files
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)

        # Function to clean a DataFrame
        def clean_dataframe(df):
            # 1. Strip spaces from column names (headers)
            # e.g., " filename " -> "filename"
            df.columns = df.columns.str.strip()
            
            # 2. Strip spaces from all string/text values in the rows
            # We select only columns that contain text ('object')
            df_obj = df.select_dtypes(['object'])
            
            # Apply the strip function to these text columns
            df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
            
            return df

        print("Cleaning whitespace from files...")
        df1 = clean_dataframe(df1)
        df2 = clean_dataframe(df2)
        
        # --- CLEANING STEP END ---


        # 2. Perform the Merge (Left Join)
        # on='filename': The common column to match lines
        # how='left': Keep all rows from df1. If a row in df1 matches df2, 
        #             add df2's data. If not, fill df2's columns with empty values (NaN).
        print("Merging data...")
        df3 = pd.merge(df1, df2, on='filename', how='left')

        # 3. Optional: Clean up "Empty" values
        # By default, pandas uses 'NaN' for missing data. 
        # If you want them to be actual empty strings "" in the CSV:
        df3 = df3.fillna("")

        # 4. Save to a new CSV file
        df3.to_csv(output_path, index=False)
        
        print(f"Success! Created {output_path} with {len(df3)} rows.")
        print("Preview of the first 5 rows:")
        print(df3.head())

    except FileNotFoundError as e:
        print(f"Error: Could not find one of the files. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the function ---
if __name__ == "__main__":
    # Change these filenames if your actual files are named differently
    merge_csvs(csv1, csv2, csv3)