import json
import os
import sys
from tempfile import NamedTemporaryFile

import numpy as np
from google.cloud import storage

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf


BUCKET = "cloud-samples-data"
PREFIX = "ai-platform/flowers/"

tf.keras.utils.disable_interactive_logging()


def blob_to_embedding(model: tf.keras.Model,
                      blob: storage.Blob) -> list[float]:
    with NamedTemporaryFile(prefix="flowers") as temp:
        blob.download_to_filename(temp.name)
        raw = tf.io.read_file(temp.name)

    image = tf.image.decode_jpeg(raw, channels=3)
    prediction = model.predict(np.array([image.numpy()]))
    return prediction[0].tolist()


def generate_and_upload_embeddings(flower: str, destination_root: str) -> None:
    print("Loading EfficientNetB0")
    model = tf.keras.applications.EfficientNetB0(
            include_top=False, pooling="avg")

    print(f"Started generating and uploading embeddings for {flower}")

    client = storage.Client(project="gs-matching-engine")

    datapoints = []

    blobs = list(client.list_blobs(BUCKET, prefix=f"{PREFIX}{flower}/"))
    for i, blob in enumerate(blobs, 1):
        print(f"[{i:3d}/{len(blobs)}] Processing {blob.name}")

        embedding = blob_to_embedding(model, blob)
        datapoints.append({
            "id": blob.name,
            "embedding": embedding,
        })

    dst_bucket_name, dst_base = destination_root[5:].split("/", maxsplit=1)
    dst_bucket = client.bucket(dst_bucket_name)
    dst_blob = dst_bucket.blob(os.path.join(dst_base, flower + ".json"))

    with dst_blob.open(mode="w") as f:
        for datapoint in datapoints:
            f.write(json.dumps(datapoint) + "\n")

    print(f"Finished generating and uploading embeddings for {flower} 🎉")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_and_upload_embeddings.py FLOWER DESTINATION_ROOT")
        print("  FLOWER: daisy, dandelion, roses, sunflowers, or tulips")
        print("  DESTINATION_ROOT: root path of Cloud Storage like gs://my-bucket/embeddings/")
        sys.exit(1)

    generate_and_upload_embeddings(sys.argv[1], sys.argv[2])
