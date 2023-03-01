# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from docmatcher import vectorizer_pb2 as docmatcher_dot_vectorizer__pb2


class VectorizerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Vectorize = channel.unary_unary(
                '/docmatcher.VectorizerService/Vectorize',
                request_serializer=docmatcher_dot_vectorizer__pb2.VectorizeRequest.SerializeToString,
                response_deserializer=docmatcher_dot_vectorizer__pb2.VectorizeResponse.FromString,
                )


class VectorizerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Vectorize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VectorizerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Vectorize': grpc.unary_unary_rpc_method_handler(
                    servicer.Vectorize,
                    request_deserializer=docmatcher_dot_vectorizer__pb2.VectorizeRequest.FromString,
                    response_serializer=docmatcher_dot_vectorizer__pb2.VectorizeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'docmatcher.VectorizerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VectorizerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Vectorize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/docmatcher.VectorizerService/Vectorize',
            docmatcher_dot_vectorizer__pb2.VectorizeRequest.SerializeToString,
            docmatcher_dot_vectorizer__pb2.VectorizeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)