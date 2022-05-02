# CLTV Prediction with BG-NBD and Gamma-Gamma


# Preparing Data

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

# 1. Read the OmniChannel.csv data. Creating a copy of the dataframe.
df_ = pd.read_csv('databases/flo_data_20k.csv')
df = df_.copy()

#2. Define the outlier_thresholds and replace_with_thresholds functions needed to suppress outliers.
# Note: When calculating cltv, frequency values ​​must be integers. Therefore, the lower and upper limits are rounded with round().
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = round(quartile3 + 1.5 * interquantile_range)
    low_limit = round(quartile1 - 1.5 * interquantile_range)
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

# 3. Set the variables "order_num_total_ever_online","order_num_total_ever_offline","customer_value_total_ever_offline","customer_value_total_ever_online"
# was the one that suppressed outliers.

df.describe().T
df.head()
df.isnull().sum()

columns = ["order_num_total_ever_online", "order_num_total_ever_offline", "customer_value_total_ever_offline",
           "customer_value_total_ever_online"]
for col in columns:
    replace_with_thresholds(df, col)

# 4. Omnichannel means that customers shop from both online and offline platforms.
# New variables have been created for the total number of purchases and spending of each customer.

df["TotalValue"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
df["TotalOrder"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]



# 5. Examine the variable types. Change the type of variables that express date to date.

date_columns = df.columns[df.columns.str.contains("date")]
df["first_order_date"] = pd.to_datetime(df["first_order_date"])
df["last_order_date"] = pd.to_datetime(df["last_order_date"])

df.dtypes
df.shape

#Creating the CLTV Data Structure

#1. Analysis date was taken 2 days after the date of the last purchase in the data set.

today_date = df["last_order_date"].max() + dt.timedelta(days=2)
type(today_date)
df["recency"] = (df["last_order_date"] - df["first_order_date"]).dt.days
df["T"] = (today_date - df["first_order_date"]).dt.days
# 2.customer_id, recency_cltv_weekly, T_weekly, frequency ve monetary_cltv_avg değerlerinin yer aldığı yeni bir cltv dataframe'i oluşturunuz.

cltv_df = df.groupby('master_id').agg(
    {'recency': lambda recency: recency.values,
     "T": lambda T: T.values,
     'TotalOrder': lambda TotalOrder: TotalOrder.values,
     "TotalValue": lambda TotalValue: TotalValue.values})

cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']

cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]

cltv_df.describe().T #inspection of cltv_df

#3. BG/NBD, Establishment of Gamma-Gamma Models, Calculation of 6-month CLTV

cltv_df = cltv_df[(cltv_df['recency'] > 0)]

cltv_df = cltv_df[(cltv_df['frequency'] > 1)]

cltv_df["recency"] = cltv_df["recency"] / 7 #This must be week so divided to 7

cltv_df["T"] = cltv_df["T"] / 7 #This must be week so divided to 7



bgf = BetaGeoFitter(penalizer_coef=0.001)

bgf.fit(cltv_df['frequency'],
        cltv_df['recency'],
        cltv_df['T'])


#4.Estimate expected purchases from customers in 3 months and added to cltv dataframe as exp_sales_3_month.

bgf.predict(12,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)

cltv_df["expected_purc_3_month"] = bgf.predict(12,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])



#5. Estimate expected purchases from customers in 6 months and added to cltv dataframe as exp_sales_3_month.
bgf.predict(24,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)

#6.  The 10 people who will make the most purchases in the 3rd and 6th months were reviewed.

cltv_df.sort_values("exp_sales_3_month", ascending=False)[:10]

cltv_df.sort_values("exp_sales_6_month", ascending=False)[:10]

plot_period_transactions(bgf)
plt.show()

#7.  Gamma-Gamma model fitted. It was added to the cltv dataframe as exp_average_value by estimating the average value of the customers.

ggf = GammaGammaFitter(penalizer_coef=0.01)

ggf.fit(cltv_df['frequency'], cltv_df['monetary'])

ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary']).head(10)

cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                       cltv_df['monetary'])
# 7. Calculated 6 months CLTV and add it to the dataframe with the name cltv.

cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df['frequency'],
                                   cltv_df['recency'],
                                   cltv_df['T'],
                                   cltv_df['monetary'],
                                   time=6,  # 6 months
                                   freq="W",  # frequency of T
                                   discount_rate=0.01)


cltv.head()
cltv = cltv.reset_index()

cltv_final = cltv_df.merge(cltv, on="master_id", how="left")

#Observed the 20 people with the highest CLTV value.

cltv_final.sort_values(by="clv", ascending=False).head(20)


#Creating Segments by CLTV


#1. According to 6-month CLTV, all your customers were divided into 4 groups (segments) and their group names were added to the dataset.


cltv_final["segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])

#Does it make sense to divide customers into 4 groups based on CLTV scores? A piece of code is used to interpret whether it should be less or more.

cltv_final.groupby("segment").agg(
    {"count", "mean", "sum"})
