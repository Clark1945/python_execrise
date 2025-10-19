import grpc
from concurrent import futures

from fastapi_demo import transaction_pb2_grpc, transaction_pb2

### 模擬一個TransactionService 代表了與當前Server互動的另一個Server


class TransactionService(transaction_pb2_grpc.TransactionServiceServicer):
    def GetTransactionInfo(self, request, context) -> transaction_pb2.TransactionResponse:
        # 模擬資料庫查詢
        transaction_data = {
            1: ("Clark", "clark@example.com"),
            2: ("Alice", "alice@example.com"),
        }
        name, email = transaction_data.get(request.id, ("Unknown", "none"))
        return transaction_pb2.TransactionResponse(id=request.id, name=name, email=email)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_pb2_grpc.add_TransactionServiceServicer_to_server(TransactionService(), server)
    server.add_insecure_port("0.0.0.0:50051")
    print("🚀 gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
