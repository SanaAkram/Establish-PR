import csv


def clean_and_save_data(input_filename, output_filename='cleaned_scrapped_data.csv'):
    # Function to convert list to string with semicolons
    def list_to_string(lst):
        return '; '.join(lst)

    cleaned_data = []

    # Try different encodings if UTF-8 fails
    encodings = ['utf-8', 'latin-1', 'utf-16']

    for encoding in encodings:
        try:
            with open(input_filename, 'r', newline='', encoding=encoding) as csvfile:
                csvreader = csv.DictReader(csvfile)

                for row in csvreader:
                    full_name = row['full_name']
                    first_name = row['first_name']
                    last_name = row['last_name']
                    company = row['company']

                    # Attempt to evaluate lists safely
                    try:
                        regions = eval(row['Region(s)'])
                        stages = eval(row['Stages'])
                        industries = eval(row['Industries'])
                    except:
                        regions = []
                        stages = []
                        industries = []

                    # Convert lists to strings
                    regions_str = list_to_string(regions)
                    stages_str = list_to_string(stages)

                    # Remove regions that are in industries list
                    cleaned_industries = [industry for industry in industries if industry not in regions]
                    industries_str = list_to_string(cleaned_industries)

                    cleaned_data.append({
                        'full_name': full_name,
                        'first_name': first_name,
                        'last_name': last_name,
                        'company': company,
                        'Region(s)': regions_str,
                        'Stages': stages_str,
                        'Industries': industries_str
                    })
            break
        except UnicodeDecodeError:
            print(f"Failed to decode with encoding {encoding}, trying next encoding...")
        except Exception as e:
            print(f"An error occurred: {e}")
            return

    # Save cleaned data to CSV
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['full_name', 'first_name', 'last_name', 'company', 'Region(s)', 'Stages', 'Industries']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        csvwriter.writerows(cleaned_data)


# Example usage
input_filename = 'scrapped_data.csv'  # Replace with your input CSV file name
clean_and_save_data(input_filename)
