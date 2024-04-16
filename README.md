# mage-gharchive-etl-orchestration

### Setup

1. Build the container: `docker compose build`
2. Start the container: `docker compose up`
3. Add secrets.json with the google cloud credentials
4. Change io_config.yaml to:
version: 0.1.1
default:
  # Google
  GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/secrets.json"


## Backfilled setup

1. Fill the start and end date and time for the dates you want to fill your database
1. Interval type -> hour
1. Interval units -> 1

Notes:
It seems mage transform to json if the output is not a dataframe => tuples or dictionaries that containes dataframes are transformed into json => individual calls, one hour at a time, and structure:
  - load_data step includes until first dataframe conversion, included.
  - transform step includes until after converted to schema
  - export step includes save the data into a datalake