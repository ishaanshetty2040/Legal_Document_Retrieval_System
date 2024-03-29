# import streamlit as st
# import requests

# # FastAPI backend URL
# backend_url = "http://localhost:8000/find_similar_text/"  

# st.title("Text Chunk Search App")

# # Input for the query
# query = st.text_input("Enter your query:")

# if st.button("Search"):
#     if query:
#         # Make a GET request to the FastAPI backend
#         response = requests.get(backend_url, params={"query_text": query})

#         if response.status_code == 200:
#             similar_chunks = response.json()
#             if similar_chunks:
#                 st.subheader("Similar Chunks:")
#                 for idx, chunk in enumerate(similar_chunks, 1):
#                     st.write(f"**Chunk {idx}**")
#                     context_text = chunk["chunk_text"]
#                     page_number = chunk["page_number"]
                    
#                     # Display the card with context text (chunk_text) and page number
#                     with st.container():
#                         st.write(context_text)
#                         st.write(f"Page Number: {page_number}")
#             else:
#                 st.write("No similar chunks found.")
#         else:
#             st.write("Error connecting to the backend.")
#     else:
#         st.write("Please enter a query.")


#2nd code
# import streamlit as st
# import requests

# # FastAPI backend URL
# backend_url = "http://localhost:8000/find_similar_text/"  

# st.title("Text Chunk Search App")

# # Input for the query
# query = st.text_input("Enter your query:")

# if st.button("Search"):
#     if query:
#         # Make a GET request to the FastAPI backend
#         response = requests.get(backend_url, params={"query_text": query})

#         if response.status_code == 200:
#             similar_chunks = response.json()
#             if similar_chunks:
#                 st.subheader("Similar Chunks:")
#                 for idx, chunk in enumerate(similar_chunks, 1):
#                     context_text = chunk["chunk_text"]
#                     page_number = chunk["page_number"]
                    
#                     # Display each chunk within a card
#                     st.write(f"**Chunk {idx}**")
#                     st.write(f"Page Number: {page_number}")
#                     st.write(context_text)
#                     st.markdown("---")  # Add a horizontal line to separate cards
#             else:
#                 st.write("No similar chunks found.")
#         else:
#             st.write("Error connecting to the backend.")
#     else:
#         st.write("Please enter a query.")


#3rd code

# import streamlit as st
# import requests

# # FastAPI backend URL
# backend_url = "http://localhost:8000/find_similar_text/" 

# st.title("Text Chunk Search App")

# # Input for the query
# query = st.text_input("Enter your query:")

# if st.button("Search"):
#     if query:
#         # Make a GET request to the FastAPI backend
#         response = requests.get(backend_url, params={"query_text": query})

#         if response.status_code == 200:
#             similar_chunks = response.json()
#             if similar_chunks:
#                 st.subheader("Similar Chunks:")
#                 for idx, chunk in enumerate(similar_chunks, 1):
#                     context_text = chunk["chunk_text"]
#                     page_number = chunk["page_number"]
#                     pdf_filename = chunk["document_file_name"]
                    
#                     # Display each chunk within a card
#                     st.write(f"**Chunk {idx}**")
#                     st.write(f"Page Number: {page_number}")
#                     st.write(context_text)
                    
#                     # Create a clickable link to the PDF document
#                     pdf_link = f"http://localhost:8000/pdfs/{pdf_filename}"
#                     st.write(f"View PDF: [Open PDF]({pdf_link})")
#                     st.markdown("---")  # Add a horizontal line to separate cards
#             else:
#                 st.write("No similar chunks found.")
#         else:
#             st.write("Error connecting to the backend.")
#     else:
#         st.write("Please enter a query.")


#4th code

# import streamlit as st
# import requests
# import urllib.parse

# # FastAPI backend URL
# backend_url = "http://localhost:8000/find_similar_text/"  

# st.title("Text Chunk Search App")

# # Input for the query
# query = st.text_input("Enter your query:")

# if st.button("Search"):
#     if query:
#         # Make a GET request to the FastAPI backend
#         response = requests.get(backend_url, params={"query_text": query})

#         if response.status_code == 200:
#             similar_chunks = response.json()
#             if similar_chunks:
#                 st.subheader("Similar Chunks:")
#                 for idx, chunk in enumerate(similar_chunks, 1):
#                     context_text = chunk["chunk_text"]
#                     page_number = chunk["page_number"]
#                     pdf_filename = chunk["document_file_name"]
                    
#                     # Display each chunk within a card
#                     st.write(f"**Chunk {idx}**")
#                     st.write(f"Page Number: {page_number}")
#                     st.write(context_text)
                    
#                     # Create a clickable link to the PDF document with proper encoding
#                     pdf_link = f"http://localhost:8000/pdfs/{urllib.parse.quote(pdf_filename)}#page={page_number}"
#                     st.write(f"View PDF: [Open PDF]({pdf_link})")
#                     st.markdown("---")  # Add a horizontal line to separate cards
#             else:
#                 st.write("No similar chunks found.")
#         else:
#             st.write("Error connecting to the backend.")
#     else:
#         st.write("Please enter a query.")

#5th code
# import streamlit as st
# import requests
# import tempfile
# import fitz  # PyMuPDF
# from PIL import Image
# import urllib.parse
# import base64

# # FastAPI backend URL
# backend_url = "http://localhost:8000/find_similar_text/"  

# st.title("CourtDoc Navigator 🔎")

# # Input for the query
# query = st.text_input("Enter your query:")

# if st.button("Search"):
#     if query:
#         # Make a GET request to the FastAPI backend
#         response = requests.get(backend_url, params={"query_text": query})

#         if response.status_code == 200:
#             similar_chunks = response.json()
#             if similar_chunks:
#                 st.subheader("Similar Chunks:")
#                 for idx, chunk in enumerate(similar_chunks, 1):
#                     context_text = chunk["chunk_text"]
#                     page_number = chunk["page_number"]
#                     pdf_filename = chunk["document_file_name"]

#                     # Display each chunk within a card
#                     st.write(f"**Chunk {idx}**")
#                     st.write(f"Page Number: {page_number}")
#                     st.write(context_text)

#                     # Create a clickable link to the PDF document with the page number
#                     pdf_link = f"http://localhost:8000/pdfs/{urllib.parse.quote(pdf_filename)}#page={page_number}"
#                     st.write(f"View PDF: [Open PDF]({pdf_link})")

#                     # Add a small icon for preview
#                     if st.button("Preview", key=f"preview_{idx}"):
#                         # Download the PDF page and convert it to an image
#                         pdf_url = f"http://localhost:8000/pdfs/{urllib.parse.quote(pdf_filename)}"

#                         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
#                             pdf_data = requests.get(pdf_url).content
#                             pdf_file.write(pdf_data)

#                         pdf_doc = fitz.open(pdf_file.name)
#                         pdf_page = pdf_doc.load_page(page_number -1)  # Page numbers are 1-based
#                         img = pdf_page.get_pixmap()

#                         with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as img_file:
#                             img.save(img_file.name)
#                             img_data = Image.open(img_file.name)

#                         # Convert the image to base64
#                         img_base64 = base64.b64encode(img_data.tobytes()).decode()

#                         # Display the image using HTML
#                         st.markdown(f'<img src="data:image/png;base64,{img_base64}" alt="Preview" style="max-width:100%;">')

#                     st.markdown("---")  # Add a horizontal line to separate cards
#             else:
#                 st.write("No similar chunks found.")
#         else:
#             st.write("Error connecting to the backend.")
#     else:
#         st.write("Please enter a query.")

#5th code works fine, except for the preview button

#6th code
import streamlit as st
import requests
import urllib.parse
import fitz
from io import BytesIO
from PIL import Image

# Backend URLs
backend_url = "http://localhost:8000/find_similar_text/"
summary_url = "http://localhost:8000/summarize_document/"
pdf_image_url = "http://localhost:8000/pdf_image/"
backend_url = "http://localhost:8000/find_similar_text/"  
base_url="http://localhost:8000"
# Function to display PDF page as image
def display_pdf_page_as_image(pdf_url, page_number):
    # Download the PDF file from the backend URL
    pdf_response = requests.get(pdf_url)
    
    if pdf_response.status_code == 200:
        # Open the downloaded PDF as a PyMuPDF document
        pdf_document = fitz.open(stream=pdf_response.content, filetype="pdf")
        
        # Load the specified page (Page numbers start from 0 in PyMuPDF)
        page = pdf_document.load_page(page_number - 1)
        
        # Get the page as an image (adjust scale if needed)
        image = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Adjust scale if needed
        return image
    else:
        return None  # Return None if there's an issue downloading the PDF
st.title("CourtDoc Navigator 🔎")

# Input for the query
query = st.text_input("Enter your query:")

# Checkbox for sorting by date
sort_by_date = st.checkbox("Sort by Date")

# Search button
if st.button("Search"):
    if query:
        # Make a GET request to the FastAPI backend
        params = {"query_text": query, "sort_by_date": sort_by_date}
        response = requests.get(backend_url, params=params)

        if response.status_code == 200:
            similar_chunks = response.json()
            if similar_chunks:
                st.subheader("Similar Chunks:")
                for idx, chunk in enumerate(similar_chunks, 1):
                    context_text = chunk["chunk_text"]
                    page_number = chunk["page_number"]
                    pdf_filename = chunk["document_file_name"]
                    case_date = chunk["case_date"]  # Extract case date

                    # Display each chunk
                    st.write(f"**Filename: {pdf_filename}**")
                    st.write(f"Page Number: {page_number}")
                    st.write(f"Case Date: {case_date}")  # Display case date
                    st.write(context_text)

                    # Create a clickable link to the PDF document with the page number
                    

                    pdf_link = f"http://localhost:8000/pdfs/{urllib.parse.quote(pdf_filename)}#page={page_number}"

                    
                    st.write(f"View PDF: [Open PDF]({pdf_link})")


                    pdf_url = f"http://localhost:8000/pdfs/{urllib.parse.quote(pdf_filename)}"

                    

                    # Fetch and display document summary
                    summary_response = requests.post(summary_url, json={"filepath": pdf_filename})
                    if summary_response.status_code == 200:
                        summary_text = summary_response.json().get("summary")
                        st.write("Document Summary:")
                        st.text_area(label="Summary Text", value=summary_text, height=200)
                    else:
                        st.write("Error fetching document summary.")

                    # Display PDF page as image
                    image_link = f"{base_url}/pdf_image/{urllib.parse.quote(pdf_filename)}/{page_number}"
                    st.markdown(f"Preview: [View]({image_link})")
                    button_key = f"display_page_{idx}_image" 
                    if st.button("Display Page as Image",key=button_key):
                        # pdf_url.seek(0)  # Reset file pointer to the beginning
                        image = display_pdf_page_as_image(pdf_url, page_number)
                        img_bytes = image.tobytes()
                        img = Image.open(BytesIO(img_bytes))
                        st.image(img, caption=f"Page {page_number} as Image", use_column_width=True)
                    
                    # Add a separator between chunks
                    st.markdown("---")
            else:
                st.write("No similar chunks found.")
        else:
            st.write("Error connecting to the backend.")
    else:
        st.write("Please enter a query.")







