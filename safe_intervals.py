import sys
from itertools import groupby, dropwhile, tee
import random
import argparse

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def check_biggest(args):
    d = []
    def getter(c):
        for l in c:
            C, D = map(int, l.split('\t')[1:3])
            yield C, D

    for k, chrom in groupby(
        dropwhile(
            lambda l: l.startswith('@'),
            args.interval_list),
        key=lambda x: x.split('\t')[0]):
        print(k, max(r[0] - l[1] for l,r in pairwise(getter(chrom))))



def main(args):
    # check_biggest(args)

    # @SQ     SN:GL000222.1   LN:18686...
    chr_header = [l.strip().split() for l in args.dict if l.startswith('@SQ')]
    assert all(
        l[1].startswith('SN') and l[2].startswith('LN') for l in chr_header
    )

    chr_len = {l[1][3:]: int(l[2][3:]) for l in chr_header}

    tot_len = sum(chr_len.values())
    target_split_length = tot_len // args.numsplit

    for k, chrom in groupby(
        dropwhile(
            lambda l: l.startswith('@'),
            args.interval_list),
        key=lambda x: x.split('\t')[0]):

        # target_splits = int(chr_len[k] / tot_len * args.numsplit) + 1
        # target_split_length = chr_len[k] / target_splits

        # A --- B ___ C --- D
        # 3 regions
        # A -> B unknown (last)
        # B -> C unsafe to split (inter)
        # C -> D safe to split (cur)
        # invariant, |A -> B| < target_len
        A, B = 1, 0
        C, D = None, chr_len[k]
        for l in chrom:
            C, D = map(int, l.split('\t')[1:3])

            # first remove B + C
            # either by emitting A->C
            # or A->C fits in one interval
            # and is emitted in the while loop
            if C - A >= target_split_length:
                # don't bother with a tiny split
                # B -> C might be huge anyway
                if B - A < target_split_length * 0.5:
                    print(f"{k}:{A}-{C}")
                else:
                    print(f"{k}:{A}-{B}")
                    print(f"{k}:{B+1}-{C}")
                A = C + 1

            # while loop only splits in the safe C->D region
            assert C - A < target_split_length
            while A + target_split_length < D:
                print(f"{k}:{A}-{A+target_split_length}")
                A = A + target_split_length + 1

            B = D

        assert D == chr_len[k], k
        print(f"{k}:{A}-{D}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        'interval_list',
        type=open,
    )
    parser.add_argument(
        'dict',
        type=open,
    )
    parser.add_argument(
        'numsplit',
        type=int,
    )
    args = parser.parse_args()

    sys.exit(main(args))
