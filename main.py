import os
from google.cloud import storage, bigquery
import pandas as pd
from pandas_gbq import to_gbq
import io
from collections import defaultdict

# Variable definitions
bucket_name = 'pubsite_prod_rev_XXXXXXXXXXXXXXXXXXXX'
bigquery_dataset = 'XXXXXXXX'
bigquery_project_id = 'XXXXXXXXX'

# Initializing clients through the service account responsible for the operation
storage_client = storage.Client()
bigquery_client = bigquery.Client()

# Function to get a list of all available reports to be read and transferred
def get_reports_list(bucket_name):
    reports_list = []
    try:
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs()

        for blob in blobs:
            reports_list.append(blob.name)
    except Exception as e:
        print(f"Error accessing reports: {e}")

    return reports_list

# Some columns contain special characters that may cause issues when loading into BigQuery
def sanitize_column_names(df):
    df.columns = df.columns.str.replace('[^a-zA-Z0-9_]', '_', regex=True)
    return df

# Select only the reports that were relevant for the moment's challenges
def filter_reports(reports_list):
    filtered_list = []
    for report in reports_list:
        if 'store_performance' in report or 'retained_installers' in report:
            filtered_list.append(report)
    return filtered_list

# Extracting metrics and sub-metrics
def extract_metrics(report_name):
    parts = report_name.split('/')
    try:
        if len(parts) >= 4:
            main_metric = parts[2]
            sub_metric = parts[3].rsplit('_', 1)[-1].replace('.csv', '')
        elif len(parts) == 3:
            main_metric = parts[1]
            sub_metric = parts[2].rsplit('_', 1)[-1].replace('.csv', '')
        else:
            main_metric = parts[1]
            sub_metric = parts[1]
        return main_metric, sub_metric
    except IndexError as e:
        print(f"Error extracting metrics from {report_name}: {e}")
        return None, None

# For each report in the list, download the corresponding files for that report pattern and concatenate different dates into a single DataFrame
def process_and_combine_reports(reports_list):

    combined_data = defaultdict(lambda: defaultdict(list))

    for report_name in reports_list:
        main_metric, sub_metric = extract_metrics(report_name)
        if main_metric is None or sub_metric is None:
            print(f"The report {report_name} was not processed correctly by extract_metrics")
            continue

        try:
            # Download the report
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(report_name)
            report_content = blob.download_as_bytes()

            # Load the report into a pandas DataFrame using UTF-16 encoding
            try:
                actual_report_df = pd.read_csv(io.BytesIO(report_content), encoding='utf-16')
                actual_report_df = sanitize_column_names(actual_report_df)

                # Adjust the name of the first column to 'created_at' (Date would disrupt queries)
                actual_report_df.rename(columns={actual_report_df.columns[0]: 'created_at'}, inplace=True)

                # Remove the 'package_name' column if it exists (not useful)
                if 'package_name' in actual_report_df.columns:
                    actual_report_df.drop('package_name', axis=1, inplace=True)

                combined_data[main_metric][sub_metric].append(actual_report_df)

            except Exception as e:
                print(f"Error reading {report_name} with encoding 'utf-16': {e}")
                continue

        except Exception as e:
            print(f"Error processing report {report_name}: {e}")

    return combined_data

# Load each report from the combined_data dictionary, which groups concatenated data from various reports, into BigQuery
def load_combined_data_to_bigquery(combined_data):
    for main_metric, sub_metrics in combined_data.items():
        for sub_metric, dataframes in sub_metrics.items():
            combined_df = pd.concat(dataframes, ignore_index=True)
            table_name = f"{main_metric}_{sub_metric}"
            dataset_table = f"{bigquery_dataset}.{table_name}"

            try:
                to_gbq(combined_df, dataset_table, project_id=bigquery_project_id, if_exists='replace')
                print(f"Data successfully loaded for metrics: {main_metric}/{sub_metric} with: {combined_df.shape[0]} rows in BigQuery.")
            except Exception as e:
                print(f"Error loading metrics: {main_metric}/{sub_metric} into BigQuery, error description: {e}")

def get_data(request):
        try:
            
            # Variable that holds the complete list of reports
            reports_list = get_reports_list(bucket_name)

            # Filter reports from the complete list, selecting only those that are relevant to us based on the key names above ('store_performance' and 'retained_installers')
            filtered_reports_list = filter_reports(reports_list)

            # Process and load all reports into BigQuery
            combined_data = process_and_combine_reports(filtered_reports_list)
            load_combined_data_to_bigquery(combined_data)

            return {"message": "Data loading completed."}
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return {"error":str(e)}
