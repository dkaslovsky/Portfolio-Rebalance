import argparse
import numpy as np
import pandas as pd
import sys

""" Rebalances a portfolio by allocating dollars to be added to each fund to realize targets """


def load_from_csv(path_to_csv):
    """
    Reads portfolio information from csv file
    :param path_to_csv: path to csv file
    :return: dataframe
    """
    df = pd.read_csv(path_to_csv)
    validate_csv(df)
    df = df.set_index('Fund')
    return df


def validate_csv(df):
    """
    Ensures csv file has required columns and data is valid
    :param df: DataFrame
    :return:
    """
    required_cols = {'Fund', 'Balance', 'Target'}
    if set(df.columns) != required_cols:
        raise ValueError('Must provide all required columns: %s' % required_cols)
    if not np.allclose(df['Target'].sum(), 1):
        raise ValueError('Targets must sum to 1')
    if (df['Balance'] < 0).any():
        raise ValueError('Balances must not be negative')
    return True


def rebalance(df, total_dollars_added):
    """
    Allocates dollars to each fund according to specified targets
    :param df: DataFrame
    :param total_dollars_added: total dollars to be added to portfolio
    :return:
    """
    cur_balance = df['Balance'].sum()
    new_balance = cur_balance + total_dollars_added
    dollars_to_add_per_fund = (df['Target'] * new_balance) - df['Balance']
    if (dollars_to_add_per_fund < 0).any():
        raise ValueError('Must add more money for strictly additive rebalance')
    return dollars_to_add_per_fund


def display_rebalance_info(df, rebalance_funds):
    """
    Print DataFrame with amount to be used for rebalancing and allocation info
    :param df: DataFrame
    :param rebalance_funds: Series resulting from rebalance()
    :return:
    """
    rebalanced = pd.DataFrame(index=df.index)
    rebalanced['Allocation'] = rebalance_funds / rebalance_funds.sum()
    rebalanced['Target_Allocation'] = df['Target']
    rebalanced['Difference'] = rebalanced['Allocation'] - rebalanced['Target_Allocation']
    rebalanced = (100 * rebalanced).round(2)
    rebalanced['Dollars_to_Add'] = rebalance_funds
    print rebalanced[['Dollars_to_Add', 'Allocation', 'Target_Allocation', 'Difference']].to_string()


def display_allocation_info(df):
    """
    Print DataFrame with current allocation, target allocation, and difference for each fund
    :param df: DataFrame
    :return:
    """
    allocation_df = pd.DataFrame(index=df.index)
    allocation_df['Current_Allocation'] = df['Balance'] / df['Balance'].sum()
    allocation_df['Target_Allocation'] = df['Target']
    allocation_df['Difference'] = allocation_df['Current_Allocation'] - allocation_df['Target_Allocation']
    print (100 * allocation_df[['Current_Allocation', 'Target_Allocation', 'Difference']]).round(2).to_string()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('portfolio_csv', help='Path to csv containing portfolio information')
    parser.add_argument('funds_to_add', help='Total dollars to be added to portfolio', type=float)
    args = parser.parse_args()

    # load data
    try:
        df = load_from_csv(args.portfolio_csv)
    except ValueError as e:
        print e
        sys.exit()

    # compute rebalance funds
    try:
        rebalance_funds = rebalance(df, args.funds_to_add)
    except ValueError as e:
        print e
        sys.exit()

    # display results
    print '\nCurrent allocation vs Targets...'
    display_allocation_info(df)
    print '\nDollars to add to reach target allocation...'
    display_rebalance_info(df, rebalance_funds)
    print '\n'
