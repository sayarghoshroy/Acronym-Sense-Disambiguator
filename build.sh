mkdir $2
echo "0" > docnum
python3 indexer.py $1 $2  0 100000
python3 indexer.py $1 $2  100000 200000
python3 indexer.py $1 $2  200001 300000
python3 indexer.py $1 $2  300001 400000
python3 indexer.py $1 $2  500001 600000
python3 indexer.py $1 $2  600001 700000
python3 combine.py $2
