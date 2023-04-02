i="0"
while [ 2 -gt 1 ]
do
i=$[$i+1]
echo $i
python main.py data/real/cubes.txt gen shapes/3d333.tsv >> solns/333_loop.tsv
done
