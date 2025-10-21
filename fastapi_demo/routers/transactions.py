import grpc
from fastapi import APIRouter, HTTPException

from fastapi_demo import transaction_pb2_grpc, transaction_pb2

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/transaction/{transaction_id}")
def get_transaction(transaction_id: int):
    # 建立一個到 gRPC server 的「channel」（通道）連線
    # insecure_channel 表示不使用 TLS/SSL（明文）。
    # with 區塊確保在區塊結束時自動關閉 channel（釋放資源）。
    with grpc.insecure_channel("localhost:50051") as channel:
        # 使用由 protoc 生成的 gRPC client 類別 TransactionServiceStub。
        # stub 是一個本地的 client 物件，用來呼叫遠端 gRPC 服務的方法（像 RPC 的 proxy）。
        stub = transaction_pb2_grpc.TransactionServiceStub(channel)
        try:
            response = stub.GetTransactionInfo(transaction_pb2.TransactionRequest(id=transaction_id))
            return {
                "id": response.id,
                "name": response.name,
                "email": response.email
            }
        except grpc.RpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error occurred: {e.details()}")