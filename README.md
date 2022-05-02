#  CLTV Prediction with BG-NBD and Gamma-Gamma

# What is CLTV (Customer Life Time Value)?
It is the total value of a customer for that company over their entire relationship with the company.
CLTV is a prediction of the net profit attributed to an ongoing relationship between customer and product.CLTV helps set marketing budgets and ensures that companies pursue the most effective users.
If a company can predict a user’s lifetime value successfully, it provides marketers with a much better base on which to make decisions 

# CALCULATION
 CLTV = (Customer Value / Churn Rate) * Profit Margin
 
 Customer Value = Average Order Value * Purchase Frequency
 
 Avarage Order Value = Total Price / Total Transaction

 Purchase Frequency = Total Transaction / Total Number of Customer
 
 Churn Rate = 1 - Repeat Rate
 
 Repeat Rate = Number of customers making multiple purchases / Total number of customers
 
 Profit Margin = Total Price * 0.10

# PREDICTION
 
 CLTV = (Customer Value / Churn Rate) * Profit Margin
 
 Customer Value = Purchase Frequency * Average Order Value
 
 CLTV = Expected Number of Transaction * Expected Avarage Profit
 
 CLTV = BGNBD Model * Gamma Gamma Model

# Business Problem
