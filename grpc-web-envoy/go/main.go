package main

import (
	"context"
	"log"
	"net"
	"os"
	"sync"

	pb "github.com/nownabe/google-cloud-examples/grpc-web-envoy/go/gen/bookstore"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/reflection"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"
)

type shelf struct {
	books map[int64]*pb.Book
}

func newShelf() *shelf {
	return &shelf{books: make(map[int64]*pb.Book)}
}

type bookstoreService struct {
	pb.UnimplementedBookstoreServiceServer

	mu      sync.RWMutex
	shelves map[int64]*shelf
}

func (s *bookstoreService) ListBooks(req *pb.ListBooksRequest, stream pb.BookstoreService_ListBooksServer) error {
	s.mu.RLock()
	defer s.mu.RUnlock()

	shelf, ok := s.shelves[req.Shelf]
	if !ok {
		return status.Error(codes.NotFound, "shelf not found")
	}

	if shelf.books == nil {
		return status.Error(codes.Internal, "internal server error")
	}

	for _, book := range shelf.books {
		if err := stream.Send(book); err != nil {
			return err
		}
	}

	return nil
}

func (s *bookstoreService) CreateBook(ctx context.Context, req *pb.CreateBookRequest) (*pb.Book, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, ok := s.shelves[req.Shelf]; !ok {
		s.shelves[req.Shelf] = newShelf()
	}

	shelf := s.shelves[req.Shelf]

	if _, ok := shelf.books[req.Book.Id]; ok {
		return nil, status.Error(codes.AlreadyExists, "book already exists")
	}

	shelf.books[req.Book.Id] = req.Book

	return req.Book, nil
}

func (s *bookstoreService) GetBook(ctx context.Context, req *pb.GetBookRequest) (*pb.Book, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	shelf, ok := s.shelves[req.Shelf]
	if !ok {
		return nil, status.Error(codes.NotFound, "shelf not found")
	}

	if shelf.books == nil {
		return nil, status.Error(codes.Internal, "internal server error")
	}

	book, ok := shelf.books[req.Book]
	if !ok {
		return nil, status.Error(codes.NotFound, "book not found")
	}

	return book, nil
}

func (s *bookstoreService) DeleteBook(ctx context.Context, req *pb.DeleteBookRequest) (*emptypb.Empty, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	shelf, ok := s.shelves[req.Shelf]
	if !ok {
		return nil, status.Error(codes.NotFound, "shelf not found")
	}

	if shelf.books == nil {
		return nil, status.Error(codes.Internal, "internal server error")
	}

	if _, ok := shelf.books[req.Book]; !ok {
		return nil, status.Error(codes.NotFound, "book not found")
	}

	delete(shelf.books, req.Book)

	return &emptypb.Empty{}, nil
}

func (s *bookstoreService) UpdateBook(ctx context.Context, req *pb.UpdateBookRequest) (*pb.Book, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	shelf, ok := s.shelves[req.Shelf]
	if !ok {
		return nil, status.Error(codes.NotFound, "shelf not found")
	}

	if shelf.books == nil {
		return nil, status.Error(codes.Internal, "internal server error")
	}

	if _, ok := shelf.books[req.Book.Id]; !ok {
		return nil, status.Error(codes.NotFound, "book not found")
	}

	shelf.books[req.Book.Id] = req.Book

	return req.Book, nil
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "50051"
	}

	s := grpc.NewServer()

	svc := &bookstoreService{
		shelves: make(map[int64]*shelf),
	}
	pb.RegisterBookstoreServiceServer(s, svc)

	reflection.Register(s)

	lis, err := net.Listen("tcp", ":"+port)
	if err != nil {
		log.Fatalf("failed to listen: %v, err")
	}

	log.Printf("server listening at %v", lis.Addr())

	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
