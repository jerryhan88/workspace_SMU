#!/bin/bash

os_type=`uname -a | awk '{print $1}'`
echo $os_type 
if [ $os_type=Darwin ]; then
	echo osX
	prefix=''
else
	echo Linux
fi

