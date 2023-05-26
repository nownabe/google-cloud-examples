FROM golang:1.20.4 AS build-stage

ENV CGO_ENABLED=0
ENV GOOS=linux
ENV GOARCH=amd64

WORKDIR /src

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build \
  -o /app \
  -a \
  -ldflags "-s -w -extldflags '-static'" \
  -trimpath

FROM gcr.io/distroless/static-debian11

ENV PORT=50051

WORKDIR /
COPY --from=build-stage /app /app

USER nonroot:nonroot

ENTRYPOINT ["/app"]
