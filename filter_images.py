import pandas as pd
import os
import shutil


def organize_and_rename_images(csv_path, image_source_folder, output_base_folder):
    try:
        # --- 1. Setup ---
        if not os.path.exists(csv_path):
            print(f"Error: CSV file '{csv_path}' not found.")
            return
        if not os.path.exists(image_source_folder):
            print(f"Error: Image source folder '{image_source_folder}' not found.")
            return

        # Create output directories if they don't exist
        real_folder = os.path.join(output_base_folder, 'real')
        fake_folder = os.path.join(output_base_folder, 'fake')
        os.makedirs(real_folder, exist_ok=True)
        os.makedirs(fake_folder, exist_ok=True)

        # --- 2. Load and Clean CSV ---
        # keep_default_na=False ensures empty fields are strings "" rather than NaN
        df = pd.read_csv(csv_path, keep_default_na=False)

        # Clean column headers (remove spaces)
        df.columns = df.columns.str.strip()

        # Clean string values (remove spaces from text cells)
        df_obj = df.select_dtypes(['object'])
        df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

        # Ensure 'fake' is numeric for logic
        df['fake'] = pd.to_numeric(df['fake'], errors='coerce').fillna(0)

        # Define the artifact columns to check
        artifact_cols = ['anatomical', 'stylistic', 'functional', 'law_of_physics', 'sociocultural']

        # Counters for summary
        processed_count = 0
        missing_count = 0

        print(f"Processing {len(df)} rows...")

        # --- 3. Iterate through rows ---
        for index, row in df.iterrows():
            original_filename = row['filename']
            
            # Skip if filename is empty
            if not original_filename:
                continue

            # Construct Source Path
            source_path = os.path.join(image_source_folder, original_filename)

            if not os.path.exists(source_path):
                print(f"Warning: Image not found: {original_filename}")
                missing_count += 1
                continue

            is_fake = (row['fake'] == 1)

            """
            # --- 4. Construct New Filename ---
            # Format: type_generator_artifacts_filename
            
            # Part A: Type (Real/Fake)



            file_type = "fake" if is_fake else "real"
            
            # Part B: Generator
            # Only add if it has a value
            generator = str(row.get('generator', ''))
            
            # Part C: Artifacts
            # Collect names of columns where value is 1 (or "1", or "True")
            active_artifacts = []
            for col in artifact_cols:
                # Get value, convert to string to be safe against mixed types (0 vs "0")
                val = str(row.get(col, '0')).lower()
                # Check if it represents "True" or "1"
                if val in ['1', '1.0', 'true', 'yes']:
                    active_artifacts.append(col)
            
            # Join artifacts with underscore (e.g., "anatomical_stylistic")
            artifacts_str = "_".join(active_artifacts)

            # --- 5. Assemble the Name ---
            # We use a list and filter out empty strings to avoid double underscores (e.g. fake__filename)
            name_parts = [file_type, generator, artifacts_str, original_filename]
            # Filter out empty strings
            name_parts = [part for part in name_parts if part]
            
            new_filename = "_".join(name_parts)
            
            """

            # --- 6. Copy File ---
            target_folder = fake_folder if is_fake else real_folder
            target_path = os.path.join(target_folder, original_filename)

            try:
                shutil.copy2(source_path, target_path)
                processed_count += 1
            except Exception as e:
                print(f"Error copying {original_filename}: {e}")

        # --- 7. Summary ---
        print("-" * 30)
        print(f"Done!")
        print(f"Images copied: {processed_count}")
        print(f"Images missing: {missing_count}")
        print(f"Output location: {output_base_folder}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Run the function ---
if __name__ == "__main__":
    # INPUTS
    csv_file = 'images_artifacts_final.csv'  # Your result from the previous step
    input_image_folder = 'stimuli' # Folder where your raw images are currently
    output_folder = 'images_real_fake'  # Where the new folders will be created

    organize_and_rename_images(csv_file, input_image_folder, output_folder)