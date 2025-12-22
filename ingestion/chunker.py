from typing import List, Dict, Any
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

class IPOChunker:
    def __init__(self, chunk_size=1000, chunk_overlap=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def chunk_document(self, parsed_pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Chunks the parsed page data while respecting section boundaries.
        We do NOT cross section boundaries with chunks.
        """
        final_chunks = []

        # Group pages by section to ensure chunks stay within section context
        current_section_pages = []
        last_section = None

        for page in parsed_pages:
            if last_section is not None and page['section'] != last_section:
                # Process the previous section
                final_chunks.extend(self._process_section_group(current_section_pages))
                current_section_pages = []
            
            current_section_pages.append(page)
            last_section = page['section']

        # Process the final section
        if current_section_pages:
            final_chunks.extend(self._process_section_group(current_section_pages))

        print(f"[SUCCESS] Created {len(final_chunks)} chunks.")
        return final_chunks

    def _process_section_group(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a list of pages belonging to the same section and chunks them.
        Propagates metadata (Page No) to each chunk.
        """
        section_chunks = []
        
        # Combine text for better continuity, but track page boundaries? 
        # Simpler approach for RAG: Chunk per page or small window of pages. 
        # Flow.md suggests: "Never cross sections" and "Preserve page numbers".
        # To strictly preserve "Page Number" for a specific chunk, it is safer to chunk strictly within a page 
        # OR handle multi-page chunks carefully. 
        
        # Strategy: Chunk PER PAGE to ensure precise citations. 
        # (Trade-off: Loss of context across page breaks, but vital for 'Page X' accuracy)
        
        for page in pages:
            raw_text = page['text']
            # Remove excessive whitespace
            clean_text = " ".join(raw_text.split()) 
            
            if not clean_text:
                continue

            chunks = self.splitter.split_text(clean_text)
            
            for chunk in chunks:
                chunk_metadata = {
                    "text": chunk,
                    "section": page['section'],
                    "page": page['page'],
                    "source": page['source']
                }
                section_chunks.append(chunk_metadata)

        return section_chunks
