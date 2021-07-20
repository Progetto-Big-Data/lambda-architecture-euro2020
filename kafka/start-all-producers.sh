#!/bin/bash

declare -a StringArray=("718186" "718252" "721122" "721123" "723370")

for val in "${StringArray[@]}"; do
   python kafka/statistics_producer.py --interval 1 --fixture "$val" &
done

# python kafka/final_results_producer.py &
