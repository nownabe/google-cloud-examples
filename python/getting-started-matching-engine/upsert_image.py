import os
import sys

import numpy as np
from google.cloud.aiplatform_v1 import (
    IndexServiceClient,
    UpsertDatapointsRequest,
    IndexDatapoint,
)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf

tf.keras.utils.disable_interactive_logging()


def file_to_embedding(model: tf.keras.Model, path: str) -> list[float]:
    raw = tf.io.read_file(path)
    image = tf.image.decode_jpeg(raw, channels=3)
    prediction = model.predict(np.array([image.numpy()]))
    return prediction[0].tolist()


class Upserter:
    def __init__(self, index_name: str):
        self._index_name = index_name

        location = index_name.split("/")[3]
        api_endpoint = f"{location}-aiplatform.googleapis.com"
        self._client = IndexServiceClient(
            client_options={"api_endpoint": api_endpoint}
        )

    def upsert(self,
               index_name: str,
               datapoint_id: str,
               embedding: list[float]) -> None:
        datapoint = IndexDatapoint(
            datapoint_id=datapoint_id,
            feature_vector=embedding,
        )
        request = UpsertDatapointsRequest(
            index=self._index_name,
            datapoints=[datapoint]
        )
        self._client.upsert_datapoints(request=request)


def upsert_image(index_name: str, image_path: str):
    print("Loading EfficientNetB0")
    model = tf.keras.applications.EfficientNetB0(
            include_top=False, pooling="avg")

    print(f"Started generating embeddings for {image_path}")
    embedding = file_to_embedding(model, image_path)

    upserter = Upserter(index_name=index_name)
    upserter.upsert(datapoint_id=image_path, embedding=embedding)


def main():
    if len(sys.argv) != 2:
        print("Usage: python upsert.py IMAGE_FILE")
        print("  IMAGE_FILE: path to an image file")
        sys.exit(1)

    index_name = os.environ["INDEX_NAME"]
    image_path = sys.argv[1]

    upsert_image(index_name=index_name, image_path=image_path)


if __name__ == "__main__":
    main()
