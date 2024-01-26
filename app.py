from flask import Flask, render_template, request
import os
import fitz

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        uploaded_files = request.files.getlist('files[]')
        user_keywords = request.form.get('keywords','').split(',')

        # Print for debugging purposes
        print(f'User Keywords: {user_keywords}')

        result_messages = process_resume(uploaded_files, user_keywords)
        return '<br>'.join(result_messages)
    except Exception as e:
        return f'Error: {e}'


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_number in range(doc.page_count):
        page = doc[page_number]
        text += page.get_text()
    return text

def process_resume(file_paths, user_keywords):
    try:
        result_messages = []

        for uploaded_file in file_paths:
            file_path = os.path.join('uploads', uploaded_file.filename)
            uploaded_file.save(file_path)

            if file_path.lower().endswith('.pdf'):
                extracted_text = extract_text_from_pdf(file_path)
                
                # Convert both the extracted text and user keywords to lowercase
                # Convert both the extracted text and user keywords to lowercase
                extracted_text_lower = extracted_text.lower()
                user_keywords_lower = [keyword.lower() for keyword in user_keywords]
                # Check for case-insensitive keyword matches
                matched_keywords = [keyword for keyword in user_keywords_lower if keyword in extracted_text_lower]

                if extracted_text and matched_keywords:
                    result_messages.append(f'Resume {uploaded_file.filename} matched keywords: {matched_keywords}. Shortlisted!')
                else:
                    # Optionally, you can delete the file to avoid cluttering the uploads folder
                    os.remove(file_path)
                    if not extracted_text:
                        result_messages.append(f'Resume {uploaded_file.filename} has no text extracted. Not shortlisted. File not saved.')
                    elif not matched_keywords:
                        result_messages.append(f'Resume {uploaded_file.filename} did not match any user keywords. Not shortlisted. File not saved.')
            else:
                result_messages.append(f'Resume {uploaded_file.filename} has an unsupported file format. Only PDF files are supported.')

        return result_messages
    except Exception as e:
        return [f'Error: {e}']



if __name__ == '__main__':
    app.run(debug=True)
