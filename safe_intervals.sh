#!/bin/bash
set -euo pipefail

# rename chrs, assuming here that coordinates do not change
# certainly MT is different, but maybe also Y
sed -e 's|^chr||g' genes.bed | awk '$1 ~ /^[0-9]+$/' > genes.37.bed
sed -e 's|^chr||g' genes.bed | awk '$1 ~ /^X$|^Y$/' >> genes.37.bed

# gatk needs the file to be called interval_list...
cp hs37d5x.dict hs37d5x.dict.interval_list

gatk BedToIntervalList --INPUT genes.37.bed --SD hs37d5x.dict --OUTPUT genes.37.interval_list

# invert to get an 'all genome' list, then subtract the genes to get a 'safe regions'
gatk IntervalListTools --ACTION CONCAT --INVERT --INPUT hs37d5x.dict.interval_list --OUTPUT hs37d5x.dict.all.interval_list
gatk IntervalListTools --ACTION SUBTRACT --INPUT hs37d5x.dict.all.interval_list --SECOND_INPUT genes.37.interval_list --OUTPUT hs37d5x.dict.all.sub.interval_list

# combine intervals to try get ~N safe regions
python3 safe_intervals.py hs37d5x.dict.all.sub.interval_list hs37d5x.dict 25000 | awk '/^([0-9]+|X|Y|MT):/' > hs37d5x.nogenes.20k.intervals

python3 check.py hs37d5x.nogenes.20k.intervals 
wc -l hs37d5x.nogenes.20k.intervals 
