#!/bin/bash
# this script uses the AK REST API and the event merge script 
# in https://github.com/MoveOnOrg/misc_scripts/blob/master/ak-event-merge/merge.py
# to bulk merge events

file="events_to_merge.csv" 
# absolute path to csv with two columns
# don't forget to delete the header row
# and add a blank line to the end of the csv 
# or this script will skip the last row

# before running this script 
# fill in <signup page id> with AK page ID (integer) of the signup page for TO_EVENT',
# your AK instance base URL, <user> and <password>.
# run this script in misc-scripts/ak-event-merge/ with `bash bulk_event_merge.sh`

signup=
baseurl="https://act.moveon.org/" 
user=""
pass=""

while IFS=, read -r fromevent toevent
do
  python merge.py --FROM_EVENT $fromevent --TO_EVENT $toevent --SIGNUP_PAGE $signup --AK_BASEURL $baseurl --AK_USER $user --AK_PASS $pass
done < "$file"