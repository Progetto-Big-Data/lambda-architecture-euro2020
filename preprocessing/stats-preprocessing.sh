#!/bin/bash

declare -a StringArray=("718186" "718252" "721122" "721123" "723370")

for val in "${StringArray[@]}"; do
   python preprocessing/fill_null_stats.py "dataset/stats_$val.json"
   python preprocessing/create_delta_stats.py "dataset/filled_na_stats_$val.json"
done
