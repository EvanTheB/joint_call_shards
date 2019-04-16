import sys
from itertools import groupby, dropwhile, tee, chain
import random
import argparse
import pandas as pd


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def longest(args):
    d = []

    def getter(c):
        for l in c:
            C, D = map(int, l.split('\t')[1:3])
            yield C, D

    for k, chrom in groupby(
            dropwhile(
                lambda l: l.startswith('@'),
                open(args.safe_list)),
            key=lambda x: x.split('\t')[0]):
        d.append(max(chain([0], (r[0] - l[1] for l, r in pairwise(getter(chrom))))))
        print(k, d[-1])
    return max(d)


def stats(args):
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
    return desc['max']


def main(args):

    m = stats(args)
    print()

    l = longest(args)
    print()

    print("longest to best ratio:", m / l)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('interval_list', )
    parser.add_argument('safe_list', )
    args = parser.parse_args()

    sys.exit(main(args))
