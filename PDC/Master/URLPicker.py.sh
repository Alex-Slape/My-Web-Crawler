#!/bin/bash
iternum=$1
echo $iternum
for ((c = 1; c <= $iternum; c++))
do
	python ../URLPicker/URLPicker.py &
done
