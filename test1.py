from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2


app = FastAPI()
data = []

db_name = "apitest"
db_user = "postgres"
db_pswd = "1234"
db_host = "localhost"
db_port = "5432"

conn = psycopg2.connect(
    dbname = db_name,
    user = db_user,
    password = db_pswd,
    host = db_host,
    port = db_port
)


class Book(BaseModel):
    title: str
    author: str
    publisher: str


@app.post("/book")
def createbook(book: Book):
    data.append(book.dict())
    cursor = conn.cursor()
    insert_query = "INSERT INTO book (title, author, publisher) VALUES (%s, %s, %s)"

    cursor.execute(insert_query, (book.title, book.author, book.publisher))

    conn.commit()

    cursor.close()
    return book

@app.get("/{title}")
def readbook(title: str):
    cursor = conn.cursor()

    select_query = "SELECT title, author, publisher from book WHERE title = %s"
    cursor.execute(select_query, (title,))

    book  = cursor.fetchone()
    
    cursor.close()
    if book:

        return book
    else:
        return {"Error":"Data does not exist"}

@app.put("/book/{title}")
def updatebook(title: str, book: Book):
    cursor = conn.cursor()

    update_query = "UPDATE book SET author=%s, publisher=%s WHERE title = %s"
    cursor.execute(update_query, (book.author, book.publisher, title))
    conn.commit()
    cursor.close

    return {"msg":"values updated"}


@app.delete("/book/{title}")
def deletebook(title: str):
    cursor = conn.cursor()

    delete_query = "DELETE FROM book WHERE title = %s"
    cursor.execute(delete_query, (title,))
    conn.commit()
    cursor.close
    return {"msg":"data delete successfully"}