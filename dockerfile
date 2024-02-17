# Use the continuumio/anaconda3 image as a base image
FROM continuumio/anaconda3

# Install gcc and other essential build tools
RUN apt-get update && apt-get install -y build-essential

# Install the required libraries
RUN pip install --no-cache-dir \
    PyMuPDF \
    sentence_transformers \
    annoy \
    fastapi \
    uvicorn \
    jinja2 \
    python-multipart \
    sqlite-utils \
    streamlit
