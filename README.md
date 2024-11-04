# Building an automated data integration between Google Cloud Platform and Play Store App Data using Python

Medium Articles with the complete guide through documentation:
- English version: [Link](https://medium.com/@leofgonzalez/automating-play-store-data-integration-with-bigquery-95bbcb02182f)
- Portuguese version: [Link](https://medium.com/@leofgonzalez/automatizando-a-integra%C3%A7%C3%A3o-de-dados-da-play-store-com-o-bigquery-dbe1ffb26a30)

This repository serves as a comprehensive guide on automating the integration between Google BigQuery and the Play Store using a Google Cloud Function, showcasing the capabilities of Python in data engineering challenges. This project is based on a real-world problem I encountered while working at Ribon, where we aimed to drive B2C growth by understanding the user journey leading to the app download.

## Project Overview
In our efforts to optimize user acquisition, we needed insights into critical metrics from the Play Store, including:

Number of impressions in organic searches
Number of product page views
Number of downloads
Number of installations
We segmented this data by:

Country of origin: During our international expansion into the U.S., we focused on acquiring both U.S. and Brazilian users.
UTM parameters: This allowed us to categorize each campaign and advertisement that brought users to our app.

## Key Sections
Environment Setup and Security Permissions
Utilizing Google Cloud services, the integration is built on a Google Cloud Function, triggered via a Cloud Scheduler CRON job. Essential configurations include:

Region: us-central1
Allocated Memory: 256 MB
Timeout: 540 seconds
Minimum Instances: 0
Maximum Instances: 3000
Runtime: Python 3.9
For a complete setup guide, refer to the Medium article linked above.

Full Integration Code Development in Python
The integration process involves importing necessary libraries, initializing clients, retrieving reports, sanitizing data, and loading it into BigQuery. For the complete Python code, check the repository files: main.py.

Validation and Key Observations
After implementing the code, validation through Google Cloud Platform logs is essential. This helps to ensure the function executes as intended, and allows for debugging and performance monitoring.

## Conclusion
This project exemplifies the efficiency and flexibility of Python in handling complex data engineering tasks. By integrating Play Store metrics into BigQuery, we can leverage these insights for better decision-making in user acquisition strategies.

For a detailed walkthrough of the code and its functionalities, please refer to the Medium article mentioned above.
