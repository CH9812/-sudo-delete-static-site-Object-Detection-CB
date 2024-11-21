from flask import Flask, request, render_template
import os
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Function to extract text from PDF files
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text

# Function to extract text from DOCX files
def extract_text_from_docx(file_path):
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return ""

# Function to extract text from TXT files
def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return ""

# Function to determine the file type and extract text
def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

# Route for home page
@app.route("/")
def index():
    return render_template('index.html')

# Route for matching job description with resumes
@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form.get('job_description', '').strip()
        resume_files = request.files.getlist('resumes')

        # Validate inputs
        if not job_description:
            return render_template('index.html', message="Please enter a job description.")
        if not resume_files:
            return render_template('index.html', message="Please upload at least one resume.")

        resumes = []
        for resume_file in resume_files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)
            extracted_text = extract_text(filename)
            if extracted_text.strip():
                resumes.append(extracted_text)
            else:
                print(f"Failed to extract text from file: {resume_file.filename}")

        if not resumes:
            return render_template('index.html', message="No valid resumes could be processed.")

        # Vectorize job description and resumes
        try:
            vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
            vectors = vectorizer.toarray()

            # Calculate cosine similarities
            job_vector = vectors[0]
            resume_vectors = vectors[1:]
            similarities = cosine_similarity([job_vector], resume_vectors)[0]

            # Get top 3 resumes and their similarity scores
            top_indices = similarities.argsort()[-5:][::-1]
            top_resumes = [resume_files[i].filename for i in top_indices]
            similarity_scores = [round(similarities[i], 2) for i in top_indices]

            return render_template(
                'index.html', 
                message="Top matching resumes:", 
                top_resumes=top_resumes, 
                similarity_scores=similarity_scores
            )
        except Exception as e:
            print(f"Error during vectorization or similarity calculation: {e}")
            return render_template('index.html', message="An error occurred during processing.")

    return render_template('index.html')

# Main block
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
