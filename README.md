1. Tenets
Precision: Prioritize accuracy and relevance in event extraction 
Contextual comprehension: Focus on capturing the context surrounding extracted events and participants.
User-centric design: Design the tool with the end-users, legal professionals, in mind, ensuring a user-friendly interface and intuitive functionalities.

2. Executive summary/Synopsis

Our idea tackles a significant issue that attorneys in Indian courts deal with: the laborious and prone to error manual analysis of unstructured legal case documents.
Insufficient contextual knowledge frequently causes delays and imprecise case comprehension. 
We suggest creating an automated event extraction tool as a solution to this. This program efficiently extracts important events, important players and timelines.
Optimizing case analysis through an intuitive interface, guaranteeing prompt and precise insights.

3. Measures of success


Contribution to Legal Research: The project's influence on legal research and analysis, demonstrated through citations, adoption in academic studies, and advancements in legal technology, indicating its impact and success.
Accuracy of Event Extraction: The system's ability to accurately identify and extract key events from legal case documents.
Improved Legal Insights: The system's capacity to provide meaningful and relevant insights from extracted events, aiding in trend identification.
User Acceptance and Satisfaction: Positive feedback from legal professionals, researchers, and stakeholders who use the system, indicating its value and usability.
Scalability and Maintenance: The system's scalability to manage increasing volumes of legal case documents and its capability for ongoing maintenance and updates.


4. In Scope
Develop a natural language processing (NLP) system capable of understanding user queries in natural language.
Integrate a search functionality that accepts natural language queries and retrieves relevant documents from a database.
Provide a user-friendly interface for entering queries and viewing search results.
Implement a document preview feature that displays a snippet or preview of the PDF page most relevant to the query.
Enable users to access the full PDF document directly from the search results.
Ensure accuracy and relevance of search results by leveraging advanced NLP techniques.

5. Out of Scope
Offer translation services for documents in languages other than the one in which the query is made.
Support handwritten or image-based queries for document retrieval.
Include advanced document analysis features such as sentiment analysis beyond the scope of relevance determination.



6. Open issues

Optimal Embedding Model Selection
Handling Document Variances
User Interface Design for Accessibility
Scalability and Performance
Integration with Existing Legal Systems
Handling Ambiguities in Legal Language


7. Use Cases
Legal Document Analysis and Review:
Case Preparation and Strategy Development
Legal Research and Information Retrieval



8.Proposed solution summary
















9. Dependencies

 User Interface
The user interface will consist of a search bar where users can input keywords. Focus on a clean and user-friendly layout.
The tech stack involves Streamlit.

Search Engine 
The search engine will process user-entered keywords and search through the legal documents.
Text Processing and Embedding Libraries:
sentence_transformers: Used for converting textual data into dense vector embeddings.
annoy: Employed for building and querying the approximate nearest neighbors (ANN) index, enhancing the efficiency of similarity searches.
Web Frameworks:
FastAPI: Used for building the backend API to handle requests for similar text chunks and serve static PDF files.
Document Parser
Responsible for parsing the legal documents( PyMuPDF)
Database
To store metadata about the legal documents, like keywords and links to corresponding PDF files
We have chosen SQLite since it is an SQL DB which offers NoSQL capabilities for unstructured data.
PDF Renderer
Once relevant cases are identified, the PDF renderer component will retrieve and display the corresponding PDF files.
PyMuPDF 
Image Processing Libraries:
PIL (Pillow): Utilized for converting image data and generating image previews of PDF pages.




10.Functional requirements
Users should be able to search and retrieve specific events, entities, or documents based on keywords
Capable of identifying and extracting critical events, key participants, and timelines from parsed legal documents.
Provide a user-friendly interface for legal professionals to interact with the system, enabling quick and accurate case analysis.
Ensure that the system can handle a growing volume of documents and users while maintaining optimal performance and responsiveness.

11. Non Functional Requirements
Performance: The system shall provide fast and responsive search functionality, with query response times optimized for user satisfaction
Extendability / Maintenance: The codebase shall be well-documented to facilitate ease of understanding and maintenance by future developers.
