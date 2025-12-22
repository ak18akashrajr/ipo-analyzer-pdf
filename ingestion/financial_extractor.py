import re
from typing import Dict, Any, List

class FinancialExtractor:
    def __init__(self):
        # Regex patterns for key financial metrics
        # Note: These are heuristic-based and might need refinement for specific PDF layouts.
        self.patterns = {
            # Matches "Revenue from operations  29,493.8  24,582.0..." -> Captures first number group
            "revenue": [
                r"Revenue\s+from\s+operations[\s\S]{0,100}?([\d,]+\.?\d*)",
                r"Total\s+Income[\s\S]{0,100}?([\d,]+\.?\d*)",
                r"Revenue\s+from\s+Operations[\s\S]{0,100}?([\d,]+\.?\d*)"
            ],
            "pat": [
                r"Profit\s+for\s+the\s+period/year[\s\S]{0,100}?([\d,]+\.?\d*)",
                r"Profit\s+After\s+Tax[\s\S]{0,100}?([\d,]+\.?\d*)",
                r"Net\s+Profit[\s\S]{0,100}?([\d,]+\.?\d*)"
            ],
            # Use negative lookahead or ensure number is > 10 distinct from 1/10 face value
            # Or just look for numbers with decimal points (EPS usually has decimals)
            "eps": [
                r"Basic\s+earnings\s+per\s+equity\s+share[\s\S]{0,150}?([\d,]+\.\d+)", 
                r"Diluted\s+earnings\s+per\s+equity\s+share[\s\S]{0,150}?([\d,]+\.\d+)",
                r"EPS[\s\S]{0,150}?([\d,]+\.\d+)"
            ],
            "net_worth": [
                r"Net\s+Worth[\s\S]{0,100}?([\d,]+\.?\d*)",
            ],
            "total_borrowings": [
                # Handle "-" explicitly if possible, or ensure we don't jump too far
                r"Total\s+Borrowings[\s\S]{0,50}?(-|[\d,]+\.?\d*)", 
                r"(?:Total Debt|Non-current borrowings)[\s\S]{0,50}?(-|[\d,]+\.?\d*)",
            ]
        }

    def extract_metrics(self, text_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Scans strictly through 'FINANCIAL_STATEMENTS' section chunks to find key metrics.
        Returns a simplified dictionary of found metrics.
        """
        extracted_financials = {
            "revenue": None,
            "pat": None,
            "eps": None,
            "net_worth": None,
            "total_borrowings": None
        }

        # Filter only financial section chunks to reduce false positives
        financial_chunks = [c for c in text_chunks if c['section'] == "FINANCIAL_STATEMENTS"]
        
        if not financial_chunks:
            # Fallback: Search all chunks if section detection failed
            financial_chunks = text_chunks

        full_financial_text = " ".join([c['text'] for c in financial_chunks])
        
        # Sanitize text: Remove Rupee symbols and other likely artifacts to simplify regex matches
        full_financial_text = full_financial_text.replace('\u20b9', '').replace('Rs.', '')

        for key, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, full_financial_text, re.IGNORECASE)
                if match:
                    # Found a match, clean it and store it
                    value_str = match.group(1).replace(',', '').strip()
                    try:
                        if value_str == '-':
                            value = 0.0
                        else:
                            value = float(value_str)
                        
                        extracted_financials[key] = value
                        break # Stop after first match for this key
                    except ValueError:
                        continue
        
        print(f"[SUCCESS] Extracted Financials: {extracted_financials}")
        return extracted_financials

if __name__ == "__main__":
    # Test stub
    pass
