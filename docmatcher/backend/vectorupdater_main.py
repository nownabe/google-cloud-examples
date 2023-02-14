from logging import getLogger
from os import environ, path
from tempfile import mkdtemp
import pickle

from google.cloud import storage
from gensim.models import KeyedVectors

from vectorupdater.app import create_app
from vectorupdater.vectorizer import JapaneseWordExtractor, Word2Vec


logger = getLogger("uvicorn")


class Loader:
    """
    The primary purpose of this class is to avoid instantiation of
    Cloud Storage Client that needs authentication.
    """

    def __init__(self):
        self.__client = None

    def get_ipadic_path(self, ipadic_path: str) -> str:
        if not ipadic_path.startswith("gs://"):
            return ipadic_path

        logger.info("started downloading ipadic from %s", ipadic_path)

        tmpdir = mkdtemp(prefix="ipadic")
        bucket_name, name = self._parse_gcs_uri(ipadic_path)
        bucket = self._client.bucket(bucket_name)

        for blob in bucket.list_blobs(prefix=name):
            filepath = path.join(tmpdir, blob.name.split("/")[-1])
            blob.download_to_filename(filepath)

        logger.info("finished downloading ipadic")

        return tmpdir

    def get_model(self, model_path: str) -> KeyedVectors:
        if model_path.startswith("gs://"):
            logger.info("started downloading word2vec model from %s", model_path)

            bucket_name, name = self._parse_gcs_uri(model_path)
            bucket = self._client.bucket(bucket_name)
            blob = bucket.blob(name)
            with blob.open(mode="rb") as f:
                model = pickle.load(f)

            logger.info("finished downloading word2vec model")

            return model
        elif model_path.endswith(".pkl"):
            with open(model_path, mode="rb") as f:
                return pickle.load(f)
        else:
            raise Exception("unknown model format")

    @property
    def _client(self) -> storage.Client:
        if self.__client is not None:
            return self.__client

        self.__client = storage.Client()
        return self.__client

    def _parse_gcs_uri(self, uri: str) -> list[str]:
        return uri[5:].split("/", maxsplit=1)


loader = Loader()
ipadic_path = loader.get_ipadic_path(environ["MECAB_IPADIC"])
model = loader.get_model(environ["WORD2VEC_MODEL"])

extractor = JapaneseWordExtractor(ipadic_path=ipadic_path)
vectorizer = Word2Vec(word_extractor=extractor, model=model)

app = create_app(vectorizer=vectorizer)

if __name__ == "__main__":
    import uvicorn

    port = int(environ.get("PORT", "3002"))
    log_level = environ.get("LOG_LEVEL", "info")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=log_level)
