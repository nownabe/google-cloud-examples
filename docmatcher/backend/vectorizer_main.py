from concurrent import futures
import logging
from os import environ, path
from tempfile import mkdtemp
import pickle

from google.cloud import storage
from gensim.models import KeyedVectors

import grpc

from gen.docmatcher.vectorizer_pb2_grpc \
    import add_VectorizerServiceServicer_to_server
from vectorizer.service import VectorizerService
from vectorizer.vectorizer import JapaneseWordExtractor, Word2Vec


logger = logging.getLogger("vectorizer")


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


def main(port: str, max_workers: int, ipadic_path: str, model_path: str):
    loader = Loader()
    ipadic_path = loader.get_ipadic_path(ipadic_path)
    model = loader.get_model(model_path)

    extractor = JapaneseWordExtractor(ipadic_path=ipadic_path)
    vectorizer = Word2Vec(word_extractor=extractor, model=model)

    service = VectorizerService(vectorizer=vectorizer)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    add_VectorizerServiceServicer_to_server(service, server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info("server started listening on %s", port)
    server.wait_for_termination()


if __name__ == "__main__":
    port = environ.get("PORT", "3003")
    max_workers = int(environ.get("MAX_WORKERS", "10"))
    ipadic_path = environ["MECAB_IPADIC"]
    model_path = environ["WORD2VEC_MODEL"]

    logging.basicConfig(level=logging.INFO)

    main(port=port,
         max_workers=max_workers,
         ipadic_path=ipadic_path,
         model_path=model_path)
