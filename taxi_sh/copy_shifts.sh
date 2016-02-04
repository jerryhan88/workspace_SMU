#!/bin/bash

cd /home/taxi/shift

for f in shift-09*.csv
do cat $f > "/home/ckhan/taxi/shifts/${f}"
done 

for f in shift-10*.csv
do cat $f > "/home/ckhan/taxi/shifts/${f}"
done 

exit 0