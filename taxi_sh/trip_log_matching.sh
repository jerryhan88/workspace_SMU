#!/bin/bash

prefix=$( ./check_os_and_set_prefix.sh )

echo "${prefix}/logs_ext/0901"
target_file="${prefix}/logs_ext/0901/logs-090101.csv"
# cat $target_file 

./logger.sh "processing $target_file" 

while read -r line; do
	a=$(echo $line | awk -F',' '{print $3}')
	echo $a
	if [ "$a" == X ]
	then
		echo XX
	else
		echo YY
	fi
	#a=$(date -d @1267619929 | awk -F' ' '{print $3}')
	
	break
	
	#if [ "$a" -gt 2 ]
	#then
		#	break  # Skip entire rest of loop.
	#fi

:'
#echo -n "$a "

 a=$(($a+1))

 if [ "$a" -eq 3 ] || [ "$a" -eq 11 ]  # Excludes 3 and 11.
 then
   continue      # Skip rest of this particular loop iteration.
 fi

 echo -n "$a "   # This will not execute for 3 and 11.
done 
'

done < $target_file