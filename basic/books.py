from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
	{'title': 'Title One', 'author': 'Author One', 'category': 'science'},
	{'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
	{'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
	{'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
	{'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
	{'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def read_all_books():
	return BOOKS

#Example:
# http://127.0.0.1:8000/books/Book%20Two
@app.get("/books/{book_title}") #Path parameter
async def read_book(book_title: str): #note the same path parameter
	for book in BOOKS:
		if book.get('title').casefold() == book_title.casefold():
			return book

#Example:
# http://127.0.0.1:8000/books/?category=math
@app.get("/books/") #Here is not a parameter
async def read_category_by_query(category: str): #Look this, category, so is by query
	books_to_return = []
	for book in BOOKS:
		if book.get('category').casefold() == category.casefold():
			books_to_return.append(book)
	return books_to_return


#Example:
# http://127.0.0.1:8000/books/Author%20One/?category=science
@app.get("/books/{book_author}/") #Path param
async def read_author_category_by_query(book_author: str, category: str): #Path and Query params
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


#Example of data to pass in body:
"""
{
	"title": "SCADA",
	"author": "Cesar",
	"category": "Python"
}
"""
#Test this from
# http://127.0.0.1:8000/docs
@app.post("/books/create_book") #Post for create
async def create_book(new_book=Body()): #Body() to get what is passed from body
    BOOKS.append(new_book) #Remember BOOKS is the list of dicts, so apend the new
    #BOOKS is in memory, after create, call the endpoint to list all books
		# http://127.0.0.1:8000/books 
		#and notice your new one :)



#Example of data to pass in body:
"""
{
	"title": "SCADA",
	"author": "Cesar Becerra",
	"category": "Python"
}
"""
#Test this from
# http://127.0.0.1:8000/docs
@app.put("/books/update_book") #PUT for UPDATE!!!
async def update_book(updated_book=Body()): #Again use Body()
	for i in range(len(BOOKS)):
		if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
			BOOKS[i] = updated_book
# http://127.0.0.1:8000/books 
#and notice your updated one :)


#Example:
# http://127.0.0.1:8000/books/delete_book/Title%20One 
@app.delete("/books/delete_book/{book_title}") #Expects a path param
async def delete_book(book_title: str):
	for i in range(len(BOOKS)): #Remember BOOKS is a list of dicts
		if BOOKS[i].get('title').casefold() == book_title.casefold():
			BOOKS.pop(i) #For delete by index
			break
# http://127.0.0.1:8000/books 
#and notice your book does not exist anymore (in memory)