from os import environ

from google.cloud import spanner


project_id = environ.get("SPANNER_PROJECT_ID")
instance_id = environ.get("SPANNER_INSTANCE_ID")
database_id = environ.get("SPANNER_DATABASE_ID")


client = spanner.Client(project=project_id)
config_name = f"{project_id}/instanceConfigs/regional-us-central1"

instance = client.instance(
    instance_id,
    configuration_name=config_name,
    display_name="Doc Matcher",
    node_count=1,
)

instance.create().result(300)

print("created instance")

with open("db/schema.sql") as f:
    schema = f.read()

database = instance.database(
    database_id,
    ddl_statements=schema.split(";")[:-1]
)

database.create().result(300)

print("created database")
