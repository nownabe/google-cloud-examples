#---- builder
FROM golang:1.22-bookworm AS builder

ENV CGO_ENABLED 0
ENV GOOS linux
ENV GOARCH amd64

WORKDIR /go/src/github.com/nownabe/google-cloud-examples/cloud-deploy/app
COPY main.go go.mod go.sum ./
RUN go build -a -trimpath -o /go/bin/app .

#---- runtime
FROM gcr.io/distroless/static-debian12:nonroot
ARG app_version=v0.0.0
ENV APP_VERSION=$app_version

COPY --from=builder /go/bin/app /app

ENTRYPOINT ["/app"]
