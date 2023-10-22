FROM golang:1.21 as builder

ENV CGO_ENABLED=0
ENV GOOS=linux
ENV GOARCH=amd64

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download
COPY . ./

RUN go build -a -trimpath -ldflags "-s -w -extldflags '-static'" -mod=readonly -v -o /bin/app

FROM gcr.io/distroless/static

COPY --from=builder /bin/app /bin/app

ENTRYPOINT ["/bin/app"]