import matplotlib.pyplot as plt
from marketing_package.rfm.marketing_package import rfm_calculation
import numpy as np

def bar_plot(df = rfm_calculation, manual_scores = [75, 50]):
    """

    Parameters
    ----------
    df :    dataframe containing column 'RFM_Score' and 'CustomerID'
         (Default value = rfm_calculation)
    manual_scores : list
         (Default value = [75, 50] :    

    Returns
    -------
    barplot

    """
    # We divide our customers into three groups based on this scores. 
    # These scores can be changed as an input. and the number of groups based on scores can also be changed with the below two lines
    # of code. However, in the future plans is to improve the grouping part based on specidic business decision on scores and groups.
    # 0 - 50 - Risky customers
    # 50 - 75 - Potential Loyalists
    # 76 - 100 - Champions
    df["Customer_segment"]=np.where(df['RFM_Score'] > manual_scores[0] ,"Champions ",
                                    (np.where(df['RFM_Score'] < manual_scores[1] , "Risky Customers" ,"Potential Loyalists")))
    data = df.groupby('Customer_segment')[['CustomerID']].count()

    data.plot(kind='bar', legend=False)  
    plt.title('Customer Segments')
    plt.xlabel('Segment')
    plt.ylabel('Number of Customers')
    plt.tight_layout()
    plt.show()
    