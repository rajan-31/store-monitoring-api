### PostgreSQL setup

Create tables

```sql
DROP TABLE IF EXISTS store_status;
DROP TABLE IF EXISTS menu_hours;
DROP TABLE IF EXISTS store_timezones;
DROP TABLE IF EXISTS reports_data;
DROP TABLE IF EXISTS reports_status;


CREATE TABLE store_timezones (
    store_id BIGINT,
    timezone_str VARCHAR(100),
    PRIMARY KEY(store_id)
);

CREATE TABLE store_status (
    store_id BIGINT NOT NULL,
    status VARCHAR(20),     -- active/inactive
    timestamp_utc TIMESTAMP
);

CREATE TABLE menu_hours (
	store_id BIGINT NOT NULL,
	day SMALLINT NOT NULL,      -- 0 to 6
	start_time_local TIME,
	end_time_local TIME
);


CREATE TABLE reports_status (
    report_id UUID,
    status VARCHAR(20),     -- Running, Complete
    PRIMARY KEY(report_id)
);

CREATE TABLE reports_data (
    report_id UUID NOT NULL,
    store_id BIGINT NOT NULL,
    uptime_last_hour SMALLINT NOT NULL,     -- minutes
    uptime_last_day SMALLINT NOT NULL,      -- hours
    uptime_last_week SMALLINT NOT NULL,     -- hours
    downtime_last_hour SMALLINT NOT NULL,   -- minutes
    downtime_last_day SMALLINT NOT NULL,    -- hours
    downtime_last_week SMALLINT NOT NULL,   -- hours
	FOREIGN KEY (report_id)
    	REFERENCES reports_status (report_id)
    	ON DELETE CASCADE
);
```

Check data

```sql
SELECT * FROM store_timezones LIMIT 5; 
SELECT * FROM store_status LIMIT 5; 
SELECT * FROM menu_hours LIMIT 5;
SELECT * FROM reports_status LIMIT 5;
SELECT * FROM reports_data LIMIT 5;

\d+ store_timezones; 
\d+ store_status;
\d+ menu_hours;
\d+ reports_status;
\d+ reports_data;
```

Truncate data

```sql
TRUNCATE store_timezones, store_status, menu_hours;
TRUNCATE reports_status, reports_data;
```