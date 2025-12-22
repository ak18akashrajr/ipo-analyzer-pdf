import fitz  # PyMuPDF
import re
from typing import List, Dict, Any

class IPOParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        
        # Define regex patterns for major sections based on standard RHP structure
        # Updated to be more flexible with spacing and case
        self.section_patterns = {
            "RISK_FACTORS": re.compile(r"RISK\s+FACTORS", re.IGNORECASE),
            "FINANCIAL_STATEMENTS": re.compile(r"(?:FINANCIAL\s+STATEMENTS|CONSOLIDATED\s+FINANCIAL\s+INFORMATION|SUMMARY\s+OF\s+RESTATED\s+FINANCIAL\s+INFORMATION|RESTATED\s+FINANCIAL\s+INFORMATION)", re.IGNORECASE),
            "BUSINESS_OVERVIEW": re.compile(r"(?:BUSINESS\s+OVERVIEW|OUR\s+BUSINESS)", re.IGNORECASE),
            "MANAGEMENT_DISCUSSION": re.compile(r"MANAGEMENT['’]S\s+DISCUSSION\s+AND\s+ANALYSIS", re.IGNORECASE),
            "USE_OF_PROCEEDS": re.compile(r"USE\s+OF\s+PROCEEDS", re.IGNORECASE),
            "LEGAL_INFO": re.compile(r"LEGAL\s+AND\s+OTHER\s+INFORMATION", re.IGNORECASE),
            "SUMMARY_FINANCIALS": re.compile(r"SUMMARY\s+FINANCIAL\s+DATA", re.IGNORECASE),
        }

    def parse(self, max_pages=None) -> List[Dict[str, Any]]:
        """
        Parses the PDF page by page, extracting text and identifying sections.
        Returns a list of dictionaries containing text, page number, and section metadata.
        """
        extracted_data = []
        current_section = "INTRODUCTION" # Default start section

        # Limit pages if requested
        pages_to_process = list(enumerate(self.doc, start=1))
        if max_pages:
            pages_to_process = pages_to_process[:max_pages]

        for page_num, page in pages_to_process:
            text = page.get_text("text")  # Extract plain text
            
            # Heuristic: Check the first 1000 characters for section headers
            # (Headers might not be at the very top)
            header_check_text = text[:1000]
            
            detected_section = self._detect_section(header_check_text)
            if detected_section:
                current_section = detected_section
            
            page_data = {
                "text": text,
                "page": page_num,
                "section": current_section,
                "source": "RHP"
            }
            extracted_data.append(page_data)
            
        print(f"[SUCCESS] Parsed {len(extracted_data)} pages from {self.pdf_path}")
        return extracted_data

    def _detect_section(self, text_snippet: str) -> str:
        """
        Checks if the text snippet matches any known section header.
        """
        for section_name, pattern in self.section_patterns.items():
            if pattern.search(text_snippet):
                return section_name
        return None

if __name__ == "__main__":
    # Test block
    # parser = IPOParser("sample.pdf")
    # data = parser.parse()
    # print(data[:2])
    pass
