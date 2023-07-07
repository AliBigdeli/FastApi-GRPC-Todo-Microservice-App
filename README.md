<div align="center">
<h1 align="center">FastAPI Integrated with gRPC Todo App in Microservice</h1>
<h3 align="center">Sample Project of how to use grpc and apigateway in a microservice architecture</h3>
</div>
<p align="center">
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://fastapi.tiangolo.com/" target="_blank"> <img src="https://styles.redditmedia.com/t5_22y58b/styles/communityIcon_r5ax236rfw961.png" alt="fastapi" width="40" height="40"/> </a>
<a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://www.postgresql.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a>
<a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a>
<a href="https://grpc.io/" target="_blank"> <img src="https://grpc.io/img/logos/grpc-icon-color.png" alt="grpc" width="40" height="40"/> </a>
<a href="https://grpc.io/" target="_blank"> <img src="https://camo.githubusercontent.com/69904c66b71d0d32dab9ce4eff70605368fef35c8dcc4faa03fae5b394b33016/68747470733a2f2f7777772e66726565636f646563616d702e6f72672f6e6577732f636f6e74656e742f696d616765732f73697a652f77323030302f323032302f30352f756e6e616d65642d312e706e67" alt="protobuf" width="70" height="40"/> </a>
</p>

# Guideline
- [Guideline](#guideline)
- [Goal](#goal)
- [Development usage](#development-usage)
  - [Clone the repo](#clone-the-repo)
  - [docker-compose](#docker-compose)
  - [Build everything](#build-everything)
- [Schema](#schema)
- [what is Kong?](#what-is-kong)
- [what is grpc?](#what-is-grpc)
- [what is protobuf?](#what-is-protobuf)
- [Hamravesh Deployment](#hamravesh-deployment)
- [License](#license)
- [Bugs](#bugs)

# Goal
This project is meant to be a guidance of how to setup grpc server and use it in other apis communications


# Development usage
You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
It's available on Windows, macOS and most distros of Linux. 

If you're using Windows, it will be expected that you're following along inside
of [WSL or WSL
2](https://nickjanetakis.com/blog/a-linux-dev-environment-on-windows-with-wsl-2-docker-desktop-and-more).

That's because we're going to be running shell commands. You can always modify
these commands for PowerShell if you want.


## Clone the repo
Clone this repo anywhere you want and move into the directory:
```bash
git clone https://github.com/AliBigdeli/FastApi-GRPC-Todo-Microservice-App.git
```

## docker-compose
the config file includes 4 services:
- kong : as the api gateway which is declarative
- postgres-db : as the database to handle data storage
- todo_grpc : grpc server to serve the crud
- todo_api : fastapi application to handle requests through kong gateway

```yaml
version: '3.9'

services:

  # defining the name of the service
  kong:

    # defining the image we want to use as base
    image: kong:3.1.1-alpine
    
    # defingin container name
    container_name: kong

    # implementing the config for db less configs
    volumes:
      - ./kong/kong.yml:/usr/local/kong/declarative/kong.yml

    # declaring the environment variables 
    environment:
      - KONG_DATABASE=off
      - KONG_DECLARATIVE_CONFIG=/usr/local/kong/declarative/kong.yml
      - KONG_PROXY_ACCESS_LOG=/dev/stdout
      - KONG_ADMIN_ACCESS_LOG=/dev/stdout
      - KONG_PROXY_ERROR_LOG=/dev/stderr
      - KONG_ADMIN_ERROR_LOG=/dev/stderr
      - KONG_ADMIN_LISTEN=0.0.0.0:8001

    # outer ports
    ports:
      - "80:8000"
      - "8001:8001"
  
  postgres-db:
    container_name: postgres-db
    image: postgres:15-alpine
    volumes:
      - ./postgre/data:/var/lib/postgresql/data
    expose:
      - 5432
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres


    restart: always

  todo_api:
    build: 
      context: ./services/todo-api
      dockerfile: ./Dockerfile
    container_name: todo_api
    command: sh -c "uvicorn main:app --host 0.0.0.0 --port 8000"
    volumes:
      - ./services/todo-api/main.py:/user/src/main.py
    expose:
      - 8000
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres-db/postgres
    depends_on:
      - postgres-db
    restart: on-failure

  todo_grpc:
    container_name: todo_grpc
    build: 
      context: ./services/todo-grpc
      dockerfile: ./Dockerfile
    expose:
      - 50051
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres-db/postgres
    depends_on:
      - postgres-db
    restart: on-failure

```

## Build everything

*The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python + requirements dependencies.*

```bash
docker compose up --build
```

Now that everything is built and running we can treat it like any other FastAPI
app. Visit <http://localhost/todo/swagger> in your favorite browser.

**Note:** If you receive an error about a port being in use? Chances are it's because
something on your machine is already running on port 8000. then you have to change the docker-compose.yml file according to your needs.

# Schema
<div align="center" ><img loading="lazy" style="width:400px" src="./docs/schema.png"></div>


# what is Kong?
Kong is an open-source API gateway and service mesh that was built to manage, secure, and scale microservices and APIs. It was created by Kong Inc. and is available under the Apache 2.0 license.

API gateways are tools that sit between client applications and the backend services that they rely on, providing an additional layer of security, control, and management. Kong provides a range of features that help to simplify and streamline the process of building and managing APIs. Some of the key features of Kong include:

- Routing and Load Balancing: Kong can route incoming requests to the appropriate backend service and distribute traffic across multiple instances of the service for load balancing purposes.

- Authentication and Authorization: Kong supports a variety of authentication and authorization mechanisms, including OAuth2, JWT, and API keys, to ensure that only authorized clients can access the API.

- Traffic Control and Rate Limiting: Kong provides fine-grained control over the amount of traffic that can be handled by the API, allowing administrators to set limits on the number of requests that can be made per second or per minute.

- Analytics and Monitoring: Kong provides detailed analytics and monitoring capabilities, allowing administrators to track API usage and performance in real-time.

- Plugin Architecture: Kong supports a wide range of plugins that can be used to extend its functionality, including plugins for logging, caching, transformations, and more.

Overall, Kong provides a powerful set of tools for managing APIs and microservices, offering a range of features that can help to improve security, scalability, and performance.

in order to deploy and use kong you can use the following repo: <https://github.com/AliBigdeli/ApiGateway-Hamravesh-Docker-Kong-Template.git>

# what is grpc?

gRPC (gRPC Remote Procedure Calls) is an open-source framework for building high-performance, language-agnostic, and platform-independent RPC (Remote Procedure Call) systems. It was developed by Google and is part of the Cloud Native Computing Foundation (CNCF).

gRPC allows developers to define the structure of their APIs using Protocol Buffers, a language-agnostic binary serialization format. It supports multiple programming languages, including C++, Java, Python, Ruby, Go, Node.js, and many others. With gRPC, developers can define their service interfaces once and generate client and server-side code for multiple languages automatically.

gRPC uses HTTP/2 as its transport protocol, which provides several benefits over HTTP/1.1, such as multiplexing multiple requests over a single connection, header compression, and server push. It also supports bi-directional streaming and flow control, making it ideal for building real-time communication systems, such as chat applications and live streaming services.

Overall, gRPC simplifies the process of building distributed systems by providing developers with a high-performance, scalable, and efficient RPC framework that works across multiple languages and platforms.

# what is protobuf?

Protocol Buffers, or protobuf for short, is a language-agnostic binary serialization format created by Google. It is used to serialize structured data for communication between different services or for storing data in a compact manner. 

Protocol Buffers define a language- and platform-neutral format for exchanging structured data. It allows data to be serialized to a compact binary format, making it easy to transmit over a network or store in a file. Protobuf messages are defined using a simple language called the Protocol Buffer Language, which is used to describe the structure of the data being serialized. The language is designed to be easy to read and write, and the resulting serialized data is both compact and efficient to parse.

One of the key advantages of using Protocol Buffers is that it allows for backwards compatibility when evolving the structure of data over time. This is because Protocol Buffers are designed to be extensible and allow for the addition of new fields without breaking existing clients. It also makes it easy to generate code for multiple programming languages, as the protobuf specification can be used as input to code generators that produce language-specific classes or structures for representing the data.

Overall, Protocol Buffers offer a lightweight, efficient, and flexible way to serialize structured data, making them a popular choice for use in distributed systems and other applications where data exchange and storage are critical.

# Hamravesh Deployment

if you are interested in how you can deploy it in hamravesh service provider you can use the following document:

[Hamravesh deployment document](hamravesh-deployment/README.md)


# License
MIT.


# Bugs
Feel free to let me know if something needs to be fixed. or even any features seems to be needed in this repo.
