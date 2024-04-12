
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







