# your_script.py
import sys
import json

def process_resume(json_path, keywords):
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            resume_data = json.load(json_file)
            
            resume_text = resume_data.get('text', '')
            
            matched_keywords = [keyword for keyword in keywords if keyword.lower() in resume_text.lower()]
            
            if matched_keywords:
                print(f'Resume matched keywords: {matched_keywords}')
            else:
                print('Resume did not match any keywords. Not shortlisted.')
    except FileNotFoundError:
        print(f'File not found: {json_path}')
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON: {e}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python your_script.py <json_path> <comma-separated-keywords>')
    else:
        json_path = sys.argv[1]
        keywords = sys.argv[2].split(',')
        process_resume(json_path, keywords)
