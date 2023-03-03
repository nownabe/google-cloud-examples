import os
from tempfile import NamedTemporaryFile

import numpy as np
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.io import read_file
from tensorflow.image import decode_jpeg
from fastapi import FastAPI
from pydantic import BaseModel, Field
from google.cloud import storage
from google.cloud.aiplatform_v1 import (
    IndexServiceClient,
    UpsertDatapointsRequest,
    IndexDatapoint,
)

INDEX_NAME = os.environ["INDEX_NAME"]

BUCKET_NAME = "cloud-samples-data"
FLOWER_BASE = "ai-platform/flowers"
LOCATION = INDEX_NAME.split("/")[3]
API_ENDPOINT = f"{LOCATION}-aiplatform.googleapis.com"

model = EfficientNetB0(include_top=False, pooling="avg")
bucket = storage.Client().bucket(BUCKET_NAME)
index = IndexServiceClient(client_options={"api_endpoint": API_ENDPOINT})
app = FastAPI()


class RootResponse(BaseModel):
    ok: bool


@app.get("/")
async def root() -> RootResponse:
    return RootResponse(ok=True)


class CreateEmbeddingRequest(BaseModel):
    name: str = Field(
        ...,
        description="""path to flower image file following
gs://cloud-samples-data/ai-platform/flowers/.
For example, 'tulips/100930342_92e8746431_n.jpg'""",
    )


class CreateEmbeddingResponse(BaseModel):
    id: str
    embedding: list[float]


@app.post("/embeddings")
async def create_embedding(req: CreateEmbeddingRequest) -> CreateEmbeddingResponse:
    blob = bucket.blob(os.path.join(FLOWER_BASE, req.name))
    with NamedTemporaryFile(prefix="updater") as temp:
        blob.download_to_filename(temp.name)
        raw = read_file(temp.name)

    image = decode_jpeg(raw)
    embedding = model.predict(np.array([image.numpy()]))[0].tolist()

    # https://github.com/googleapis/python-aiplatform/blob/v1.22.0/google/cloud/aiplatform_v1/types/index.py#L183
    datapoint = IndexDatapoint(datapoint_id=req.name, feature_vector=embedding)

    # https://github.com/googleapis/python-aiplatform/blob/v1.22.0/google/cloud/aiplatform_v1/types/index_service.py#L250
    upsert_req = UpsertDatapointsRequest(index=INDEX_NAME, datapoints=[datapoint])

    # https://github.com/googleapis/python-aiplatform/blob/v1.22.0/google/cloud/aiplatform_v1/services/index_service/client.py#L1089
    index.upsert_datapoints(request=upsert_req)

    return CreateEmbeddingResponse(id=req.name, embedding=embedding)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    uvicorn.Server(config).run()
