import argparse
import os

import pandas as pd


NEW_BALANCE_COLUMN_MAP = {
    'Symbol': 'Fund',
    'Total Value': 'Balance',
}

def get_new_filename(args):
    file_name, ext = os.path.splitext(os.path.basename(args.portfolio_csv))
    new_file_name = file_name + '_UPDATED' + ext
    return os.path.join(os.path.dirname(args.portfolio_csv), new_file_name)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('portfolio_csv', help='Path to csv containing portfolio information')
    parser.add_argument('new_balance_csv', help='Path to csv containing updated balance information')
    args = parser.parse_args()

    portfolio_df = pd.read_csv(args.portfolio_csv)
    new_balance_df = (
        pd.read_csv(args.new_balance_csv)
        .rename(columns=NEW_BALANCE_COLUMN_MAP)
        .filter(NEW_BALANCE_COLUMN_MAP.values())
    )

    updated_df = pd.concat(
        [
            portfolio_df.drop('Balance', axis=1).set_index('Fund'),
            new_balance_df.set_index('Fund'),
        ],
        axis=1,
        join='inner',
    ).reset_index()
    
    updated_file_path = get_updated_filename(args)
    updated_df.to_csv(updated_file_path, index=False)
