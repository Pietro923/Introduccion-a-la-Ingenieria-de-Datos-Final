from pathlib import Path
from dagster import EnvVar
from dagster_dbt import DbtCliResource, DbtProject

dbt_testing = DbtProject(
    #project_dir="C:\Users\USUARIO\dbt_testing",
    project_dir=Path("C:/Users/USUARIO/dbt_testing").resolve(),
    profiles_dir=Path("C:/Users/USUARIO/.dbt").resolve(),    
    #profiles_dir=Path.home().joinpath(".dbt"),
    #target="dev",
    #profile="dbt_testing"
)

dbt_testing.prepare_if_dev()