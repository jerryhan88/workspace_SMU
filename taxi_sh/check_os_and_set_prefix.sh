#!/bin/bash

os_type=`uname -a | awk '{print $1}'`
 
if [ $os_type=Darwin ]; then
	echo /Users/JerryHan88/taxi
else
	echo /home/ckhan/taxi
fi