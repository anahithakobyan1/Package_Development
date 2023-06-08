# RFM Analysis Package

This Python package provides an easy-to-use implementation of RFM (Recency, Frequency, Monetary) analysis, a customer segmentation technique that uses past purchase behavior to divide customers into groups. It uses the customer transaction data to  divide the customers into three groups based on their RFM scores: Champions, Potential Loyalists and Risky Customers.

Recency - How recently a customer has made a purchase
Frequency - How often a customer makes a purchase
Monetary Value - How much money a customer spends on purchases


## Data Format

The RFM Analysis package expects data in CSV or Excel format having the following columns:

CustomerID: Unique identifier for each customer.
InvoiceDate: Date of the purchase (transaction).
InvoiceNo: Unique identifier for each invoice.
TotalSum: The total sum of the purchase.

## Usage 

To use the package you can use the code in example.py which uses a sample data in the tests directory or you can follow these steps.

#### Step 1. Import the necessary libraries.
rfm_calculation is a function in marketing_package\rfm\marketing_package.py, where the main code for calculating RFM scores is written.
bar_plot is a function in marketing_package.plot.py which visualizes the customer segments as bars.
tests is a package that includes the sample data called *** OnlineRetail.csv ***.

```
from marketing_package.rfm.marketing_package import rfm_calculation
from marketing_package.plot import bar_plot
import tests

```
#### Step 2. Run the rfm_calculation() on your data or on sample data using this code.

```
rfm_test = rfm_calculation('tests/OnlineRetail.csv', customerID = 'CustomerID',quantity = 'Quantity', unitprice = 'UnitPrice', InvoiceDate = 'InvoiceDate', InvoiceNo = 'InvoiceNo', LastPurshaceDate = 'LastPurshaceDate', weights = [0.25, 0.25, 0.5])
print(rfm_test)

```

#### Step 3. Visualize the scores.

```
bar_plot(rfm_test)
```



## Contributing
We welcome contributions to the RFM Analysis Marketing package! Please open an issue or submit a pull request onmy GitHub page.

## License
This project is licensed under the terms of the MIT license.
