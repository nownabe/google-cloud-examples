package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"cloud.google.com/go/compute/metadata"
	texporter "github.com/GoogleCloudPlatform/opentelemetry-operations-go/exporter/trace"
	"go.nownabe.dev/clog"
	"go.nownabe.dev/clog/errors"
	"go.opentelemetry.io/contrib/detectors/gcp"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/codes"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.4.0"
	"go.opentelemetry.io/otel/trace"
)

var projectID string

func logSpan(ctx context.Context, prefix string) {
	spanCtx := trace.SpanContextFromContext(ctx)
	clog.Infof(ctx, "[%s] IsValid=%t, TraceID=%s, SpanID=%s, IsSampled=%t", prefix, spanCtx.IsValid(), spanCtx.TraceID(), spanCtx.SpanID(), spanCtx.IsSampled())
}

func main() {
	ctx := context.Background()

	projectID, err := metadata.ProjectID()
	if err != nil {
		log.Printf("metadata.ProjectID failed: %v", err)
	}

	logger := clog.New(os.Stdout, clog.SeverityInfo, true, clog.WithTrace(projectID))
	clog.SetDefault(logger)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	if err := setTrace(projectID); err != nil {
		clog.Err(ctx, errors.Errorf("setTrace failed: %w", err))
	}

	propagator := otel.GetTextMapPropagator()
	tracer := otel.GetTracerProvider().Tracer("trace-run-app2")

	f := func(w http.ResponseWriter, r *http.Request) {
		ctx := r.Context()
		fmt.Printf("[app2] Traceparent=%q\n", r.Header.Get("traceparent"))
		fmt.Printf("[app2] X-Cloud-Trace-Context=%q\n", r.Header.Get("X-Cloud-Trace-Context"))

		ctx = propagator.Extract(ctx, propagation.HeaderCarrier(r.Header))
		logSpan(ctx, "app2:1")

		ctx, span := tracer.Start(ctx, fmt.Sprintf("%s %s %s", r.Method, r.URL.Path, r.Proto))
		defer span.End()
		logSpan(ctx, "app2:2")

		span.AddEvent("app2 event") // event can be seen on Trace explorer

		err := errors.New("app2 error")
		clog.Err(ctx, err)
		span.SetStatus(codes.Error, err.Error()) // No effect

		/*
			"exception" can be seen on Trace explorer
			with "app2 error" in 'exception.message', "*errors.WithStack" in 'exception.type',
			and stacktrace in 'exception.stacktrace' but stactrace is less meaningful.
			https://github.com/open-telemetry/opentelemetry-go/blob/main/sdk/trace/span.go#L432
		*/
		span.RecordError(err, trace.WithStackTrace(true))

		w.WriteHeader(http.StatusOK)
	}

	http.HandleFunc("/", f)

	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Printf("http.ListenAndServe: %v", err)
	}
}

func setTrace(projectID string) error {
	exporter, err := texporter.New(texporter.WithProjectID(projectID))
	if err != nil {
		return fmt.Errorf("texporter.New: %w", err)
	}

	res, err := resource.New(context.Background(),
		resource.WithDetectors(gcp.NewDetector()),
		resource.WithTelemetrySDK(),
		resource.WithAttributes(semconv.ServiceNameKey.String("trace-run-app2")))
	if err != nil {
		return fmt.Errorf("resource.New: %w", err)
	}

	tp := sdktrace.NewTracerProvider(
		sdktrace.WithSampler(sdktrace.AlwaysSample()),
		sdktrace.WithBatcher(exporter),
		sdktrace.WithResource(res),
	)
	otel.SetTracerProvider(tp)
	otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(propagation.TraceContext{}, propagation.Baggage{}))

	return nil
}
