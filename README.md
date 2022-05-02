#  CLTV Prediction with BG-NBD and Gamma-Gamma

# What is CLTV (Customer Life Time Value)?

It is the total value of a customer for that company over their entire relationship with the company.

CLTV is a prediction of the net profit attributed to an ongoing relationship between customer and product.CLTV helps set marketing budgets and ensures that companies pursue the most effective users.

If a company can predict a user’s lifetime value successfully, it provides marketers with a much better base on which to make decisions 

# Calculation

 CLTV = (Customer Value / Churn Rate) * Profit Margin
 
 Customer Value = Average Order Value * Purchase Frequency
 
 Avarage Order Value = Total Price / Total Transaction

 Purchase Frequency = Total Transaction / Total Number of Customer
 
 Churn Rate = 1 - Repeat Rate
 
 Repeat Rate = Number of customers making multiple purchases / Total number of customers
 
 Profit Margin = Total Price * 0.10

# Prediction
 
 CLTV = (Customer Value / Churn Rate) * Profit Margin
 
 Customer Value = Purchase Frequency * Average Order Value
 
 CLTV = Expected Number of Transaction * Expected Avarage Profit
 
 CLTV = BGNBD Model * Gamma Gamma Model

# Business Problem

 Company wants to set a roadmap for sales and marketing activities.
 
 In order for the company to make a medium-long-term plan, it is necessary to estimate the potential value that existing customers will provide to the company in the future.
 
# Dataset Story

 The dataset is based on the past shopping behavior of customers who made their last purchases from OmniChannel (both online and offline) in 2020 - 2021.
 consists of the information obtained.

 master_id: Unique client number
 
 order_channel : Which channel of the shopping platform is used (Android, ios, Desktop, Mobile, Offline)
 
 last_order_channel : The channel where the last purchase was made
 
 first_order_date : The date of the customer's first purchase
 
 last_order_date : The date of the last purchase made by the customer
 
 last_order_date_online : The date of the last purchase made by the customer on the online platform
 
 last_order_date_offline : The date of the last purchase made by the customer on the offline platform
 
 order_num_total_ever_online : The total number of purchases made by the customer on the online platform
 
 order_num_total_ever_offline : Total number of purchases made by the customer offline
 
 customer_value_total_ever_offline : The total price paid by the customer for offline shopping
 
 customer_value_total_ever_online : The total price paid by the customer for their online shopping
 
 interested_in_categories_12 : List of categories that the customer has shopped in the last 12 months
 
 store_type : It represents 3 different companies. If the person who shopped from company A made it from company B, it was written as A, B.
