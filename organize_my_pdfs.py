#!/usr/bin/env python3
# got through all pdfs in /Users/albert/Documents/SwiftScan and check with `pdftotext <file> -` if file is ORC'd, if not, detect language (if fra, eng, deu) and use ocrmypdf for ORC'ing.
import os
import subprocess
import re

from pytz import NonExistentTimeError

def is_orc_pdf(file_path):
    """Check if a PDF file is OCR'd."""
    try:
        output = subprocess.check_output(['pdftotext', file_path, '-'], stderr=subprocess.STDOUT)
        text = output.decode('utf-8')
        return bool(text.strip())
    except subprocess.CalledProcessError:
        return False

def detect_language(file_path):
    """Detect the language of a PDF file, one of 'fra', 'eng', or 'deu'."""
    
    #     try:
    #     output = subprocess.check_output(['pdfinfo', file_path], stderr=subprocess.STDOUT)
    #     for line in output.decode('utf-8').splitlines():
    #         match = re.search(r'Language:\s*(\w+)', line)
    #         if match:
    #             return match.group(1)
    # except subprocess.CalledProcessError:
    #     return NonExistentTimeError
    
    # try:
    #     output = subprocess.check_output(['pdftotext', file_path, '-'], stderr=subprocess.STDOUT)
    #     text = output.decode('utf-8')
        
    #     # Simple regex to find language codes in the text
    #     if re.search(r'\b(fra|eng|deu)\b', text, re.IGNORECASE):
    #         match = re.search(r'\b(fra|eng|deu)\b', text, re.IGNORECASE)
    #         return match.group(0).lower()
    # except subprocess.CalledProcessError:
    #     pass
    # return None

def ocr_pdf(file_path):
    """Run OCR on a PDF file."""
    try:
        subprocess.check_call(['ocrmypdf', file_path, file_path])
    except subprocess.CalledProcessError:
        pass

def process_pdfs(directory):
    """Process all PDF files in a directory."""
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.pdf'):
                file_path = os.path.join(root, filename)
                print(f"Processing {file_path}...")
                # if not is_orc_pdf(file_path):
                #     language = detect_language(file_path)
                #     if language:
                #         print(f"Detected language for {file_path}: {language}")
                #     ocr_pdf(file_path)
