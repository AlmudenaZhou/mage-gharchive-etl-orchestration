# mage-gharchive-etl-orchestration

## Mage Structure

Mage phase follows the [ETL process](https://github.com/AlmudenaZhou/data-engineer-gharchive//blob/main/README.md#etl) outlined in the main README. The orchestrator initiates individual calls, processing data one hour at a time. The Mage process is divided into three steps:

- **Load data**: This module, available at [load_data](gharchive/data_loaders/download_gharchive_data_bulk.py), manages the process until the initial conversion of data into a dataframe.
- **Transform**: This stage is divided into two distinct parts:
  - The first part involves expanding dictionary keys into columns. This transformation is performed by the module located at [expand_dict_df_columns.py](gharchive/transformers/expand_dict_df_columns.py).
  - The second part concerns schema conversion, which is executed by the module found at [dataframe_to_schema.py](gharchive/transformers/dataframe_to_schema.py).
- **Export**: This module, accessible at [dataframe_to_gcs_parquet.py](gharchive/data_exporters/dataframe_to_gcs_parquet.py), is responsible for saving the processed data into a datalake, specifically in the Parquet format.

Note:
Mage transforms data into JSON if the output is not a dataframe, such as tuples or dictionaries containing dataframes.

## Setup

1. Build the container: `docker compose build`
1. Start the container: `docker compose up`
1. Add `secrets.json` with the Google Cloud credentials
1. Modify `io_config.yaml` as follows:
    ```
    version: 0.1.1
    default:
      # Google
      GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/secrets.json"
    ```
1. Access Mage via the URL provided by Cloud Run or the designated port, typically https://localhost:6789 if available.
1. Activate the trigger named "hourly trigger".

## Backfilled setup

To load historical data or fill gaps from failed real-time hourly triggers, from the mage main menu follow these steps:

1. Navigate to the "Triggers" tab on the left-hand side.
1. Click on the "+ New Trigger" button.
1. Choose the trigger type as "Schedule".
1. Enter a name and description for the trigger.
1. Select "hourly" as the interval type.
1. Set the interval units to "1".
1. Define the start and end date and time for the period you wish to populate in your database.