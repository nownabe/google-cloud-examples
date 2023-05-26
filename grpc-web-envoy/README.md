# gRPC-Web with Sidecar Envoy on Cloud Run

## Deploy

Configure your project.

```shell
gcloud config set project YOUR-PROJECT-ID
```

Enable services.

```shell
gcloud services enable \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com
```

Create Artifact Registry repository.

```shell
gcloud artifacts repositories create \
  grpc-web \
  --location us-central1 \
  --repository-format DOCKER
```

Create Service Account for Cloud Run service.

```shell
gcloud iam service-accounts create grpc-web
```

Bind `roles/run.admin` role to Cloud Build Service Account.

```shell
gcloud projects add-iam-policy-binding \
  "$(gcloud config get project)" \
  --member "serviceAccount:$(gcloud projects describe $(gcloud config get project) --format 'value(projectNumber)')@cloudbuild.gserviceaccount.com" \
  --role "roles/run.admin"
```

Bind `roles/iam.serviceAccountUser` role to Cloud Build Service Account.

```shell
gcloud iam service-accounts add-iam-policy-binding \
  "grpc-web@$(gcloud config get project).iam.gserviceaccount.com" \
  --member "serviceAccount:$(gcloud projects describe $(gcloud config get project) --format 'value(projectNumber)')@cloudbuild.gserviceaccount.com" \
  --role "roles/iam.serviceAccountUser"
```

Build and deploy gRPC-Web backend using Cloud Build.

```shell
gcloud builds submit .
```

Allow unauthenticated requests.

```shell
gcloud run services add-iam-policy-binding \
  grpc-web \
  --region us-central1 \
  --member "allUsers" \
  --role "roles/run.invoker"
```

## Call gRPC-Web Service

Call gRPC methods from local web app.

Start web app.

```shell
cd web
npm install
GRPC_HOST="$(gcloud run services describe grpc-web --region us-central1 --format 'value(status.url)')" \
  npm start
```

Open <http://localhost:1234>

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
  localhost:50051 bookstore.BookstoreService/CreateBook
echo  "<CreateBook: Practical Go>"
grpcurl -plaintext \
  -d '{"shelf": 1, "book": {"id": 2, "title": "Practical Go"}}' \
  localhost:50051 bookstore.BookstoreService/CreateBook
echo "<ListBooks>"
grpcurl -plaintext \
  -d '{"shelf": 1}' \
  localhost:50051 bookstore.BookstoreService/ListBooks
echo "<GetBook: Mastering Go>"
grpcurl -plaintext \
  -d '{"shelf": 1, "book": 1}' \
  localhost:50051 bookstore.BookstoreService/GetBook
echo "<UpdateBook: Mastering Go>"
grpcurl -plaintext \
  -d '{"shelf": 1, "book": {"id": 1, "title": "Mastering Go, Second Edition"}}' \
  localhost:50051 bookstore.BookstoreService/UpdateBook
echo "<ListBooks>"
grpcurl -plaintext \
  -d '{"shelf": 1}' \
  localhost:50051 bookstore.BookstoreService/ListBooks
echo "<DeleteBook: Practical Go>"
grpcurl -plaintext \
  -d '{"shelf": 1, "book": 2}' \
  localhost:50051 bookstore.BookstoreService/DeleteBook
echo "<ListBooks>"
grpcurl -plaintext \
  -d '{"shelf": 1}' \
  localhost:50051 bookstore.BookstoreService/ListBooks
```

### Envoy

```shell
getenvoy run -c envoy/envoy.yaml
```

### Web Frontend

```shell
cd web
npm install
GRPC_HOST="http://localhost:8080" npm start
```

## References

* gRPC
  * BookstoreService comes from [envoy/test/proto/bookstore.proto](https://github.com/envoyproxy/envoy/blob/c2ae2211196a48b12d2e36d00c6c2889ae2f434a/test/proto/bookstore.proto)
  * [Basics tutorial | Go | gRPC](https://grpc.io/docs/languages/go/basics/)
  * [grpc-go/main.go at master · grpc/grpc-go · GitHub](https://github.com/grpc/grpc-go/blob/master/examples/helloworld/greeter_server/main.go)
  * [grpc/health-checking.md at master · grpc/grpc · GitHub](https://github.com/grpc/grpc/blob/master/doc/health-checking.md)
* gRPC-Web
  * [grpc-web/net/grpc/gateway/examples/helloworld at master · grpc/grpc-web · GitHub](https://github.com/grpc/grpc-web/tree/master/net/grpc/gateway/examples/helloworld)
  * [grpc/grpc-web: gRPC for Web Clients](https://github.com/grpc/grpc-web)
* Envoy
  * [gRPC-Web — envoy 1.27.0-dev-c2ae22 documentation](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/grpc_web_filter)
  * [CORS Configuration with Envoy](https://www.emmanuelgautier.com/blog/snippets/envoy-cors-configuration)
* Cloud Run
  * [Deploying to Cloud Run  |  Cloud Run Documentation  |  Google Cloud](https://cloud.google.com/run/docs/deploying?hl=en#sidecars)
  * [Cloud Run YAML Reference  |  Cloud Run Documentation  |  Google Cloud](https://cloud.google.com/run/docs/reference/yaml/v1)
  * [Cloud Run YAML Schema](https://run.googleapis.com/$discovery/rest?version=v1)
  * [Container health checks (services)  |  Cloud Run Documentation  |  Google Cloud](https://cloud.google.com/run/docs/configuring/healthchecks#grpc-liveness-probes)
