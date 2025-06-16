from PyPDF2 import PdfReader

class TextExtractor:

    def extract_text_from_file(self, filepath: str, content_type: str) -> str:
        if content_type == "application/pdf":
            return self.extract_text_from_pdf(filepath)
        elif content_type.startswith("text/"):
            return self.extract_text_from_txt(filepath)
        else:
            raise ValueError("Unsupported file type")

    def extract_text_from_pdf(self, filepath: str) -> str:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "").replace('\n', '')
        return text

    def extract_text_from_txt(self, filepath: str) -> str:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()