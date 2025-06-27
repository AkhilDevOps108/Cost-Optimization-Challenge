# Cost-Optimization-Challenge
Cost Optimization Challenge: Managing Billing Records in Azure Serverless Architecture
# Azure Cost Optimization: Billing Record Archival

This solution demonstrates a cost-saving approach for storing infrequently accessed billing records using Azure Cosmos DB and Blob Storage.

## Key Features
- Retain hot data in Cosmos DB
- Archive old data to Blob Storage
- No API changes required
- Fast reads even for old records
- Fully serverless using Azure Functions

## Folder Structure
- `archive-job/`: Azure Function for daily archival
- `read-proxy/`: API-compatible reader with fallback to blob
