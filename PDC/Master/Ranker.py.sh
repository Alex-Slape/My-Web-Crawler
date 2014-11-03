iternum=$1
echo $iternum
for ((c = 1; c <= $iternum; c++))
do
	python ../MapReduce/Ranker.py &
done
