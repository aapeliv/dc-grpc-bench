import logging
from time import sleep
from concurrent import futures

import grpc
import messages_pb2
import messages_pb2_grpc
from datetime import datetime, timedelta, timezone

from shared import timer
from google.protobuf.timestamp_pb2 import Timestamp

logger = logging.getLogger(__name__)

def now():
    return datetime.now()

def Timestamp_from_datetime(dt: datetime):
    pb_ts = Timestamp()
    pb_ts.FromDatetime(dt)
    return pb_ts

class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        handler = continuation(handler_call_details)
        prev_func = handler.unary_unary
        method = handler_call_details.method

        def timetaking_function(request, context):
            with timer(method):
                res = prev_func(request, context)
            return res

        return grpc.unary_unary_rpc_method_handler(
            timetaking_function,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )


class Servicer(messages_pb2_grpc.BenchServicer):
    def GetGroupChat(self, request, context):
        return messages_pb2.GroupChat(
            group_chat_id=51,
            title="Test title",
            member_user_ids=[2,3,4],
            admin_user_ids=[10042434,293,1],
            only_admins_invite=True,
            is_dm=False,
            created=Timestamp_from_datetime(now()),
            unseen_message_count=15,
            last_seen_message_id=8839123,
            latest_message=conversations_pb2.Message(
                message_id=119,
                author_user_id=309,
                time=Timestamp_from_datetime(now()),
                text=conversations_pb2.MessageContentText(text="this is a pretend message"),
            ),
        )


server = grpc.server(futures.ThreadPoolExecutor(max_workers=6), interceptors=[LoggingInterceptor()])
messages_pb2_grpc.add_BenchServicer_to_server(Servicer(), server)

with open("privkey.pem", "rb") as f:
    key_data = f.read()

with open("fullchain.pem", "rb") as f:
    chain_data = f.read()

creds = grpc.ssl_server_credentials([(key_data, chain_data)])
server.add_secure_port("[::]:8443", creds)
logging.info(f"Added secure port on 8443")

server.start()
server.wait_for_termination()
