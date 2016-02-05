#!/bin/bash

os_type=`uname -a | awk '{print $1}'`
 
if [ $os_type == Darwin ]; then
	echo $os_type /Users/JerryHan88/taxi
else
	echo $os_type /home/ckhan/taxi 
fi