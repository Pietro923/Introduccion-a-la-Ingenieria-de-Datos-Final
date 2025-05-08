from dagster import AssetExecutionContext
from dagster_dbt import dbt_assets, DbtCliResource
from ..dbt_integrations import dbt_testing

@dbt_assets(
    manifest=dbt_testing.manifest_path,
    select="dbt_testing.movies dbt_testing.critic_reviews dbt_testing.user_reviews dbt_testing.review_stats dbt_testing.user_critic_reviews dbt_testing.movies_users"
)
def dbt_analytics(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()