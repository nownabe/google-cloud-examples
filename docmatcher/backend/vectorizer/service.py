from gen.docmatcher import vectorizer_pb2 as pb
from gen.docmatcher import vectorizer_pb2_grpc as grpc
from .vectorizer import Vectorizer


class VectorizerService(grpc.VectorizerServiceServicer):
    def __init__(self, vectorizer: Vectorizer):
        self._vectorizer = vectorizer

    def Vectorize(self, request: pb.VectorizeRequest, context):
        vector = self._vectorizer.vectorize(request.content)

        return pb.VectorizeResponse(vector=vector.tolist())
