import os
import pandas as pd
 
# 1. Read the original Excel file
df = pd.read_excel("data/raw/Online Retail.xlsx")
 
# 2. Convert the date column to a date/time type
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)
 
# 3. Print the audit information
print("Original row count:", len(df))
print("\nColumn types:")
print(df.dtypes)
 
print("\nDate coverage:")
print(df["InvoiceDate"].min(), "to", df["InvoiceDate"].max())
 
print("\nMissing values:")
print(df.isna().sum())
 
print("\nDuplicate rows:", df.duplicated().sum())
 
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
print("Cancelled invoice rows:", cancelled.sum())
 
print("Rows with non-positive quantity:",
      (df["Quantity"] <= 0).sum())
 
print("Rows with non-positive unit price:",
      (df["UnitPrice"] <= 0).sum())
 
# 4. Make a copy so the original data stays unchanged
clean = df.copy()
 
# 5. Remove exact duplicate rows
clean = clean.drop_duplicates()
 
# 6. Exclude cancelled invoices
clean = clean[
    ~clean["InvoiceNo"].astype(str).str.startswith("C")
]
 
# 7. Keep positive quantities and prices, and valid dates
clean = clean[
    (clean["Quantity"] > 0) &
    (clean["UnitPrice"] > 0) &
    (clean["InvoiceDate"].notna())
]
 
# 8. Keep records with an identifiable customer ID
clean = clean.dropna(subset=["CustomerID"])
 
# 9. Calculate the value of each transaction line
clean["Revenue"] = clean["Quantity"] * clean["UnitPrice"]
 
# 10. Create the output folder and save the cleaned data
print("\nRows after cleaning:", len(clean))
os.makedirs("data/processed", exist_ok=True)
clean.to_csv("data/processed/cleaned_retail.csv", index=False)
 
print("Cleaned data saved in data/processed/cleaned_retail.csv")

# Use one day after the latest valid transaction as the reference date
reference_date = clean["InvoiceDate"].max() + pd.Timedelta(days=1)
 
# Create one row per customer
rfm = clean.groupby("CustomerID").agg(
    Last_Purchase=("InvoiceDate", "max"),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
).reset_index()
 
# Calculate recency in days
rfm["Recency"] = (
    reference_date - rfm["Last_Purchase"]
).dt.days
 
# Save the customer-level table
rfm.to_csv("data/processed/customer_rfm.csv", index=False)
 
print(rfm.head())
print("Number of identifiable customers:", rfm["CustomerID"].nunique())


# Create scores from 1 (lower) to 5 (higher).
# For Recency, a lower number of days is better,
# so the labels are reversed.
 
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)
 
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)
 
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)
 
# Define three specific groups.
# Customers who do not match these rules become Low-engagement.
conditions = [
    (rfm["R_Score"] >= 4) &
    (rfm["F_Score"] >= 4) &
    (rfm["M_Score"] >= 4),
 
    (rfm["R_Score"] >= 4) &
    (rfm["F_Score"] <= 2),
 
    (rfm["R_Score"] <= 2) &
    (rfm["F_Score"] >= 3)
]
 
labels = [
    "High-value loyal",
    "Recently active",
    "At-risk"
]
 
import numpy as np
 
rfm["Segment"] = np.select(
    conditions,
    labels,
    default="Low-engagement"
)
 
rfm.to_csv("data/processed/customer_segments.csv", index=False)
 
print(rfm["Segment"].value_counts())

# Overall business totals
total_customers = rfm["CustomerID"].nunique()
total_orders = clean["InvoiceNo"].nunique()
total_revenue = clean["Revenue"].sum()
 
print("Identifiable customers:", total_customers)
print("Distinct valid orders:", total_orders)
print("Total purchasing value (£):", round(total_revenue, 2))
 
# Summary for each segment
segment_summary = rfm.groupby("Segment").agg(
    Customer_Count=("CustomerID", "count"),
    Average_Recency=("Recency", "mean"),
    Average_Frequency=("Frequency", "mean"),
    Average_Spending=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum")
)
 
segment_summary["Revenue_Percentage"] = (
    segment_summary["Total_Revenue"] /
    segment_summary["Total_Revenue"].sum() * 100
)
 
print("\nSegment summary:")
print(segment_summary.round(2))
 
segment_summary.to_csv(
    "data/processed/segment_analysis.csv"
)

import os
import matplotlib.pyplot as plt
 
os.makedirs("reports/figures", exist_ok=True)
 
# Chart 1: Number of customers in each segment
rfm["Segment"].value_counts().plot(kind="bar", figsize=(8, 5))
plt.title("Number of Customers by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("reports/figures/customer_counts.png")
plt.close()
 
# Chart 2: Total revenue by segment
segment_summary["Total_Revenue"].sort_values(ascending=False).plot(
    kind="bar", figsize=(8, 5)
)
plt.title("Total Revenue by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("reports/figures/revenue_by_segment.png")
plt.close()
 
# Chart 3: Average spending by segment
segment_summary["Average_Spending"].plot(kind="bar", figsize=(8, 5))
plt.title("Average Customer Spending by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Average Spending (£)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("reports/figures/average_spending.png")
plt.close()
 
# Chart 4: Recency against frequency
for name in rfm["Segment"].unique():
    part = rfm[rfm["Segment"] == name]
    plt.scatter(part["Recency"], part["Frequency"], label=name, alpha=0.5)
 
plt.title("Customer Recency vs Frequency")
plt.xlabel("Recency (days)")
plt.ylabel("Number of Orders")
plt.legend()
plt.tight_layout()
plt.savefig("reports/figures/recency_frequency.png")
plt.close()
 
print("Four charts saved in reports/figures/")