# Online_Retail_Analysis
## Objective
#### The main goal of this project is to analyze an online retail dataset to gain insights into customer behavior, segment customers based on their purchasing patterns, and discover associations between products using market basket analysis. This enables better marketing strategies, personalized offerings, and improved inventory management.

## 1. Data Loading
#### - The dataset is loaded from an Excel file named Online Retail.xlsx.

#### - The structure, size, and top records of the dataset are examined to understand the raw data.

## 2. Data Cleansing
#### - Only transactions with positive quantities and non-null CustomerID values are kept.

#### - This ensures the analysis focuses on valid, completed transactions by identifiable customers.

## 3. General Data Overview
### Key stats are computed:

#### - Unique Customers: Number of distinct customers.

#### - Unique Products: Number of distinct items/products.

## 4. RFM Analysis
### This section segments customers based on Recency, Frequency, and Monetary value:

#### - Recency: Days since last purchase.

#### - Frequency: Number of transactions.

#### - Monetary: Total quantity of products purchased.

#### Each metric is scored on a scale of 1 to 5 and combined into an RFM_Score.

#### Customers are categorized into segments such as: Top Customers, Loyal Customers, Mid-Level Customers, Low-Value Customers. A bar chart visualizes the distribution of customers across these segments.

## 5. Time-Based Sales Analysis
### Analyzes sales quantity trends over: Months, Weeks, Days. This helps to identify patterns in sales volume over time using time-series plots.

## 6. Market Basket Analysis
### Identifies frequently bought-together products using the Apriori algorithm:
#### - Transactions are converted into a list of product sets per invoice.

#### - A one-hot encoded DataFrame is created for product combinations.

#### - Frequent itemsets are mined based on minimum support.

#### Association rules are generated and evaluated based on: Support, Confidence, Lift. Rules with high lift (>1.2) are highlighted as strong associations. A scatter plot is created to visualize the relationship between support and confidence, sized by lift.

## Conclusion
### This project provides a comprehensive analytical workflow, including:

#### - Customer segmentation via RFM analysis.

#### - Sales trend analysis over different timeframes.

#### - Product bundling opportunities via market basket analysis.

#### - Such analysis is valuable for customer relationship management (CRM), targeted marketing, and inventory optimization.
