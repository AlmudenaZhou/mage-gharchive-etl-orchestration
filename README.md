# mage-gharchive-etl-orchestration

## Mage Structure

Mage phase follows the [ETL process](../README.md#etl) outlined in the main README. The orchestrator initiates individual calls, processing data one hour at a time. The Mage process is divided into three steps:

- [load_data](gharchive/data_loaders/download_gharchive_data_bulk.py) covers the process until the initial dataframe conversion
- [transform](gharchive/transformers/compress_data_to_df_bulk.py)  encompasses the process from data compression to schema conversion.
- [export](gharchive/data_exporters/dataframe_to_gcs_parquet.py) handles the saving of data into a datalake.

Note:
Mage transforms data into JSON if the output is not a dataframe, such as tuples or dictionaries containing dataframes.

## Setup

1. Build the container: `docker compose build`
2. Start the container: `docker compose up`
3. Add `secrets.json` with the Google Cloud credentials
4. Modify `io_config.yaml` as follows:
    ```
    version: 0.1.1
    default:
      # Google
      GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/secrets.json"
    ```


## Backfilled setup

To load historical data or fill gaps from failed real-time hourly triggers, follow these steps:

1. Specify the start and end date and time for the period you want to fill in your database.
1. Select the interval type as "hour".
1. Set the interval units to "1".
