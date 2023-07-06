# FastApi-GRPC-Microservice-App
 a biref example of how two services can communicate with grpc and also have rest api


syntax = "proto3";

package unary;

service Unary{
  // A simple RPC.
  //
  // Obtains the MessageResponse at a given position.
 rpc GetServerResponse(Message) returns (MessageResponse) {}

}

message Message{
 string message = 1;
}

message MessageResponse{
 string message = 1;
 bool received = 2;
}


python -m grpc_tools.protoc --proto_path=. ./unary.proto --python_out=. --grpc_python_out=.