#!/usr/bin/env python

"""
Write all matrices in a Kaldi archive (text format) to Numpy .npz format.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2014-2015, 2019
"""

from __future__ import division
from __future__ import print_function
import argparse
import datetime
import numpy as np
import sys

from kaldi import read_kaldi_ark


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)

    parser.add_argument("kaldi_ark_fn", help="Kaldi archive file in text format")
    parser.add_argument("npz_fn", help="Numpy output file")
    parser.add_argument("--filter_fn", default=None, help="A filter file containing utterance IDs to retain. This text file should contain one ID per line. Utterances not in the list are discarded at the output. Omitting this optional argument causes no utterances to be discarded.")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    print(str(datetime.datetime.now()))

    filterset = None
    if args.filter_fn:
        print("Reading filter set:", args.filter_fn)
        with open(args.filter_fn, "r") as fid:
            filterset = set([aline.strip() for aline in fid])

    print("Reading Kaldi archive:", args.kaldi_ark_fn)
    kaldi_ark = read_kaldi_ark(args.kaldi_ark_fn, retain_filter=filterset)
    print("Number of keys in archive:", len(kaldi_ark.keys()))

    # all_features = np.asarray(np.concatenate(kaldi_ark.values(), axis=0), dtype=np.float32)
    # print("Number of feature vectors:", all_features.shape[0])
    # print("Feature vector dimensions:", all_features.shape[1])

    print("Writing feature vectors to file:", args.npz_fn)
    np.savez(args.npz_fn, **kaldi_ark)

    print(str(datetime.datetime.now()))


if __name__ == "__main__":
    main()
