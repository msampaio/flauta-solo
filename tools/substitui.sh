#!/bin/bash


function troca(){
    for f in $(find .. -name "*.py")
    do
        g=${f}-tmp
        cat $f | sed "s/$a/$b/g" > $g
        mv $g $f
    done
}

for l in $(cat lista.txt)
do
    a=$(echo $l | awk -F '.' '{print $1}')
    b=$(echo $l | awk -F '.' '{print $2}')
    echo $a $b
    troca

done
