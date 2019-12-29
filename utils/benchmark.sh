# ./utils/benchmark.sh [n]
#       n: times to run each day / default: 10

N=$([ "$1" == "" ] && echo 10 || echo $1)
for i in $(seq -f "%02g" 1 25); do
    echo === day$i.py ===

    for s in $(seq 1 "$N"); do
        python3 day$i.py | tail -n 1
    done
done