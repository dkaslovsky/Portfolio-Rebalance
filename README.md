# Portfolio-Rebalance
Small project for rebalancing an investment portfolio by allocating funds to realize specified targets

<br>

**Example Usage**

Rebalance the portfolio summarized by `example_funds.csv` by adding $1000:
```
>> python rebalance.py example_portfolio.csv 1000
Current allocation vs Targets...
             Current_Allocation  Target_Allocation  Difference
Fund                                                          
InvestmentA               45.45               50.0       -4.55
InvestmentB               18.18               20.0       -1.82
InvestmentC               36.36               30.0        6.36

Dollars to add to reach target allocation...
             Dollars_to_Add  Allocation  Target_Allocation  Difference
Fund                                                                  
InvestmentA           525.0        52.5               50.0         2.5
InvestmentB           210.0        21.0               20.0         1.0
InvestmentC           265.0        26.5               30.0        -3.5
```

If the dollar amount to be added is not enough for an additive (positive) contribution to each fund, no contribution is possible:

```
>> python rebalance.py example_portfolio.csv 100
Must add more money for strictly additive rebalance
```

Negative contributions can be computed by passing the `--allow_negative` flag:

```
>> python rebalance.py --allow_negative example_portfolio.csv 100
Current allocation vs Targets...
             Current_Allocation  Target_Allocation  Difference
Fund                                                          
InvestmentA               45.45               50.0       -4.55
InvestmentB               18.18               20.0       -1.82
InvestmentC               36.36               30.0        6.36

Dollars to add to reach target allocation...
             Dollars_to_Add  Allocation  Target_Allocation  Difference
Fund                                                                  
InvestmentA            75.0        75.0               50.0        25.0
InvestmentB            30.0        30.0               20.0        10.0
InvestmentC            -5.0        -5.0               30.0       -35.0
```
