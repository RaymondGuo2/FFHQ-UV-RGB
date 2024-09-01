#!/bin/bash

cd ./RGB_Fitting
for exp in {1..45}; do
    for value in -1 1; do
        python alter_expression.py --exp_component $exp --change_value $value
    done
done