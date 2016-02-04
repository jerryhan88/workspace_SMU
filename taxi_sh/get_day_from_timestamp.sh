#!/bin/bash

os_type=$1
t_timestamp=$2

if [ $os_type == Darwin ]; then
	t_day=$(date -r $t_timestamp | awk -F' ' '{print $3}')
else 
	t_day=$(date -d @$t_timestamp | awk -F' ' '{print $3}')
fi

echo $t_day