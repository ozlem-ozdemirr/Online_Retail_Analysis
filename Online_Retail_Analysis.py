# 1. Libraries
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

sns.set(style='whitegrid')
%matplotlib inline

# 2. Data Loading 
df = pd.read_excel('Online Retail.xlsx')
print(f"Total number of records in the dataset: {df.shape[0]}")

print("\nTop 5 Records:")
display(df.head())

print("\nDataset Column Information:")
print(df.info())

# 3. Data Cleansing
df_clean = df[(df['Quantity'] > 0) & (df['CustomerID'].notnull())].copy()
print(f"\nNumber of Records in the Cleaned Dataset: {df_clean.shape[0]}")

# 4. General Information About the Data
print(f"Total Number of Unique Customers: {df_clean['CustomerID'].nunique()}")
print(f"Total Number of Unique Products: {df_clean['Description'].nunique()}")

# 5. RFM Analysis
today_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df_clean.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (today_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'Quantity': 'sum'
}).rename(columns={'InvoiceDate': 'Recency',
                   'InvoiceNo': 'Frequency',
                   'Quantity': 'Monetary'})

# Calculating RFM Scores
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'], 5, labels=[1,2,3,4,5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5]).astype(int)

rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

def segment(x):
    if x.startswith('5'):
        return 'Top Customers'
    elif x.startswith('4'):
        return 'Loyal Customers'
    elif x.startswith('3'):
        return 'Mid-Level Customers'
    else:
        return 'Low-Value Customers'

rfm['Segment'] = rfm['RFM_Score'].apply(segment)

print("\nCustomer Segment Distribution:")
print(rfm['Segment'].value_counts())

plt.figure(figsize=(10,6))
sns.countplot(data=rfm, x='Segment', order=rfm['Segment'].value_counts().index)
plt.title('Customer Segment Distribution')
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.show()

# 6. Time-Based Sales Analysis
df_clean['InvoiceMonth'] = df_clean['InvoiceDate'].dt.to_period('M')
monthly_sales = df_clean.groupby('InvoiceMonth')['Quantity'].sum()

plt.figure(figsize=(12,5))
monthly_sales.plot(marker='o')
plt.title('Monthly Sales Quantity')
plt.xlabel('Month')
plt.ylabel('Sales Quantity')
plt.show()

df_clean['InvoiceWeek'] = df_clean['InvoiceDate'].dt.to_period('W')
weekly_sales = df_clean.groupby('InvoiceWeek')['Quantity'].sum()

plt.figure(figsize=(12,5))
weekly_sales.plot(marker='o', color='orange')
plt.title('Weekly Sales Quantity')
plt.xlabel('Week')
plt.ylabel('Sales Quantity')
plt.show()

df_clean['InvoiceDay'] = df_clean['InvoiceDate'].dt.to_period('D')
daily_sales = df_clean.groupby('InvoiceDay')['Quantity'].sum()

plt.figure(figsize=(12,5))
daily_sales.plot(marker='.', color='green')
plt.title('Daily Sales Quantity')
plt.xlabel('Gün')
plt.ylabel('Sales Quantity')
plt.show()

# 7. Market Basket Analysis
transactions = df_clean.groupby('InvoiceNo')['Description'].apply(list).values.tolist()

te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

print(f"Total Number of Transactions (Invoices): {len(transactions)}")
print(f"Total Number of Product Types: {len(te.columns_)}")

frequent_itemsets = apriori(df_encoded, min_support=0.01, use_colnames=True)
frequent_itemsets.sort_values(by='support', ascending=False, inplace=True)

print("\nMost Frequent Product Sets:")
print(frequent_itemsets.head(10))

rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.6)
rules = rules.sort_values(by='confidence', ascending=False)

print("\nStrongest Association Rules:")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

strong_rules = rules[rules['lift'] > 1.2]

print("\nLift > 1.2 rules with the highest lift value:")
print(strong_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].sort_values('lift', ascending=False).head(10))

plt.figure(figsize=(10,6))
sns.scatterplot(x='support', y='confidence', size='lift', data=rules, legend=False, sizes=(20, 200))
plt.title('Association Rules: Support vs Confidence')
plt.xlabel('Support')
plt.ylabel('Confidence')
plt.show()
