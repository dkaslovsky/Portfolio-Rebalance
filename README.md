# Portfolio-Rebalance
Rebalances an investment portfolio by allocating funds to realize specified targets

<br>

**Example Usage**

Rebalance the portfolio summarized by `example_funds.csv` by adding $1000:
```
python rebalance.py example_funds.csv 1000
```

```
Current allocation vs Targets...
       Current_Allocation  Target_Allocation  Difference
Fund                                                    
FundA               45.45               50.0       -4.55
FundB               18.18               20.0       -1.82
FundC               36.36               30.0        6.36

Dollars to add to reach target allocation...
       Dollars_to_Add  Allocation  Target_Allocation  Difference
Fund                                                            
FundA           525.0        52.5               50.0         2.5
FundB           210.0        21.0               20.0         1.0
FundC           265.0        26.5               30.0        -3.5
```
