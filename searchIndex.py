
from fastapi import FastAPI, Query, Path, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import sqlite3
import os
import requests
import fitz
import base64
from PIL import Image
from fastapi.responses import StreamingResponse
from io import BytesIO
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
from datetime import datetime

app = FastAPI()

# Load the Sentence Transformer Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Dimensions for the vector embeddings
VEC_INDEX_DIM = 384

# Load the Annoy index
u = AnnoyIndex(VEC_INDEX_DIM, 'angular')
u.load("vecindex.ann")

# SQLite connection
con = sqlite3.connect("my_chunks3.db")
cur = con.cursor()

# Configure FastAPI to serve static files (PDFs)
app.mount("/pdfs", StaticFiles(directory="pdfs"), name="pdfs")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as pdf_file:
            for page in pdf_file:
                text += page.get_text()
    except Exception as e:
        print("Error:", e)
    return text

# Function to summarize text
def summarize_text(text):
    api_key = "ENTER_YOUR_API_KEY"
    endpoint = "https://api.together.xyz/v1/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": f"<s>[INST] Summarize the following text: {text} [/INST]",
        "max_tokens": 512,
        "stop": ["</s>", "[/INST]"],
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "n": 1
    }
    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

class ChunkResponse(BaseModel):
    chunk_text: str
    page_number: int
    document_file_name: str
    case_date: str

@app.get("/find_similar_text/", response_model=List[ChunkResponse])
async def read_similar_text(query_text: str, sort_by_date: Optional[bool] = False):
    """
    Given a query_text and an optional sort_by_date parameter, find the top 10 text chunks 
    from the database that are semantically similar and sort them by case date if specified.
    """

    # Convert the query text into an embedding
    embedding = model.encode([query_text])
    input_vec = embedding[0]

    # Retrieve the IDs of the top 10 most similar text chunks
    chunk_ids = u.get_nns_by_vector(input_vec, 10, search_k=-1, include_distances=False)
    
    # Build the SQL query
    sql_query = "SELECT chunk_id, chunk_text, page_number, document_file_name, case_date FROM chunks_fact WHERE chunk_id IN ({})".format(','.join(['?'] * len(chunk_ids)))
    
    # Fetch the actual text chunks from the SQLite database
    cur.execute(sql_query, chunk_ids)
    res = cur.fetchall()

    # Construct the result list
    result = [{"chunk_text": chunk[1], "page_number": chunk[2], "document_file_name": chunk[3], "case_date": chunk[4]} for chunk in res]

    # Sort the results by case date if specified
    if sort_by_date:
        result.sort(key=lambda x: datetime.strptime(x["case_date"], "%d %B, %Y"), reverse=True)

    return result

class SummaryRequest(BaseModel):
    filepath: str

class SummaryResponse(BaseModel):
    summary: str

@app.post("/summarize_document/", response_model=SummaryResponse)
async def summarize_document(request: SummaryRequest):
    """
    Given a filepath, summarize the document and return the summary.
    """
    try:
        filepath = request.filepath
        # Extract text from the PDF
        pdf_path = os.path.join("pdfs", filepath)
        extracted_text = extract_text_from_pdf(pdf_path)

        # Summarize text using Together AI API
        if extracted_text:
            summary_response = summarize_text(extracted_text)
            if summary_response:
                if summary_response.get('choices') and len(summary_response['choices']) > 0:
                    summary_text = summary_response['choices'][0]['text']
                    return {"summary": summary_text}
                else:
                    return {"summary": "No summary generated by the API."}
            else:
                return {"summary": "Failed to get response from the API."}
        else:
            return {"summary": "Failed to extract text from the PDF."}
    except Exception as e:
        return HTTPException(detail=f"Error: {e}", status_code=500)

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

pdfs_folder = "pdfs" 

@app.get("/pdf_image/{file_name}/{page_number}")
async def get_pdf_image(file_name: str = Path(...), page_number: int = Path(...)):
    pdf_path = os.path.join(pdfs_folder, file_name)
    
    if not os.path.exists(pdf_path) or not pdf_path.lower().endswith(".pdf"):
        return {"message": "PDF file not found or invalid"}

    pdf_document = fitz.open(pdf_path)
    
    if page_number < 1 or page_number > pdf_document.page_count:
        pdf_document.close()
        return {"message": "Invalid page number"}

    page = pdf_document.load_page(page_number - 1)  # Page numbers start from 0 in PyMuPDF
    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Adjust scale if needed

    # Convert the pixmap to a PIL image
    pil_image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

    # Save the PIL image as a PNG file in memory
    png_image = BytesIO()
    pil_image.save(png_image, format="PNG")
    png_image.seek(0)

    pdf_document.close()

    return StreamingResponse(png_image, media_type="image/png")
