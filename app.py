from flask import Flask, render_template, request
import os
import fitz
from datetime import datetime
import csv

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        uploaded_files = request.files.getlist('files[]')
        user_keywords = request.form.get('keywords', '').split(',')

        print(f'User Keywords: {user_keywords}')

        
        save_keywords_to_csv(user_keywords)

        result_messages = process_resume(uploaded_files, user_keywords)
        return '<br>'.join(result_messages)
        
    except Exception as e:
        return f'Error: {e}'

def save_keywords_to_csv(keywords):
    try:
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        filename = 'user_keywords.csv'

        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['Date', 'Keywords']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            
            if os.stat(filename).st_size == 0:
                writer.writeheader()

            
            writer.writerow({'Date': current_date, 'Keywords': ', '.join(keywords)})
    except Exception as e:
        print(f'Error saving keywords: {e}')
    


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        folder_name = 'contact'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        filename = os.path.join(folder_name, f"{name}.txt")
        with open(filename, 'w') as f:
            f.write(f"Name: {name}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Message:\n{message}\n")
        
        return render_template('contact.html', name=name)
    return render_template('contact.html')

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
                
                
                extracted_text_lower = extracted_text.lower()
                user_keywords_lower = [keyword.lower() for keyword in user_keywords]
                
                matched_keywords = [keyword for keyword in user_keywords_lower if keyword in extracted_text_lower]

                if extracted_text and matched_keywords:
                    result_messages.append(f'{uploaded_file.filename} --> <span style="color:blue;">Shortlisted and Uploaded!</span>')
                else:
                    os.remove(file_path)
                    if not extracted_text:
                        result_messages.append(f'{uploaded_file.filename}--><span style="color:red;">Not shortlisted.</span> ')
                    elif not matched_keywords:
                        result_messages.append(f'{uploaded_file.filename}--><span style="color:red;">Not shortlisted.</span> ')
            else:
                result_messages.append(f'{uploaded_file.filename} -->has an unsupported file format. Only PDF files are supported.')

        return result_messages
    except Exception as e:
        return [f'Error: {e}']



if __name__ == '__main__':
    app.run(debug=True)
