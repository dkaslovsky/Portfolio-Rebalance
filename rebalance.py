""" Rebalances a portfolio by allocating dollars to be added to each fund to realize targets """

import argparse
import sys

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'portfolio_csv',
        help='Path to csv containing portfolio information',
    )
    parser.add_argument(
        'dollars_to_add',
        type=float,
        help='Total dollars to be added to portfolio',
    )
    parser.add_argument(
        '--allow_negative',
        action='store_true',
        required=False,
        help='Allow negative contributions',
    )
    return parser.parse_args()


def load_from_csv(path_to_csv: str) -> pd.DataFrame:
    """
    Reads portfolio information from csv file
    :param path_to_csv: path to csv file
    """
    df = pd.read_csv(path_to_csv)
    validate_csv(df)
    df = df.set_index('Fund')
    return df


def validate_csv(df: pd.DataFrame) -> None:
    """
    Ensures csv file has required columns and data is valid
    :param df: DataFrame read from csv file
    """
    required_cols = {'Fund', 'Balance', 'Target'}
    if set(df.columns) != required_cols:
        raise ValueError('Must provide all required columns: %s' % required_cols)
    if not np.allclose(df['Target'].sum(), 1):
        raise ValueError('Targets must sum to 1')
    if (df['Balance'] < 0).any():
        raise ValueError('Balances must not be negative')


def rebalance(
    df: pd.DataFrame,
    total_dollars_added: float,
    allow_negative: bool = False,
) -> pd.Series:
    """
    Allocates dollars to each fund according to specified targets
    :param df: DataFrame with portfolio data
    :param total_dollars_added: total dollars to be added to portfolio
    :param allow_negative: allow negative contributions
    """
    cur_balance = df['Balance'].sum()
    new_balance = cur_balance + total_dollars_added
    dollars_to_add_per_fund = (df['Target'] * new_balance) - df['Balance']
    if not allow_negative:
        if (dollars_to_add_per_fund < 0).any():
            raise ValueError('Must contribute more money for strictly additive rebalance')
    return dollars_to_add_per_fund


def display_allocation(df: pd.DataFrame) -> None:
    """
    Print DataFrame with current allocation, target allocation, and difference for each fund
    :param df: DataFrame with portfolio data
    """
    allocation_df = pd.DataFrame(index=df.index)
    allocation_df['Current_Allocation'] = df['Balance'] / df['Balance'].sum()
    allocation_df['Target_Allocation'] = df['Target']
    allocation_df['Difference'] = \
        allocation_df['Current_Allocation'] - allocation_df['Target_Allocation']

    allocation_df = (
        (100 * allocation_df[['Current_Allocation', 'Target_Allocation', 'Difference']])
        .round(2)
        .sort_values('Difference', ascending=False)
    )
    print(allocation_df)


def display_rebalanced(df: pd.DataFrame, rebalance_funds: pd.Series) -> None:
    """
    Print DataFrame with amount to be used for rebalancing and allocation info
    :param df: DataFrame with rebalanced portfolio data
    :param rebalance_funds: Series resulting from rebalance()
    """
    rebalanced = pd.DataFrame(index=df.index)
    rebalanced['Allocation'] = rebalance_funds / rebalance_funds.sum()
    rebalanced['Target_Allocation'] = df['Target']
    rebalanced['Difference'] = rebalanced['Allocation'] - rebalanced['Target_Allocation']
    rebalanced = (100 * rebalanced).round(2)
    rebalanced['Dollars_to_Add'] = rebalance_funds.round(2)

    rebalanced = (
        rebalanced[['Dollars_to_Add', 'Allocation', 'Target_Allocation', 'Difference']]
        .sort_values('Dollars_to_Add', ascending=False)
    )
    print(rebalanced)


if __name__ == '__main__':

    args = parse_args()

    # load and display current allocation data
    try:
        portfolio_df = load_from_csv(args.portfolio_csv)
    except ValueError as err:
        print(f'{err}\n')
        sys.exit(1)

    print('Current allocation vs Targets...')
    display_allocation(portfolio_df)
    print('')

    # compute and display rebalance fund data
    try:
        rebalance_funds = rebalance(portfolio_df, args.dollars_to_add, args.allow_negative)
    except ValueError as err:
        print(f'{err}\n')
        sys.exit(1)

    print('Dollars to add to reach target allocation...')
    display_rebalanced(portfolio_df, rebalance_funds)
    print('')
