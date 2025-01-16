from typing import List, Union
from pathlib import Path
import PyPDF2
import docx
import json

class DataLoader:    
    @staticmethod
    def load_document(file_path: Union[str, Path]) -> str:
        file_path = Path(file_path)
        
        if file_path.suffix == '.pdf':
            return DataLoader._load_pdf(file_path)
        elif file_path.suffix == '.txt':
            return DataLoader._load_text(file_path)
        elif file_path.suffix in ['.docx', '.doc']:
            return DataLoader._load_docx(file_path)
        elif file_path.suffix == '.json':
            return DataLoader._load_json(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

    @staticmethod
    def _load_pdf(file_path: Path) -> str:
        text = []
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            return "\n".join(text)
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")

    @staticmethod
    def _load_text(file_path: Path) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")

    @staticmethod
    def _load_docx(file_path: Path) -> str:
        pass

    @staticmethod
    def _load_json(file_path: Path) -> str:
        pass
