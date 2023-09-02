from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

class Book:
	id: int
	title: str
	author: str
	description: str
	rating: int
	published_year: int

	def __init__(self, id, title, author, description, rating, published_year):
		self.id = id
		self.title = title
		self.author = author
		self.description = description
		self.rating = rating
		self.published_year = published_year

#To implement validation, based on pydantic
class BookRequest(BaseModel):
	id: int | None = Field(description='id is not needed', default=None)
	title: str = Field(min_length=3, description='book title')
	author: str = Field(min_length=1)
	description: str = Field(min_length=1, max_length=100)
	rating: int = Field(gt=0, lt=6)
	published_year: int = Field(gt=1999, lt=2031)

	#This is for see an schema example on /docs
	model_config = {
		"json_schema_extra" : {
			'example': {
				'title': 'A new book',
				'author': 'codingwithroby',
				'description': 'A new description of a book',
				'rating': 5,
				'published_year': 2029
			}
		}
	}
	
BOOKS = [
	Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
	Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
	Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
	Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
	Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
	Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

app = FastAPI()


#READ
#Return specific status code after suscessful execution: status.HTTP_200_OK

@app.get("/books", status_code=status.HTTP_200_OK) #Return specific status code after suscessful execution
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)): #Path param with data validation
	for book in BOOKS:
		if book.id == book_id:
			return book
	raise HTTPException(status_code=404, detail='Item not found')

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)): #Query param with data validation
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_year: int = Query(gt=1999, lt=2031)): #Query param with data validation
    books_to_return = []
    for book in BOOKS:
        if book.published_year == published_year:
            books_to_return.append(book)
    return books_to_return


#CREATE
#Return specific status code after suscessful execution: status.HTTP_201_CREATED

def find_book_id(book: Book):
	list_ids = [b.id for b in BOOKS]
	next_id = max(list_ids) + 1
	if (book.id == None) or (book.id in list_ids):
		book.id = next_id
	return book

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest): #Notice this class BookRequest, to define a type!!!
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    

#UPDATE
#Return specific status code after suscessful execution: status.HTTP_204_NO_CONTENT

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest): #Notice this class BookRequest, to define a type!!!
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


#DELETE
#Return specific status code after suscessful execution: status.HTTP_204_NO_CONTENT

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')
