package main

type tableHeap struct {
	tables []*Table
	sortBy string
}

func newTableHeap(sortBy string) *tableHeap {
	return &tableHeap{
		tables: []*Table{},
		sortBy: sortBy,
	}
}

func (h tableHeap) Len() int { return len(h.tables) }

func (h tableHeap) Less(i, j int) bool {
	if h.sortBy == sortByBytes {
		return h.tables[i].bytes < h.tables[j].bytes
	}

	return h.tables[i].rows < h.tables[j].rows
}

func (h tableHeap) Swap(i, j int) {
	h.tables[i], h.tables[j] = h.tables[j], h.tables[i]
}

func (h *tableHeap) Push(x any) {
	h.tables = append(h.tables, x.(*Table))
}

func (h *tableHeap) Pop() any {
	old := h.tables
	n := len(old)
	x := old[n-1]
	h.tables = old[0 : n-1]
	return x
}
