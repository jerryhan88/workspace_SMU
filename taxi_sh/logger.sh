#!/bin/bash

if ! [ -f log.txt ]
then
	touch log.txt
fi

echo $(date) --- $1 >> log.txt

exit 0