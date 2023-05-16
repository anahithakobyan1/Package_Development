from marketing_package.rfm.marketing_package import rfm_calculation
from marketing_package.plot import bar_plot
import tests

rfm_test = rfm_calculation('tests/OnlineRetail.csv', customerID = 'CustomerID',quantity = 'Quantity', unitprice = 'UnitPrice', InvoiceDate = 'InvoiceDate', InvoiceNo = 'InvoiceNo', LastPurshaceDate = 'LastPurshaceDate', weights = [0.25, 0.25, 0.5])
print(rfm_test)
bar_plot(rfm_test)

