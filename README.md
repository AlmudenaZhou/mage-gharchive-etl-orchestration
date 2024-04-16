# mage-gharchive-etl-orchestration

## Mage Structure

Mage phase follows the [ETL process](../README.md#etl). The orchestrator makes individual calls, one hour at a time. The process inside Mage it is divided into 3 steps:

- [load_data](gharchive/data_loaders/download_gharchive_data_bulk.py) includes until first dataframe conversion included.
- [transform](gharchive/transformers/compress_data_to_df_bulk.py) includes until after converted to schema included.
- [export](gharchive/data_exporters/dataframe_to_gcs_parquet.py) includes save the data into a datalake

Note:
It seems mage transform to json if the output is not a dataframe => tuples or dictionaries that containes dataframes are transformed into json

## Setup

1. Build the container: `docker compose build`
2. Start the container: `docker compose up`
3. Add secrets.json with the google cloud credentials
4. Change io_config.yaml to:
    ```
    version: 0.1.1
    default:
      # Google
      GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/secrets.json"
      ```


## Backfilled setup

This will help you to load historical data or to fill gaps if a real-time hourly trigger has failed.

1. Fill the start and end date and time for the dates you want to fill your database
1. Interval type -> hour
1. Interval units -> 1
