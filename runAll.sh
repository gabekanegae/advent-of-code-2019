# ./runAll.sh [-t]
#       -t: don't print answers, only time taken

for i in $(seq -f "%02g" 1 25); do
    echo === day$i.py ===
    
    python3 day$i.py > .day$i.tmp
    
    if [ "$1" == "-t" ]; then
        grep -r "Time:" .day$i.tmp
    else
        cat .day$i.tmp
    fi
    
    rm .day$i.tmp
done