#!/bin/bash

rv=$( ./check_os_and_set_prefix.sh )
os_type=$(echo $rv | awk -F' ' '{print $1}')
prefix=$(echo $rv | awk -F' ' '{print $2}')

#yymm=$1 
yymm=0902

trip_csv="${prefix}/trips_ext/trips-${yymm}.csv"

./logger.sh "handling $trip_csv"

logs_path="${prefix}/logs_ext/${yymm}"
trip_log_temp="${logs_path}/trip_log_temp"
#
if [ -d $trip_log_temp ] ; then
	rm -rf $trip_log_temp
fi
mkdir $trip_log_temp
#
if [ $yymm == 0901 ]; then
	# The initial month for analysis
	prev_yymm=' '
elif [ $yymm == 1001 ]; then
	# Can't use 0912 data which is corrupted
	prev_yymm=' '
elif [ $yymm == 1011 ]; then
	# Can't use 1001 data which is corrupted
	prev_yymm=' '
else
	yy=${yymm:0:2}
	mm=${yymm:2:2}
	prev_mm=`expr "$mm" - 1`
	str_size=${#prev_mm}
	if [ $str_size -eq 1 ]; then
		prev_yymm="${yy}0${prev_mm}"
	else
		prev_yymm="${yy}${prev_mm}"
	fi
fi
#
while read -r line; do
	t_timestamp=$(echo $line | awk -F',' '{print $3}')
	if [ $t_timestamp == start-time ]; then
		# The header's case
		continue
	fi
	
	t_day=$(./get_day_from_timestamp.sh $os_type $t_timestamp)
	
	str_size=${#t_day}
	if [ $str_size -eq 1 ]
	then
		t_day="0${t_day}"
	fi
	
	did=$(echo $line | awk -F',' '{print $7}')
	echo $did
	d_prev_log="${trip_log_temp}/${did}"
	echo $d_prev_log 
	if [ ! -f $d_prev_log ]; then
		touch $d_prev_log
		if [ ! $prev_yymm == ' ' ]; then
			last_day_prev_month="${prefix}/logs_ext/${prev_yymm}"
			prev_month_csv="${last_day_prev_month}/$(ls $last_day_prev_month | sort | tail -1)"
			cat $prev_month_csv | grep $did | grep X > $d_prev_log 
		fi 
	else
		# Check the last log's logging time, if it is less than t_day
		# append t_day's a new csv log file (use >> command)
		last_logging_time=$(echo $(tail -1 $d_prev_log) | awk -F',' '{print $1}')
		last_logging_day=
		echo hi
		echo $last_logging_time
		
	 	# t_timestamp 	
		
		# And then use while loop
		# find the last log before trip time
		# and save other logs recorded after trip time to did_temp file
		# and mv did_temp did
	fi

done < $trip_csv
	
	
rm -rf $trip_log_temp

exit 0
