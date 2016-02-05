#!/bin/bash

digit=$1

str_size=${#digit}
if [ $str_size -eq 1 ]
then
	echo "0${digit}"
else
	echo "${digit}"
fi