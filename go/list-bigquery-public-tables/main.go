package main

import (
	"container/heap"
	"context"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"
	"sync"

	"cloud.google.com/go/bigquery"
	"golang.org/x/sync/errgroup"
	"golang.org/x/text/language"
	"golang.org/x/text/message"
	"google.golang.org/api/iterator"
)

const (
	publicDataProject = "bigquery-public-data"
	sortByRows        = "rows"
	sortByBytes       = "bytes"
)

var (
	p = message.NewPrinter(language.English)
)

type Table struct {
	name  string
	rows  uint64
	bytes int64
}

func (t *Table) PrettyRows() string {
	return p.Sprintf("%d rows", t.rows)
}

func (t *Table) PrettyBytes() string {
	return p.Sprintf("%d bytes", t.bytes)
}

type Lister struct {
	mu      sync.Mutex
	heap    *tableHeap
	project string
	topN    int
	client  *bigquery.Client
}

func newLister(ctx context.Context, project, sortBy string, topN int) (*Lister, error) {
	client, err := bigquery.NewClient(ctx, project)
	if err != nil {
		return nil, fmt.Errorf("bigquery.NewClient: %w", err)
	}

	return &Lister{
		heap:    newTableHeap(sortBy),
		project: project,
		topN:    topN,
		client:  client,
	}, nil
}

func (l *Lister) push(t *Table) {
	l.mu.Lock()
	defer l.mu.Unlock()

	heap.Push(l.heap, t)

	if l.heap.Len() > l.topN {
		heap.Pop(l.heap)
	}
}

func (l *Lister) listTopTablesInDataset(ctx context.Context, dataset *bigquery.Dataset) error {
	fmt.Fprintf(os.Stderr, "Getting tables in %s...\n", dataset.DatasetID)

	iter := dataset.Tables(ctx)

	for {
		table, err := iter.Next()
		if err == iterator.Done {
			break
		} else if err != nil {
			return fmt.Errorf("iter.Next: %w", err)
		}

		md, err := table.Metadata(ctx)
		if err != nil {
			return fmt.Errorf("table.Metadata: %w", err)
		}

		l.push(&Table{
			name:  md.FullID,
			rows:  md.NumRows,
			bytes: md.NumBytes,
		})
	}

	return nil
}

func (l *Lister) listTopTables(ctx context.Context, datasetID string) ([]*Table, error) {
	if datasetID != "" {
		ds := l.client.DatasetInProject(publicDataProject, datasetID)
		if err := l.listTopTablesInDataset(ctx, ds); err != nil {
			return nil, fmt.Errorf("l.listTopTablesInDataset: %w", err)
		}
	} else {
		eg, ctx := errgroup.WithContext(ctx)

		iter := l.client.Datasets(ctx)
		iter.ProjectID = publicDataProject

		for {
			ds, err := iter.Next()
			if err == iterator.Done {
				break
			} else if err != nil {
				return nil, fmt.Errorf("iter.Next: %w", err)
			}

			eg.Go(func() error {
				return l.listTopTablesInDataset(ctx, ds)
			})
		}

		if err := eg.Wait(); err != nil {
			return nil, err
		}
	}

	tables := []*Table{}

	for l.heap.Len() > 0 {
		t := heap.Pop(l.heap).(*Table)
		tables = append([]*Table{t}, tables...)
	}

	return tables, nil
}

func main() {
	sortBy := flag.String("sortby", sortByRows, "sort tables by bytes or number of rows")
	topN := flag.Int("topn", 30, "Number of top tables to list")
	project := flag.String("project", "", "project to run APIs")
	dataset := flag.String("dataset", "", "if this is set, tables in the specified dataset will be listed")

	flag.Parse()

	ctx := context.Background()

	l, err := newLister(ctx, *project, *sortBy, *topN)
	if err != nil {
		log.Fatalf("newLister: %v", err)
	}

	tables, err := l.listTopTables(ctx, *dataset)
	if err != nil {
		log.Fatalf("l.listTopTables: %v", err)
	}

	maxNameLen := 0
	maxRowsLen := 0
	maxBytesLen := 0

	for _, t := range tables {
		nameLen := len(t.name)
		if nameLen > maxNameLen {
			maxNameLen = nameLen
		}

		rowsLen := len(t.PrettyRows())
		if rowsLen > maxRowsLen {
			maxRowsLen = rowsLen
		}

		bytesLen := len(t.PrettyBytes())
		if bytesLen > maxBytesLen {
			maxBytesLen = bytesLen
		}
	}

	for _, t := range tables {
		namePadding := maxNameLen - len(t.name) + 1
		rowsPadding := maxRowsLen - len(t.PrettyRows()) + 1
		bytesPadding := maxBytesLen - len(t.PrettyBytes()) + 1

		fmt.Printf("%s%s%s%s%s%s\n",
			t.name, strings.Repeat(" ", namePadding),
			strings.Repeat(" ", rowsPadding), t.PrettyRows(),
			strings.Repeat(" ", bytesPadding), t.PrettyBytes())
	}
}
