FROM python:3.10-slim-buster

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --upgrade pip  && \
    pip install --no-cache-dir -r requirements.txt

COPY ./app .

# Compile the gRPC protobuf files
RUN python -m grpc_tools.protoc -I ./protobuf --python_out=. --grpc_python_out=. todo.proto