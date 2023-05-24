import {
  Book,
  ListBooksRequest,
  CreateBookRequest,
  GetBookRequest,
  DeleteBookRequest,
  UpdateBookRequest,
} from "./gen/bookstore/bookstore_service_pb";
import { BookstoreServiceClient } from "./gen/bookstore/bookstore_service_grpc_web_pb";

const grpcHost = process.env.GRPC_HOST;
const client = new BookstoreServiceClient(grpcHost);

function renderResponseCallback(responseElementId) {
  const responseElement = document.getElementById(responseElementId);

  return (err, response) => {
    if (err) {
      responseElement.innerText = `Error: ${err.message}`
    } else {
      responseElement.innerText = JSON.stringify(response.toObject(), null, 2);
    }
  }
}

function listBooks(event) {
  event.preventDefault();
  const data = new FormData(event.target);

  const req = new ListBooksRequest();
  req.setShelf(data.get("shelf"));

  const books = [];
  const stream = client.listBooks(req);
  stream.on("data", (response) => {
    books.push(response.toObject());
  });
  stream.on("end", (end) => {
    document.getElementById("list-books-response").innerText = JSON.stringify(books, null, 2);
  })
}

function createBook(event) {
  event.preventDefault();
  const data = new FormData(event.target);

  const book = new Book();
  book.setId(data.get("book.id"));
  book.setTitle(data.get("book.title"));

  const req = new CreateBookRequest();
  req.setShelf(data.get("shelf"));
  req.setBook(book)

  client.createBook(req, {}, renderResponseCallback("create-book-response"));
}

function getBook(event) {
  event.preventDefault();
  const data = new FormData(event.target);

  const req = new GetBookRequest();
  req.setShelf(data.get("shelf"));
  req.setBook(data.get("book"));

  client.getBook(req, {}, renderResponseCallback("get-book-response"));
}

function deleteBook(event) {
  event.preventDefault();
  const data = new FormData(event.target);

  const req = new DeleteBookRequest();
  req.setShelf(data.get("shelf"));
  req.setBook(data.get("book"));

  client.deleteBook(req, {}, renderResponseCallback("delete-book-response"));
}

function updateBook(event) {
  event.preventDefault();
  const data = new FormData(event.target);

  const book = new Book();
  book.setId(data.get("book.id"));
  book.setTitle(data.get("book.title"));

  const req = new UpdateBookRequest();
  req.setShelf(data.get("shelf"));
  req.setBook(book)

  client.updateBook(req, {}, renderResponseCallback("update-book-response"));
}

document
  .getElementById("list-books-form")
  .addEventListener("submit", listBooks);

document
  .getElementById("create-book-form")
  .addEventListener("submit", createBook);

document
  .getElementById("get-book-form")
  .addEventListener("submit", getBook);

document
  .getElementById("delete-book-form")
  .addEventListener("submit", deleteBook);

document
  .getElementById("update-book-form")
  .addEventListener("submit", updateBook);