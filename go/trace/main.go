package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"cloud.google.com/go/compute/metadata"
	texporter "github.com/GoogleCloudPlatform/opentelemetry-operations-go/exporter/trace"
	"go.opentelemetry.io/contrib/detectors/gcp"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.4.0"
)

func main() {
	projectID, err := metadata.ProjectID()
	if err != nil {
		log.Printf("metadata.ProjectID failed: %v", err)
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	if err := setTrace(projectID); err != nil {
		log.Printf("setTrace failed: %v", err)
	}

	propagator := otel.GetTextMapPropagator()
	tracer := otel.GetTracerProvider().Tracer("trace-demo")

	f := func(w http.ResponseWriter, r *http.Request) {
		ctx := propagator.Extract(r.Context(), propagation.HeaderCarrier(r.Header))
		ctx, span := tracer.Start(ctx, fmt.Sprintf("%s %s %s", r.Method, r.URL.Path, r.Proto))
		defer span.End()
		sc := span.SpanContext()
		fmt.Printf(`{"message":"Hello, Cloud Logging! with trace","severity":"INFO","key1":"value1","logging.googleapis.com/trace":"projects/%s/traces/%s","logging.googleapis.com/spanId":"%s","logging.googleapis.com/trace_sampled":%t}`+"\n", projectID, sc.TraceID().String(), sc.SpanID().String(), sc.IsSampled())
		time.Sleep(100 * time.Millisecond)
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
		resource.WithAttributes(semconv.ServiceNameKey.String("trace-demo")))
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
