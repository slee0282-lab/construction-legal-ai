"""
FIDIC Red Book PDF Parser
Extracts PDF content to markdown format optimized for RAG applications.

Usage:
    uv run python src/pdf_parser.py

Output:
    FIDIC-Red-Book-1999.md - Structured markdown with page headers
"""

import pymupdf
from pathlib import Path

# Get the project root directory (parent of src/)
project_root = Path(__file__).parent.parent

# Define input and output paths
input_pdf = project_root / "FIDIC-Red-Book-1999.pdf"
output_md = project_root / "FIDIC-Red-Book-1999.md"

# Validate input file exists
if not input_pdf.exists():
    raise FileNotFoundError(f"PDF not found: {input_pdf}")

print(f"📄 Converting PDF: {input_pdf.name}")
print(f"📝 Output: {output_md.name}\n")

# Open the PDF document
doc = pymupdf.open(input_pdf)
total_pages = len(doc)

# Extract text and format as markdown
markdown_content = []

for page_num, page in enumerate(doc, start=1):
    print(f"Processing page {page_num}/{total_pages}...", end='\r')

    # Get plain text from page
    plain_text = page.get_text()

    # Create markdown with page header and separator
    markdown_content.append(
        f"# Page {page_num}\n\n{plain_text}\n\n---\n\n"
    )

# Save markdown output
with open(output_md, 'w', encoding='utf-8') as f:
    f.write(''.join(markdown_content))

doc.close()

# Print summary
print(f"\n\n✅ Conversion complete!")
print(f"📊 Statistics:")
print(f"   - Total pages: {total_pages}")
print(f"   - Output size: {output_md.stat().st_size / 1024:.1f} KB")
print(f"   - File location: {output_md}")
print(f"\n💡 Next steps:")
print(f"   1. Review the markdown file")
print(f"   2. Implement RAG chunking (see README.md)")
print(f"   3. Generate embeddings for vector database")
