"""Main module."""

import pandas as pd
import numpy as np
import os


def define_boundaries(df, variable,q1=0.05,q2=0.95):# the boundaries are the quantiles
    """Detect outliers based on quantiles.

    Parameters
    ----------
    df : pandas DataFrame
        
    variable : String
            column in df
        
    q1 : float number between 0 and 1
         (Default value = 0.05)
    q2 : float number between 0 and 1
         (Default value = 0.95)

    Returns
    -------
    lower_boundary : {float, int}
                    lower quantile
    upper_boundary : {float, int}
                    upper quantile

    """
    lower_boundary = df[variable].quantile(q1) # lower quantile
    upper_boundary = df[variable].quantile(q2) # upper quantile
    return upper_boundary, lower_boundary


def drop_outliers(df,variable):
    """Drop outliers based on quantiles.

    Parameters
    ----------
    df : pandas DataFrame
        
    variable : String
            column in df
        

    Returns
    -------

    """
    upper_boundary,lower_boundary =  define_boundaries(df,variable)
    df[variable] = np.where(df[variable] > upper_boundary, upper_boundary,
                       np.where(df[variable] < lower_boundary, lower_boundary, df[variable]))

def rfm_calculation(filepath, customerID = 'CustomerID',quantity = 'Quantity', unitprice = 'UnitPrice', InvoiceDate = 'InvoiceDate', InvoiceNo = 'InvoiceNo', LastPurshaceDate = 'LastPurshaceDate', weights = [0.25, 0.25, 0.5]):
    """

    Parameters
    ----------
    filepath : path to file 
        
    customerID : String
         (Default value = 'CustomerID')
    quantity : String
         (Default value = 'Quantity')
    unitprice : String
         (Default value = 'UnitPrice')
    InvoiceDate : String
         (Default value = 'InvoiceDate')
    InvoiceNo : String
         (Default value = 'InvoiceNo')
    LastPurshaceDate : String
         (Default value = 'LastPurshaceDate')
    weights : list
         (Default value = [0.25, 0.25, 0.5])
        

    Returns
    -------
    rfm_df_final : pandas DataFrame
    

    """

    if round(sum(weights), 2) != 1.00:
        return "Error: Weights must sum up to 1"

    # Get the extension of the file
    _, file_extension = os.path.splitext(filepath)

    # Depending on the extension, read the file
    if file_extension == ".csv":
        df = pd.read_csv(filepath, encoding= 'unicode_escape')
    elif file_extension in [".xls", ".xlsx"]:
        df = pd.read_excel(filepath)
    else:
        return "Unsupported file format"
    
    df = df[df[quantity] > 0 ] # exclude the orders with 0 value
    df = df[df[unitprice] > 0] # exclude the Unit Price with 0 value
    df.dropna(inplace=True)
    drop_outliers(df,unitprice)
    drop_outliers(df, quantity)
    df['date'] = pd.DatetimeIndex(df[InvoiceDate]).date

    # Group by customers and check last date of purchase using max function
    recency_df = df.groupby(by=customerID, as_index=False)['date'].max()
    recency_df.columns = [customerID,LastPurshaceDate]

    # Calculate recent date to find recency (maximum date in the dataset)
    recent_date=recency_df.LastPurshaceDate.max()
    print(recent_date)

    # Calculate recency: maximum date from the dataset - maximum date for each customer
    recency_df['Recency'] = recency_df[LastPurshaceDate].apply(lambda x: (recent_date - x).days)
    #recency_df.head()

    # Drop duplicates based on CustomerID and InvoiceNO columns. One order might include multiple invoices.
    # Drop duplicates except for the first occurrence
    df_new= df
    df_new.drop_duplicates(subset=[InvoiceNo, customerID], keep="first", inplace=True)

    # Calculate the frequency of purchases
    frequency_df = df_new.groupby(by=[customerID], as_index=False)[InvoiceNo].count()
    frequency_df.columns = [customerID,'Frequency']
    #frequency_df.head()

    # Create column total cost
    df['TotalCost'] = df[quantity] * df[unitprice]
    monetary_df = df.groupby(by= customerID,as_index=False).agg({'TotalCost': 'sum'})
    monetary_df.columns = [customerID,'Monetary']
    #monetary_df.head()

    temp_df = recency_df.merge(frequency_df,on= customerID)
    #temp_df.head()

    # Merge with monetary dataframe to get a table with the 3 columns
    rfm_df = temp_df.merge(monetary_df,on= customerID)

    # Rank each metric R , F & M
    rfm_df['R_rank'] = rfm_df['Recency'].rank( ascending=False) 
    rfm_df['F_rank'] = rfm_df['Frequency'].rank(ascending=True)
    rfm_df['M_rank'] = rfm_df['Monetary'].rank(ascending=True)

    # normalize each rank with Max rank
    rfm_df['R_rank_norm']=(rfm_df['R_rank']/rfm_df['R_rank'].max())*100
    rfm_df['F_rank_norm']=(rfm_df['F_rank']/rfm_df['F_rank'].max())*100
    rfm_df['M_rank_norm']=(rfm_df['F_rank']/rfm_df['M_rank'].max())*100

    
    rfm_df['RFM_Score']=weights[0]*rfm_df['R_rank_norm']+weights[1]*rfm_df['F_rank_norm']+weights[2]*rfm_df['M_rank_norm']
    rfm_df=rfm_df.round(0)
    
    rfm_df_final = rfm_df[[customerID,'R_rank_norm', 'F_rank_norm', 'M_rank_norm', 'RFM_Score']]

    return rfm_df_final






