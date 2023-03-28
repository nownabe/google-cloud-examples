import heapq

from google.cloud import bigquery


PUBLIC_DATA_PROJECT = "bigquery-public-data"
SORT_BY_BYTES = "bytes"
SORT_BY_ROWS = "rows"


def list_top_tables_in_dataset(client: bigquery.Client,
                               heap: list[str],
                               sort_by: str,
                               top_n: int,
                               dataset: str) -> None:
    dataset_ref = bigquery.DatasetReference(PUBLIC_DATA_PROJECT, dataset)
    tables = client.list_tables(dataset=dataset_ref)

    for table_item in tables:
        table_ref = bigquery.TableReference(dataset_ref, table_item.table_id)
        table = client.get_table(table_ref)
        if sort_by == SORT_BY_BYTES:
            val = table.num_bytes
        else:
            val = table.num_rows

        heapq.heappush(heap, (val, table.full_table_id))

        if len(heap) > top_n:
            heapq.heappop(heap)


def list_top_tables(sort_by: str, project: str,
                    top_n: int, dataset: str) -> tuple[int, str]:

    client = bigquery.Client(project=project)

    heap = []

    if dataset is not None:
        list_top_tables_in_dataset(client, heap, sort_by, top_n, dataset)
    else:
        datasets = client.list_datasets(PUBLIC_DATA_PROJECT)

        for dataset in datasets:
            print(f"Getting tables in {dataset.dataset_id}...")
            list_top_tables_in_dataset(client, heap, sort_by, top_n,
                                       dataset.dataset_id)

    return [heapq.heappop(heap) for _ in range(len(heap[:top_n]))][::-1]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sort_by", type=str, default=SORT_BY_ROWS,
                        choices=[SORT_BY_ROWS, SORT_BY_BYTES])
    parser.add_argument("--project", type=str, default=None,
                        help="Project to run APIs")
    parser.add_argument("--top_n", type=int, default=30)
    parser.add_argument("--dataset", type=str, default=None)

    args = parser.parse_args()

    tables = list_top_tables(
        sort_by=args.sort_by,
        project=args.project,
        top_n=args.top_n,
        dataset=args.dataset,
    )

    max_name_length = max([len(t[1]) for t in tables])
    max_val_length = max([len(f"{t[0]:,}") for t in tables])

    suffix = "bytes" if args.sort_by == SORT_BY_BYTES else "rows"

    for t in tables:
        val = f"{t[0]:,}"
        padding = max_name_length - len(t[1]) + max_val_length - len(val) + 1
        print(f"{t[1]}{' ' * padding}{val} {suffix}")


if __name__ == "__main__":
    main()
