# ./utils/runAll.sh [-a|t]
#       -t: print only time taken
#       -a: print only answers

for i in $(seq -f "%02g" 1 25); do
    echo === day$i.py ===
    
    if [ "$1" == "-a" ]; then
        python3 day$i.py | head -n -1
    elif [ "$1" == "-t" ]; then
        python3 day$i.py | tail -n 1
    else
        python3 day$i.py
    fi
done
