import argparse
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
    if df['Target'].sum() != 1:
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


def build_allocation_df(df):
    """
    Construct DataFrame with current allocation, target allocation, and difference for each fund
    :param df: DataFrame
    :return:
    """
    allocation_df = pd.DataFrame(index=df.index)
    allocation_df['Current_Allocation'] = df['Balance'] / df['Balance'].sum()
    allocation_df['Target_Allocation'] = df['Target']
    allocation_df['Difference'] = allocation_df['Current_Allocation'] - allocation_df['Target_Allocation']
    return (100 * allocation_df[['Current_Allocation', 'Target_Allocation', 'Difference']]).round(2)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('portfolio_csv', help='Path to csv containing portfolio information')
    parser.add_argument('--funds_to_add', help='Total dollars to be added to portfolio', default=1000, type=float)
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

    # get current allocation info for display
    current_allocation = build_allocation_df(df)

    # display results
    print '\nCurrent allocation vs Targets...'
    print current_allocation.to_string()
    print '\nDollars to add to reach target allocation...'
    print rebalance_funds.to_string()
