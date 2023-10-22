package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"cloud.google.com/go/compute/metadata"
	texporter "github.com/GoogleCloudPlatform/opentelemetry-operations-go/exporter/trace"
	"go.opentelemetry.io/contrib/detectors/gcp"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.4.0"
	"go.opentelemetry.io/otel/trace"
)

/*
TODO: ログの検証
 - Span.AddEventやSpan.SetStatus, SetName, SetAttributes, RecordError など
*/

var projectID string

func logSpan(spanCtx trace.SpanContext, prefix string) {
	b := strings.Builder{}
	fmt.Fprint(&b, `{`)
	fmt.Fprint(&b, `"severity":"INFO",`)
	fmt.Fprintf(&b, `"message":"[%s] IsValid=%t, TraceID=%s, SpanID=%s, IsSampled=%t",`, prefix, spanCtx.IsValid(), spanCtx.TraceID(), spanCtx.SpanID(), spanCtx.IsSampled())
	fmt.Fprintf(&b, `"logging.googleapis.com/trace":"projects/%s/traces/%s",`, projectID, spanCtx.TraceID())
	fmt.Fprintf(&b, `"logging.googleapis.com/spanId":"%s",`, spanCtx.SpanID())
	fmt.Fprintf(&b, `"logging.googleapis.com/trace_sampled":%t`, spanCtx.IsSampled())
	fmt.Fprintf(&b, `}`)
	fmt.Fprintf(&b, "\n")
	fmt.Print(b.String())
}

func main() {
	var err error

	projectID, err = metadata.ProjectID()
	if err != nil {
		log.Printf("metadata.ProjectID failed: %v", err)
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	app2URL := os.Getenv("APP2_URL")

	if err := setTrace(projectID); err != nil {
		log.Printf("setTrace failed: %v", err)
	}

	propagator := otel.GetTextMapPropagator()
	tracer := otel.GetTracerProvider().Tracer("run-trace-app1")

	callApp2 := func(ctx context.Context) error {
		ctx, span := tracer.Start(ctx, "callApp2")
		defer span.End()

		spanCtx := span.SpanContext()
		logSpan(spanCtx, "app1:3")

		req, err := http.NewRequestWithContext(ctx, http.MethodGet, app2URL, nil)
		if err != nil {
			return fmt.Errorf("http.NewRequestWithContext: %w", err)
		}
		propagator.Inject(ctx, propagation.HeaderCarrier(req.Header))

		res, err := http.DefaultClient.Do(req)
		if err != nil {
			return fmt.Errorf("http.DefaultClient.Do: %w", err)
		}
		defer res.Body.Close()

		return nil
	}

	f := func(w http.ResponseWriter, r *http.Request) {
		ctx := r.Context()
		fmt.Printf("[app1] Traceparent=%q\n", r.Header.Get("traceparent"))
		fmt.Printf("[app1] X-Cloud-Trace-Context=%q\n", r.Header.Get("X-Cloud-Trace-Context"))

		ctx = propagator.Extract(ctx, propagation.HeaderCarrier(r.Header))
		spanCtx := trace.SpanContextFromContext(ctx)
		logSpan(spanCtx, "app1:1")

		ctx, span := tracer.Start(ctx, fmt.Sprintf("%s %s %s", r.Method, r.URL.Path, r.Proto))
		defer span.End()
		spanCtx = span.SpanContext()
		logSpan(spanCtx, "app1:2")

		callApp2(ctx)

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
		resource.WithAttributes(semconv.ServiceNameKey.String("run-trace-app1")))
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
