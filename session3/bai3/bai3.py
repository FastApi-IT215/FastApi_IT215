from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Nguyen Van A",
        "category": "programming",
        "year": 2022,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Tran Van B",
        "category": "web",
        "year": 2021,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Database System",
        "author": "Le Van C",
        "category": "database",
        "year": 2020,
        "is_available": True
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Pham Van D",
        "category": "programming",
        "year": 2008,
        "is_available": True
    },
    {
        "id": 5,
        "title": "Computer Network",
        "author": "Vu Van E",
        "category": "network",
        "year": 2019,
        "is_available": False
    },
    {
        "id": 6,
        "title": "FastAPI Basic",
        "author": "Nguyen Van A",
        "category": "web",
        "year": 2023,
        "is_available": True
    }
]

@app.get("/books/statistics")
def quantity_books():
    available_books = 0   
    borrowed_books = 0
    for bo in books:
        if bo['is_available'] == True:
            available_books += 1
        else:
            borrowed_books += 1
    return {"total_books": len(books),"available_books": available_books, "borrowed_books": borrowed_books}


@app.get("/books/categories")
def get_categories():
    list_categories = []
    for bo in books:
        temp_category = bo['category']
        if temp_category is not list_categories:
            list_categories.append(temp_category)

    return { "categories": list_categories}

@app.get("/books/latest")
def book_new():
    if not books:
        return {"thong bao": "No books available"}
    
    latest_book = books[0]
    for bo in books:
        if bo['year'] > latest_book['year']:
            latest_book = bo
    
    return latest_book
