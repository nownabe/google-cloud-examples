# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
References

- https://cloud.google.com/run/docs/authenticating/service-to-service?hl=ja#use_the_authentication_libraries
- https://github.com/googleapis/python-aiplatform/blob/main/google/cloud/aiplatform_v1beta1/services/match_service/client.py
- https://github.com/googleapis/python-aiplatform/blob/main/google/cloud/aiplatform_v1beta1/types/match_service.py
- https://github.com/googleapis/python-aiplatform/blob/v1.24.1/google/cloud/aiplatform/matching_engine/matching_engine_index_endpoint.py#L75
"""

import json
import os
import sys
from urllib import request

import numpy as np
from google.cloud.aiplatform.matching_engine import MatchingEngineIndexEndpoint
from google.auth.transport.requests import Request
import google.auth
from google.cloud import aiplatform_v1beta1 as vertexai

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf

tf.keras.utils.disable_interactive_logging()


def file_to_embedding(model: tf.keras.Model, path: str) -> list[float]:
    raw = tf.io.read_file(path)
    image = tf.image.decode_jpeg(raw, channels=3)
    prediction = model.predict(np.array([image.numpy()]))
    return prediction[0].tolist()


class Matcher:
    def __init__(self, index_endpoint_name: str, deployed_index_id: str):
        self._index_endpoint_name = index_endpoint_name
        self._deployed_index_id = deployed_index_id

        self._client = vertexai.MatchServiceClient(
            client_options={"api_endpoint": self._public_endpoint()}
        )

    def find_neighbors(self, embedding: list[float], neighbor_count: int):
        datapoint = vertexai.IndexDatapoint(
            datapoint_id="dummy-id",
            feature_vector=embedding
        )
        query = vertexai.FindNeighborsRequest.Query(datapoint=datapoint)
        request = vertexai.FindNeighborsRequest(
            index_endpoint=self._index_endpoint_name,
            deployed_index_id=self._deployed_index_id,
            queries=[query],
        )

        resp = self._client.find_neighbors(request)

        return resp.nearest_neighbors[0].neighbors

    def find_neighbors_rest(self, embedding: list[float], neighbor_count: int):
        endpoint_base = f"https://{self._public_endpoint()}/v1beta1"
        endpoint = f"{endpoint_base}/{self._index_endpoint_name}:findNeighbors"

        query = {
            "datapoint": {
                "datapoint_id": "dummy-id",
                "feature_vector": embedding,
            },
            "neighbor_count": neighbor_count,
        }
        data = {
            "deployed_index_id": self._deployed_index_id,
            "queries": [query]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._access_token()}",
        }

        req = request.Request(endpoint,
                              method="POST",
                              headers=headers,
                              data=json.dumps(data).encode("utf-8"))

        with request.urlopen(req) as res:
            resp = json.loads(res.read())

        return resp["nearestNeighbors"][0]["neighbors"]

    def _public_endpoint(self) -> str:
        endpoint = MatchingEngineIndexEndpoint(
            index_endpoint_name=self._index_endpoint_name
        )
        return endpoint.gca_resource.public_endpoint_domain_name

    def _access_token(self) -> str:
        creds, _ = google.auth.default()
        creds.refresh(Request())
        return creds.token


def search_for_similar_image(index_endpoint_name: str,
                             deployed_index_id: str,
                             image_path: str) -> None:
    print("Loading EfficientNetB0")
    model = tf.keras.applications.EfficientNetB0(
            include_top=False, pooling="avg")

    print(f"Started generating embeddings for {image_path}")
    embedding = file_to_embedding(model, image_path)

    matcher = Matcher(index_endpoint_name, deployed_index_id)
    neighbors = matcher.find_neighbors(embedding, 10)

    for neighbor in neighbors:
        datapoint_id = neighbor.datapoint.datapoint_id
        distance = neighbor.distance
        print(f"{datapoint_id}\tdistance={distance}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python search_for_similar_image.py IMAGE_FILE")
        print("  IMAGE_FILE: path to an image file")
        sys.exit(1)

    index_endpoint_name = os.environ["INDEX_ENDPOINT_NAME"]
    deployed_index_id = os.environ["DEPLOYED_INDEX_ID"]
    image_path = sys.argv[1]

    search_for_similar_image(index_endpoint_name=index_endpoint_name,
                             deployed_index_id=deployed_index_id,
                             image_path=image_path)


if __name__ == "__main__":
    main()
