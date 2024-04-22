if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


import pandas as pd
import numpy as np


def convert_df_to_schema(df, schema):
    new_df = df.copy()
    new_df = _adapt_columns_to_schema(new_df, schema)
    new_df = _apply_schema_types_to_df_columns(new_df, schema)
    return new_df


def _add_missing_columns(df, schema):
    missing_columns = [col for col in schema.keys() if col not in df.columns]
    for col in missing_columns:
        df[col] = pd.Series(dtype=schema[col], name=col)
    return df


def _drop_columns_not_in_schema(df, schema):
    columns_to_drop = [col for col in df.columns if col not in schema.keys()]
    df = df.drop(columns=columns_to_drop, axis=1)
    return df


def _adapt_columns_to_schema(df, schema):
    df = _add_missing_columns(df, schema)
    df = _drop_columns_not_in_schema(df, schema)
    return df


def _apply_schema_types_to_df_columns(df, schema):
    for col, dtype in schema.items():
        if df[col].dtype != dtype:
            try:
                df[col] = df[col].astype(dtype)
            except ValueError:
                print(f'{col} cannot be casted to {dtype}')
    return df


@transformer
def transform(data, *args, **kwargs):

    extended_schema_dtypes = {
        'id': 'object', 
        'type': 'object', 
        'actor_id': np.int64,
        'actor_login': 'object',
        'actor_gravatar_id': 'object',
        'actor_avatar_url': 'object',
        'actor_url': 'object',
        'repo_id': np.int64,
        'repo_name': 'object', 
        'repo_url': 'object', 
        'payload': 'object', 
        'public': 'bool',
        'created_at': 'datetime64[ns, UTC]', 
        'org_id': pd.Int64Dtype(), 
        'org_login': 'object',
        'org_gravatar_id': 'object',
        'org_avatar_url': 'object',
        'org_url': 'object',
        'other': 'object'
        }

    
    data = convert_df_to_schema(data, extended_schema_dtypes)
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
