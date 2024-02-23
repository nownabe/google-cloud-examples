package main

import (
	"fmt"
	"log/slog"
	"net/http"
	"os"

	"cloud.google.com/go/compute/metadata"
)

type Service struct {
	port string

	projectID   string
	serviceName string
	version     string
	message     string
}

func newService() (*Service, error) {
	projectID, err := getProjectID()
	if err != nil {
		return nil, err
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	return &Service{
		port:        port,
		projectID:   projectID,
		serviceName: os.Getenv("K_SERVICE"),
		version:     os.Getenv("APP_VERSION"),
		message:     os.Getenv("MESSAGE"),
	}, nil
}

func (s *Service) run() error {
	slog.Warn("service is running")

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		slog.Info(s.message,
			"projectId", s.projectID,
			"serviceName", s.serviceName,
			"appVersion", s.version,
		)
		fmt.Fprintf(w, "ok")
	})

	if err := http.ListenAndServe(":"+s.port, nil); err != http.ErrServerClosed {
		return err
	}

	return nil
}

type Job struct {
	projectID string
	jobName   string
	version   string
	message   string
}

func newJob() (*Job, error) {
	projectID, err := getProjectID()
	if err != nil {
		return nil, err
	}

	return &Job{
		projectID: projectID,
		jobName:   os.Getenv("CLOUD_RUN_JOB"),
		version:   os.Getenv("APP_VERSION"),
		message:   os.Getenv("MESSAGE"),
	}, nil
}

func (j *Job) run() error {
	slog.Warn("job is running")

	slog.Info(j.message,
		"projectId", j.projectID,
		"jobName", j.jobName,
		"appVersion", j.version,
	)

	slog.Warn("job finished")

	return nil
}

func getProjectID() (string, error) {
	if projectID := os.Getenv("PROJECT_ID"); projectID != "" {
		return projectID, nil
	}
	return metadata.ProjectID()
}

func main() {
	slog.Warn("app is starting")

	if os.Getenv("CLOUD_RUN_JOB") == "" {
		s, err := newService()
		if err != nil {
			panic(err)
		}
		if err := s.run(); err != nil {
			panic(err)
		}
	} else {
		j, err := newJob()
		if err != nil {
			panic(err)
		}
		if err := j.run(); err != nil {
			panic(err)
		}
	}

	slog.Warn("app finished")
}
