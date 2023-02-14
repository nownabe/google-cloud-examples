from logging import getLogger
from os import environ, path
from tempfile import mkdtemp
import pickle

from google.cloud.storage import Client

from vectorupdater.app import create_app
from vectorupdater.vectorizer import JapaneseWordExtractor, Word2Vec


logger = getLogger("uvicorn")


def download_ipadic_from_gcs(client: Client, ipadic_path: str) -> str:
    logger.info("started downloading ipadic from %s", ipadic_path)

    tmpdir = mkdtemp(prefix="ipadic")
    bucket_name, name = ipadic_path[5:].split("/", maxsplit=1)
    bucket = client.bucket(bucket_name)

    for blob in bucket.list_blobs(prefix=name):
        filepath = path.join(tmpdir, blob.name.split("/")[-1])
        blob.download_to_filename(filepath)

    logger.info("finished downloading ipadic")

    return tmpdir


ipadic_path = environ.get("MECAB_IPADIC")

if ipadic_path.startswith("gs://"):
    client = Client()
    ipadic_path = download_ipadic_from_gcs(ipadic_path)

model_path = environ.get("WORD2VEC_MODEL")

if model_path.startswith("gs://"):
    pass
elif model_path.endswith(".pkl"):
    with open(model_path, mode="rb") as f:
        model = pickle.load(f)


extractor = JapaneseWordExtractor(ipadic_path=ipadic_path)
vectorizer = Word2Vec(word_extractor=extractor, model=model)

app = create_app(vectorizer=vectorizer)

if __name__ == "__main__":
    import uvicorn

    port = int(environ.get("PORT", "3002"))
    log_level = environ.get("LOG_LEVEL", "info")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=log_level)
