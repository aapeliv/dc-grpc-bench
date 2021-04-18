from time import sleep

import grpc
import messages_pb2
import messages_pb2_grpc

from shared import timer


class LoggingInterceptor(grpc.UnaryUnaryClientInterceptor):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        with timer("query"):
            ret = continuation(client_call_details, request)
        return ret

channel = grpc.secure_channel("dgb-tests.coucher.org:8443", credentials=grpc.ssl_channel_credentials())
intercepted_channel = grpc.intercept_channel(channel, LoggingInterceptor())
stub = messages_pb2_grpc.BenchStub(intercepted_channel)

while True:
    with timer("outer"):
        stub.GetGroupChat(messages_pb2.GetGroupChatReq(group_chat_id=15))
