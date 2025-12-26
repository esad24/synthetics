import pandas as pd
import os

csv = "images_artifacts.csv"

def final_sort_csv(input_path, output_path):
    try:
        # 1. Load the CSV
        if not os.path.exists(input_path):
            print(f"Error: '{input_path}' not found.")
            return

        # keep_default_na=False reads empty fields as empty strings "" instead of NaN
        df = pd.read_csv(input_path, keep_default_na=False)

        # 2. Clean headers (remove accidental spaces)
        df.columns = df.columns.str.strip()

        # 3. Ensure 'fake' is a number for correct sorting (1 vs 0)
        df['fake'] = pd.to_numeric(df['fake'], errors='coerce').fillna(0)

        # --- UPDATE START: The "Realness Wiper" ---
        # Requirement: If fake=0 (Real), all other columns (except filename) must be empty.
        print("Wiping extra data for real images (fake=0)...")
        
        # Define which columns should NOT be wiped (The identifier and the label)
        cols_to_keep = ['filename', 'fake']
        
        # Identify all other columns in the CSV
        cols_to_wipe = [c for c in df.columns if c not in cols_to_keep]

        # Find rows where fake is 0 and set the target columns to empty string
        df.loc[df['fake'] == 0, cols_to_wipe] = ""
        # --- UPDATE END ---

        # 4. Create a helper column for sorting: 'has_match'
        target_col = 'fake_or_real'
        
        # Check if the column exists
        if target_col in df.columns:
            # Create a True/False column: True if the cell contains any text
            df['has_match'] = df[target_col].astype(str).str.strip().str.len() > 0
        else:
            print(f"Warning: '{target_col}' column missing. Sorting only by 'fake'.")
            df['has_match'] = False

        # 5. The Sorting Logic
        # Primary Sort: 'fake' (Descending) -> 1 (Fake) comes before 0 (Real)
        # Secondary Sort: 'has_match' (Descending) -> True (Has Data) comes before False (Empty)
        df_sorted = df.sort_values(by=['fake', 'has_match'], ascending=[False, False])

        # 6. Cleanup
        # Remove the temporary helper column before saving
        df_sorted = df_sorted.drop(columns=['has_match'])

        # 7. Save
        df_sorted.to_csv(output_path, index=False)
        
        print(f"Success! Saved to: {output_path}")
        print("Order of rows:")
        print("1. Fakes with detailed data")
        print("2. Fakes with NO detailed data")
        print("3. Reals (Data wiped, appearing at the bottom)")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    final_sort_csv(csv, 'images_artifacts_final_final.csv')
