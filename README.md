# Job Description and Resume Matching System
### Overview
This project is a Flask-based web application designed to match job descriptions with resumes. Using natural language processing (NLP) techniques like TF-IDF and cosine similarity, it calculates the relevance between uploaded job descriptions and resumes to streamline recruitment.

### Features

Upload and process resumes and job descriptions in .docx or .pdf formats.
Extract text using docx2txt and PyPDF2 libraries.
Compute similarity scores using TF-IDF Vectorizer and cosine similarity.
Intuitive web interface for file uploads and results.
Technologies Used

Backend: Flask (Python)
NLP: TF-IDF, Cosine Similarity
File Processing: docx2txt, PyPDF2
Frontend: HTML, CSS (via Flask templates)
How to Use

Clone the repository and set up the environment.
Run the Flask application locally or deploy it on a server.
Use the web interface to upload job descriptions and resumes.
View the calculated similarity score.

### Future Enhancements

Incorporate advanced NLP techniques such as BERT or Sentence Transformers for better matching accuracy.
Support for multilingual resumes and job descriptions.
Integrate Retrieval-Augmented Generation (RAG) to provide context-aware insights.
Cloud deployment for scalability and integration with HR platforms.
Contributions
Contributions are welcome! Feel free to open issues or submit pull requests for improvements.
