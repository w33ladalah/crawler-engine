#!/bin/bash

# Declare variables and assign it from command line arguments
MIN=$1
HOUR=$2
ENGINE=$3
MODE=$4
PATH=$PWD

# If MODE is "REMOVE" then delete the line that contains string from SUBSTR variable.
if [ "$MODE" = "REMOVE" ]; then
	/bin/sed -i "/$ENGINE/d" "$PATH/CURRENT_CRON_JOBS"

# If MODE is "APPEND", append it!
else
	# Write out current crontab
	/usr/bin/crontab -l > "$PATH/CURRENT_CRON_JOBS"
	
	# Remove whitespaces
	/bin/sed -i '/./!d' "$PATH/CURRENT_CRON_JOBS"

	# Echo new cron into cron file
	echo "$MIN $HOUR * * * /usr/bin/python /opt/engine.lintas.me/scheduler.py -c $ENGINE" >> "$PATH/CURRENT_CRON_JOBS"
fi

# Install new cron file
/usr/bin/crontab "$PATH/CURRENT_CRON_JOBS"