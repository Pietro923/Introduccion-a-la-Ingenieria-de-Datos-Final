from dagster import Definitions, load_assets_from_modules, define_asset_job, AssetSelection
from dg_testing.assets.airbyte import airbyte_connections
from dg_testing import assets  # noqa: TID252

from dg_testing.assets import dbt, train_model   
from dg_testing.resources import dbt_resource, postgres_io_manager, mlflow_resource

#--------------------------------Assets Definitions--------------------------------    

dbt_assets = load_assets_from_modules([dbt], group_name="raw_data_transformation")

train_assets = load_assets_from_modules([train_model])

#--------------------------------Jobs Definitions--------------------------------    
airbyte_sync_job = define_asset_job(name="airbyte_sync_job",  selection=AssetSelection.groups("raw_data_ingestion"))

dbt_sync_job = define_asset_job("dbt_sync_job" , selection=AssetSelection.groups("raw_data_transformation"))

data_prep_job = define_asset_job("data_prep_job", selection=AssetSelection.groups("data_preparation"))

sync_all_jobs = define_asset_job(name="sync_all_jobs", selection=AssetSelection.all())

#--------------------------------Definitions--------------------------------    
defs = Definitions(
    assets=[airbyte_connections, *dbt_assets, *train_assets],
    jobs=[airbyte_sync_job, dbt_sync_job, data_prep_job, sync_all_jobs],
    resources={
        "dbt": dbt_resource, 
        "postgres_io_manager": postgres_io_manager.configured({
            "connection_string": "env:POSTGRES_CONNECTION_STRING",
            "schema": "target"
        }),
        "mlflow": mlflow_resource  # 👈 agregamos esto
    }
)
