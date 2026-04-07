import os
import aiofiles
import subprocess
from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document
from app.config import settings

class TextProcessor:
    SUPPORTED_FORMATS = {
        '.txt': '_read_txt',
        '.rtf': '_read_rtf', 
        '.pdf': '_read_pdf',
        '.doc': '_read_doc',
        '.docx': '_read_docx'
    }
    
    @staticmethod
    async def extract_text(file_path: str, file_ext: str) -> str:
        """Извлечение текста из файла поддерживаемого формата"""
        method_name = TextProcessor.SUPPORTED_FORMATS.get(file_ext.lower())
        if not method_name:
            raise ValueError(f"Формат {file_ext} не поддерживается")
        
        method = getattr(TextProcessor, method_name)
        return await method(file_path)
    
    @staticmethod
    async def _read_txt(filepath: str) -> str:
        async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
            return await f.read()
    
    @staticmethod
    async def _read_rtf(filepath: str) -> str:
        from striprtf.striprtf import rtf_to_text
        async with aiofiles.open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            rtf_content = await f.read()
        return rtf_to_text(rtf_content)
    
    @staticmethod
    async def _read_pdf(filepath: str) -> str:
        text = []
        with open(filepath, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return '\n'.join(text)
    
    @staticmethod
    async def _read_docx(filepath: str) -> str:
        doc = Document(filepath)
        return '\n'.join([para.text for para in doc.paragraphs])
    
    @staticmethod
    async def _read_doc(file_path: str) -> str:
        try:
            result = subprocess.run(
                ["antiword", file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Не удалось извлечь текст из .doc файла: {e}")
        except FileNotFoundError:
            raise RuntimeError("Утилита 'antiword' не установлена. Выполните: sudo apt install antiword")
    
    @staticmethod
    def save_uploaded_file(file_content: bytes, filename: str) -> str:
        """Сохранение загруженного файла и возврат пути"""
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(exist_ok=True)
        
        filepath = upload_dir / filename
        with open(filepath, 'wb') as f:
            f.write(file_content)
        return str(filepath)