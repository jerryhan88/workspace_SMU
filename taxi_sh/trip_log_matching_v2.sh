#!/bin/bash

#yymm=$1
yymm=0902

rv=$( ./check_os_and_set_prefix.sh )
os_type=$(echo $rv | awk -F' ' '{print $1}')
prefix=$(echo $rv | awk -F' ' '{print $2}')

./logger.sh "Handling $yymm"

matching="${prefix}/matching2"
if [ ! -d $matching ] ; then
	mkdir $matching
fi

matching_csv="${matching}/matching-${yymm}.csv"

if [ -f $matching_csv ]; then
	rm $matching_csv
fi

touch $matching_csv

matching_header="trip-id,start-time,end-time,fare,trip-mode,join-queue-time"
echo $matching_header > $matching_csv 

trip_csv="${prefix}/trips_ext/trips-${yymm}.csv"

logs_path="${prefix}/logs_ext/${yymm}"
trip_log_temp="${logs_path}/trip_log_temp2"

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
	prev_mm=$(./convert_two_digit_str.sh $prev_mm)
	prev_yymm="${yy}${prev_mm}"
fi

# process the logs of the last day of prev_yymm
# Just save the last log which occured out of the airport
if [ ! $prev_yymm == ' ' ]; then
	last_day_prev_month="${prefix}/logs_ext/${prev_yymm}"
	last_day_prev_month_csv="${last_day_prev_month}/$(ls $last_day_prev_month | grep .csv | sort | tail -1)"
	while read -r log_line; do
		echo $log_line
		did=$(echo $log_line | awk -F',' '{print $3}')
		if [ $did == driver-id ]; then
			# The header's case
			continue
		fi
		ap_or_not=$(echo $log_line | awk -F',' '{print $NF}')
		ap_or_not=${ap_or_not:0:1}
		d_prev_log="${trip_log_temp}/${did}"
		if [ $ap_or_not == X ]; then
			if [ ! -f $d_prev_log ]; then
				touch $d_prev_log
			fi
			echo $log_line > $d_prev_log
		fi 
	done < $last_day_prev_month_csv 
fi
	





./logger.sh "End $yymm"

exit 0	
	
	cat $prev_month_csv | grep $did | grep X > $d_prev_log




#
re='^[0-9]+$'
while read -r trip_line; do
	#	echo $trip_line
	t_timestamp=$(echo $trip_line | awk -F',' '{print $3}')
	if [ $t_timestamp == start-time ]; then
		# The header's case
		continue
	fi
	
	t_day=$(./get_day_from_timestamp.sh $os_type $t_timestamp)
	t_day=$(./convert_two_digit_str.sh $t_day)
	#
	tid=$(echo $trip_line | awk -F',' '{print $1}')
	et=$(echo $trip_line | awk -F',' '{print $4}')
	fare=$(echo $trip_line | awk -F',' '{print $6}')
	did=$(echo $trip_line | awk -F',' '{print $7}')
	tm=$(echo $trip_line | awk -F',' '{print $NF}')
	tm=${tm:0:1}
	if [ $tm == 3 ]; then
		continue
	fi
done < $trip_csv
	
rm -rf $trip_log_temp

./logger.sh "End $yymm"

exit 0