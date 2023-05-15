import io

import streamlit as st
from google.cloud import bigquery
import vertexai
from vertexai.preview.language_models import TextGenerationModel


MODEL_NAME = "text-bison@001"
TEMPERATURE = 0.2
TOP_K = 0.8
TOP_P = 40


client = bigquery.Client()
vertexai.init()


def render_prompt(project_id: str,
                  dataset_id: str,
                  table_id: str,
                  user_prompt: str) -> str:
    table = client.get_table(f"{project_id}.{dataset_id}.{table_id}")

    restriction = "None"

    partitioning = table.time_partitioning
    if partitioning and partitioning.require_partition_filter:
        restriction = f"You MUST filter `{partitioning.field}` field in a `where` clause."

    with io.StringIO("") as buf:
        client.schema_to_json(table.schema, buf)
        schema = buf.getvalue()

    prompt = f"""
You are a skillful data scientist. Write a BigQuery SQL to answer user's prompt based on the following context.

----
Format: Plain SQL, no Markdown
Table: `{table.full_table_id}`
Restriction: {restriction}
Schema:
```json
{schema}
```
----

User's prompt: {user_prompt}
    """

    return prompt


def predict(prompt: str) -> str:
    model = TextGenerationModel.from_pretrained(MODEL_NAME)
    return model.predict(
        prompt,
        temperature=TEMPERATURE,
        top_k=TOP_K,
        top_p=TOP_P,
    ).text


def run_query(query):
    return client.query(query).to_dataframe()


def main():
    project_id = st.text_input("Project ID", value="bigquery-public-data")
    dataset_id = st.text_input("Dataset ID", value="wikipedia")
    table_id = st.text_input("Table ID", value="pageviews_2023")
    user_prompt = st.text_area("Prompt", value="Show top 10 popular articles in Japan in May, 2023.")
    is_clicked = st.button("Query")

    if is_clicked:
        st.markdown("## Rendered prompt")
        prompt = render_prompt(project_id, dataset_id, table_id, user_prompt)
        st.markdown(prompt)

        st.markdown("## Generated SQL by PaLM API")
        query = predict(prompt)
        st.markdown(f"```sql\n{query}\n```")

        st.markdown("## Query Result")
        results = run_query(query)
        st.table(results)


if __name__ == "__main__":
    main()
