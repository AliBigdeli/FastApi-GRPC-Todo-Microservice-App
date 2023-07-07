FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=50051

# Copy the application code to the container image
WORKDIR /usr/src/app

# Install application dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Expose the gRPC port
EXPOSE $PORT

# Copy the program source files
COPY ./app .

# Compile the gRPC protobuf files
RUN python -m grpc_tools.protoc -I ./protobuf --python_out=. --grpc_python_out=. todo.proto

# Start the gRPC server
# CMD [ "python", "main.py" ]