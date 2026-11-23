## Business Recomendations

Campaign 1: VIP Loyalty Rewards
The high-valu loyal customers contribute 64.56% of total revenue, and represent about 21.7% of the identified customer

Recomendation: Introduce loyalty points, exclusive discount or special offer.

Trade-off: Reward cost money, and may reduce profit margins so test cost befor making the program parmanent

Campaign 2: Win-back Campaign
661 are at-risk custormars, contributing 9.27% revenue

Recomendation: Send personalized emails with a special return offer or product recommendation

Trade-off: Some customers may not responed, even when offered discount.

Campaign 3: Second purchase offer
310 resently active customers, conttributing 1.60% revenue

Recomendation: Send a follow-up message with a carefully selected product recomendation or a second-purchase incentive.


Trade-off: The cost of the incentive may exceed the additional revenue generation.


## 1. Business Summary

This project uses Python to analyse historical online retail transactions, understand customer purchasing behaviour and group customers using Recency, Frequency and Monetary (RFM) analysis. The analysis identified 4,338 customers and 18,532 valid orders, with total purchasing value of £8,887,208.89. High-value loyal customers generated the largest revenue share (64.56%).

## 2. Dataset and Data Cleaning

Dataset: UCI Online Retail Dataset (1 December 2010–9 December 2011). It contains invoice, product, quantity, date, price, customer and country fields.
Cleaning included:
•	Removing duplicate records and cancelled invoices.
•	Excluding non-positive quantities and unit prices.
•	Excluding records without CustomerID from customer-level analysis.
•	Converting invoice dates and calculating revenue as quantity × unit price.
The cleaned dataset contains 392,692 transaction rows and is saved as data/processed/cleaned_retail.csv.

## 3. Customer Segmentation Results

Customers were scored using Recency (how recently they purchased), Frequency (how often they purchased) and Monetary value (how much they spent). Predefined RFM rules assigned customers to four segments:
Customer segment	Customers	Revenue share
High-value loyal	942	64.56%
Low-engagement	2,425	24.56%
At-risk	661	9.27%
Recently active	310	1.60%
Total	4,338	99.99%*
*Revenue shares total 99.99% because of rounding.

## 4. Business Recommendations

•	VIP Loyalty Rewards — High-value loyal customers: Offer loyalty points, exclusive benefits or tailored rewards to encourage retention.
•	Win-back Campaign — At-risk customers: Use personalised messages, product suggestions or carefully tested return offers.
•	Second-purchase Incentive — Recently active customers: Send follow-up recommendations or a targeted incentive to encourage another purchase.
These are proposed campaigns; their effectiveness and profitability should be tested.

## 5. Data Visualizations

The project generated four charts in reports/figures/: customer_counts.png, revenue_by_segment.png, average_spending.png and recency_frequency.png.
The two summary charts below are recreated from the exact customer counts and revenue percentages shown in the analysis output. The other two project charts remain available in the project's reports/figures folder.
 
 
## 6. Project Limitations

•	The dataset is historical and does not represent a retailer's current performance.
•	Records without customer IDs were excluded from customer-level segmentation.
•	Segments use predefined RFM rules; they were not discovered by a machine-learning clustering model.
•	The analysis describes past behaviour and cannot guarantee future purchases.
•	The recommended campaigns have not yet been implemented or evaluated.
