
### Logic for computing the hours overlap and uptime/downtime

We have three sources of data.

1. Store Timezones
2. Menu Hours
3. Store Status

> While importing data in the database following things are done:
> - Added missing store ids in Store Timezones

__Following steps are followed for every store_id in Store Timezones__

Step 1:

Get timezone_str using store_id and calculate the following values.

> Get get current UTC timestamp (This is for the API server)
> Convert the current UTC timestamp to the current local timestamp using timezone_str
> Use the current local timestamp to get values below

- last week's start date
- last week's end date
- last day date
- last hour start time

Step 2:

Get all Store Status records using store_id and convert timestamp_utc to local time using timezone_str

Step 3:

Get Menu Hours using store_id, and if missing, then consider open 24*7

Step 4:

Filter Store status records using Menu Hours data from step 3 for each weekday to get records which fall within the range of start_time_local to end_time_local

Step 5:

_Calculate uptime and downtime_

uptime_last_week and downtime_last_week (Hours)

- Filter Store Status records from step 4 to get records which fall within the range of last week's start date to last week's end date
- For each "active" status record, increment uptime_last_week by 1
- For each "inactive" status record, increment downtime_last_week by 1

uptime_last_day and downtime_last_day (Hours)

- Filter Store Status records from step 4 to get records which match the last day date
- For each "active" status record, increment uptime_last_day by 1
- For each "inactive" status record, increment downtime_last_day by 1

uptime_last_hour and downtime_last_hour (Minutes)

- Filter Store Status records from step 4 to get records which are from the last hour
- For each "active" status record, increment uptime_last_hour by 60
- For each "inactive" status record, increment downtime_last_hour by 60