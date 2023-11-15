# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from annoy import AnnoyIndex
# import sqlite3
# from sentence_transformers import SentenceTransformer
# from typing import List, Dict

# app = FastAPI()

# # Load the Sentence Transformer Model
# # model = SentenceTransformer("thenlper/gte-large")
# # VEC_INDEX_DIM = 1024

# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Dimensions for the vector embeddings (adjust based on model's output)
# VEC_INDEX_DIM = 384


# # Load the Annoy index
# u = AnnoyIndex(VEC_INDEX_DIM, 'angular')
# u.load("vecindex.ann")

# # SQLite connection
# con = sqlite3.connect("my_chunks2.db")
# cur = con.cursor()

# # Configure FastAPI to serve static files (PDFs)
# app.mount("/pdfs", StaticFiles(directory="pdfs"), name="pdfs")

# @app.get("/find_similar_text/", response_model=List[Dict[str, str]])
# async def read_similar_text(query_text: str):
#     """
#     Given a query_text, find the top 10 text chunks from the database that are semantically similar.
#     """

#     # Convert the query text into an embedding
#     embedding = model.encode([query_text])
#     input_vec = embedding[0]

#     # Retrieve the IDs of the top 10 most similar text chunks
#     chunk_ids = u.get_nns_by_vector(input_vec, 10, search_k=-1, include_distances=False)
#     print(chunk_ids)
#     # Fetch the actual text chunks from the SQLite database
#     list_chunk_ids = ','.join([str(k) for k in chunk_ids])
#     cur.execute("select chunk_id, chunk_text,page_number,document_file_name from chunks_fact where chunk_id in (" + list_chunk_ids + ")")
#     res = cur.fetchall()
    
#     # Construct the result list
#     result = [{ "chunk_text": chunk[1],"page_number":str(chunk[2]),"document_file_name":chunk[3]} for chunk in res]
#     return result


#random testing here going on
#"chunk_id": str(chunk[0]),
# You would then run this API using a tool like Uvicorn and send GET requests to the defined endpoint.


#original code
# from annoy import AnnoyIndex
# import sqlite3
# from sentence_transformers import SentenceTransformer


# Load the Sentence Transformer Model
# We'll use this model to convert our query text into a vector embedding.


# model = SentenceTransformer("thenlper/gte-large")
# VEC_INDEX_DIM = 1024

# u = AnnoyIndex(VEC_INDEX_DIM, 'angular')
# u.load("vecindex.ann")

# Generate the Embedding for the Query Text
# Let's convert the query text into an embedding using the Sentence Transformer model


# text = "domestic abuse"
# embedding = model.encode([text])
# input_vec = embedding[0]


# Retrieve the IDs of the top 10 most similar text chunks based on the query text's embedding:

# chunk_ids = u.get_nns_by_vector(input_vec, 10, search_k=-1, include_distances=False)
# print(chunk_ids)

# Retrieve the Actual Text Chunks from the SQLite Database
# First, establish a connection to the SQLite database.


# con = sqlite3.connect("my_chunks2.db")
# cur = con.cursor()

# cur.execute("SELECT chunk_id FROM chunks_fact LIMIT 50")

# # Fetch all the rows from the result
# chunk_ids = cur.fetchall()

# # Print the list of chunk_ids
# for chunk_id in chunk_ids:
#     print(chunk_id[0])
# Then, retrieve and print the original query text:


# list_chunk_ids = ','.join([str(k) for k in chunk_ids])
# cur.execute("select chunk_id, chunk_text from chunks_fact where chunk_id in (" + list_chunk_ids + ")")
# res = cur.fetchall()

# for i in res:
#     print(i[1])
#     print("----------")


from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from annoy import AnnoyIndex
import sqlite3
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from fastapi.responses import HTMLResponse
import requests
import base64
import fitz

app = FastAPI()

# Load the Sentence Transformer Model
# model = SentenceTransformer("thenlper/gte-large")
# VEC_INDEX_DIM = 1024

model = SentenceTransformer("all-MiniLM-L6-v2")

# Dimensions for the vector embeddings (adjust based on model's output)
VEC_INDEX_DIM = 384

# Load the Annoy index
u = AnnoyIndex(VEC_INDEX_DIM, 'angular')
u.load("vecindex.ann")

# SQLite connection
con = sqlite3.connect("my_chunks2.db")
cur = con.cursor()

# Configure FastAPI to serve static files (PDFs)
app.mount("/pdfs", StaticFiles(directory="pdfs"), name="pdfs")


@app.get("/find_similar_text/", response_model=List[Dict[str, str]])
async def read_similar_text(query_text: str):
    """
    Given a query_text, find the top 10 text chunks from the database that are semantically similar.
    """

    # Convert the query text into an embedding
    embedding = model.encode([query_text])
    input_vec = embedding[0]

    # Retrieve the IDs of the top 10 most similar text chunks
    chunk_ids = u.get_nns_by_vector(input_vec, 10, search_k=-1, include_distances=False)
    print(chunk_ids)
    # Fetch the actual text chunks from the SQLite database
    list_chunk_ids = ','.join([str(k) for k in chunk_ids])
    cur.execute(
        "SELECT chunk_id, chunk_text, page_number, document_file_name FROM chunks_fact WHERE chunk_id IN (" + list_chunk_ids + ")"
    )
    res = cur.fetchall()

    # Construct the result list
    result = [{"chunk_text": chunk[1], "page_number": str(chunk[2]), "document_file_name": chunk[3]} for chunk in res]
    return result


# Server-side route to handle PDF preview
@app.get("/preview-pdf", response_class=HTMLResponse)
async def preview_pdf(pdf_url: str = Query(...), page_number: int = Query(...)):
    # Download the PDF page and convert it to an image
    pdf_data = requests.get(pdf_url).content
    pdf_file_name = "temp.pdf"
    with open(pdf_file_name, "wb") as pdf_file:
        pdf_file.write(pdf_data)

    pdf_doc = fitz.open(pdf_file_name)
    pdf_page = pdf_doc.load_page(page_number - 1)  # Page numbers are 1-based
    img = pdf_page.get_pixmap()

    # Convert the image to base64
    img_byte_array = img.get_image_data()
    img_base64 = base64.b64encode(img_byte_array).decode()

    # Embed the image in an HTML response
    html_response = f"<img src='data:image/png;base64,{img_base64}' alt='Preview' style='max-width:100%;'>"
    return HTMLResponse(content=html_response, status_code=200)
