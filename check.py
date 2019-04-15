import sys
from itertools import groupby
import random
import argparse
import pandas as pd


def main(args):
    ds = []
    for k, chrom in groupby(
        open(args.interval_list),
        key=lambda x: x.split(':')[0]):

        ds.append(
            pd.DataFrame(
                [k, r - l] for l, r in map(
                    lambda l: map(int, l.split(':')[1].split('-')),
                    chrom
                )
            )
        )

    d = pd.concat(ds)
    # print(d.groupby(0).describe().loc[:, ['count','mean','min','max',]])
    # print(k, d.count(), d.min(), d.mean(), d.max())

    lump = d.loc[:, 1]
    desc = lump.describe()
    print(desc)

    print("max:50", desc['max'] / desc['50%'])
    print("max:mean", desc['max'] / desc['mean'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('interval_list', )
    args = parser.parse_args()

    sys.exit(main(args))
