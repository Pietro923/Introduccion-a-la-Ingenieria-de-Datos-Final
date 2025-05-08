from dagster import EnvVar, IOManager, io_manager
from dagster_airbyte import AirbyteResource
from dagster_dbt import DbtCliResource, DbtProject
import sqlalchemy
import pandas as pd
import os
from pathlib import Path
from dagster import ResourceDefinition
import mlflow

airbyte_resource = AirbyteResource(
    host=EnvVar("AIRBYTE_HOST"), #localhost
    port=EnvVar("AIRBYTE_PORT"), #8000
    username=EnvVar("AIRBYTE_USERNAME"), #airbyte
    password=EnvVar("AIRBYTE_PASSWORD") #airbyte
)


dbt_resource = DbtCliResource(    
    #project_dir="C:\Users\USUARIO\dbt_testing",
    project_dir=Path("C:/Users/USUARIO/dbt_testing").resolve(),
    profiles_dir=Path("C:/Users/USUARIO/.dbt").resolve(),
    target="dev",
    profile="dbt_testing"
)


class PostgresIOManager(IOManager):
    def __init__(self, engine, schema="target"):
        self.engine = engine
        self.schema = schema

    def load_input(self, context):
        # Get the table name and include the schema
        table_name = context.upstream_output.asset_key.path[-1]
        full_table_name = f"{self.schema}.{table_name}"
        query = f"SELECT * FROM {full_table_name}"
        return pd.read_sql(query, self.engine)

    def handle_output(self, context, obj):
        pass

@io_manager(config_schema={"connection_string": str, "schema": str})
def postgres_io_manager(init_context):
    connection_string = init_context.resource_config["connection_string"]

    # If the connection_string is an environment variable reference
    if connection_string.startswith("env:"):
        env_var = connection_string.split("env:")[1]
        connection_string = os.environ[env_var]  # Resolve the environment variable to a string

    schema = init_context.resource_config.get("schema", "target")  # Default to "public" schema
    engine = sqlalchemy.create_engine(connection_string)
    return PostgresIOManager(engine, schema)

mlflow_resource = ResourceDefinition.hardcoded_resource(mlflow)