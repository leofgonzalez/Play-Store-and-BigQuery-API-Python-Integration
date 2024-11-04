# Building an automated data integration between Google Cloud Platform and Play Store App Data using Python

This repository contains a comprehensive, practical guide to automating data integration between Google BigQuery and Play Store metrics via Google Cloud Functions. Using Python, this project tackles real-world data engineering challenges to provide actionable insights into app user behavior and drive B2C growth—a necessity I encountered while working at Ribon.

Medium Articles with the complete guide through documentation:
- English version: [Link](https://medium.com/@leofgonzalez/automating-play-store-data-integration-with-bigquery-95bbcb02182f)
- Portuguese version: [Link](https://medium.com/@leofgonzalez/automatizando-a-integra%C3%A7%C3%A3o-de-dados-da-play-store-com-o-bigquery-dbe1ffb26a30)

## Project Overview

This project automates the integration of Play Store metrics into Google BigQuery to enhance user acquisition insights. Key data points include:

- Metrics: Impressions, page views, downloads, and installations.
- Segmentation:
- - Country (focused on the U.S. and Brazil for expansion).
- - UTM Parameters (categorizing user acquisition sources).

The integration, built with Python on Google Cloud Functions, provides a scalable and efficient way to gather and analyze app performance data for better decision-making in growth strategies.

## Key Sections
Environment Setup and Security Permissions
Utilizing Google Cloud services, the integration is built on a Google Cloud Function, triggered via a Cloud Scheduler CRON job. Essential configurations include:

Full Integration Code Development in Python
The integration process involves importing necessary libraries, initializing clients, retrieving reports, sanitizing data, and loading it into BigQuery. For the complete Python code, check the repository files: main.py.

Validation and Key Observations
After implementing the code, validation through Google Cloud Platform logs is essential. This helps to ensure the function executes as intended, and allows for debugging and performance monitoring.

## Conclusion
This project exemplifies the efficiency and flexibility of Python in handling complex data engineering tasks. By integrating Play Store metrics into BigQuery, we can leverage these insights for better decision-making in user acquisition strategies.

For a detailed walkthrough of the code and its functionalities, please refer to the Medium article mentioned above.
