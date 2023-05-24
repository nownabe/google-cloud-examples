# gRPC-Web with Sidecar Envoy on Cloud Run

## Run locally

### Protobuf

Generate Go and JavaScript Code.

```shell
buf generate proto
```

### gRPC server

Run the gRPC server.

```shell
cd go
go mod install
go run main.go
```

Call methods with [grpcurl](https://github.com/fullstorydev/grpcurl).

```shell
echo "<CreateBook: Mastering Go>"
grpcurl -plaintext \
  -d '{"shelf": 1, "book": {"id": 1, "title": "Mastering Go"}}' \
  localhost:5051 bookstore.BookstoreService/CreateBook
echo  "<CreateBook: Practical Go>"
grpcurl -plaintext \
  -d '{"shelf": 1, "book": {"id": 2, "title": "Practical Go"}}' \
  localhost:5051 bookstore.BookstoreService/CreateBook
echo "<ListBooks>"
grpcurl -plaintext \
  -d '{"shelf": 1}' \
  localhost:5051 bookstore.BookstoreService/ListBooks
echo "<GetBook: Mastering Go>"
grpcurl -plaintext \
  -d '{"shelf": 1, "book": 1}' \
  localhost:5051 bookstore.BookstoreService/GetBook
echo "<UpdateBook: Mastering Go>"
grpcurl -plaintext \
  -d '{"shelf": 1, "book": {"id": 1, "title": "Mastering Go, Second Edition"}}' \
  localhost:5051 bookstore.BookstoreService/UpdateBook
echo "<ListBooks>"
grpcurl -plaintext \
  -d '{"shelf": 1}' \
  localhost:5051 bookstore.BookstoreService/ListBooks
echo "<DeleteBook: Practical Go>"
grpcurl -plaintext \
  -d '{"shelf": 1, "book": 2}' \
  localhost:5051 bookstore.BookstoreService/DeleteBook
echo "<ListBooks>"
grpcurl -plaintext \
  -d '{"shelf": 1}' \
  localhost:5051 bookstore.BookstoreService/ListBooks
```

### Envoy

```shell
getenvoy run -c envoy.yaml
```

### Web Frontend

```shell
cd web
npm install
GRPC_HOST="http://localhost:8080" npm start
```

## References

* BookstoreService comes from [envoy/test/proto/bookstore.proto](https://github.com/envoyproxy/envoy/blob/c2ae2211196a48b12d2e36d00c6c2889ae2f434a/test/proto/bookstore.proto)
* [Basics tutorial | Go | gRPC](https://grpc.io/docs/languages/go/basics/)
* [grpc-go/main.go at master · grpc/grpc-go · GitHub](https://github.com/grpc/grpc-go/blob/master/examples/helloworld/greeter_server/main.go)
* [gRPC-Web — envoy 1.27.0-dev-c2ae22 documentation](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/grpc_web_filter)
* [grpc-web/net/grpc/gateway/examples/helloworld at master · grpc/grpc-web · GitHub](https://github.com/grpc/grpc-web/tree/master/net/grpc/gateway/examples/helloworld)
* [grpc/grpc-web: gRPC for Web Clients](https://github.com/grpc/grpc-web)
