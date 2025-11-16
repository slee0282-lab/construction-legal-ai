#!/usr/bin/env python3
"""
PDF Extractor for FIDIC Red Book 1999
Extracts the actual General Conditions text from the PDF
"""

import sys
from pathlib import Path

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False


def extract_with_pypdf(pdf_path: str, output_path: str):
    """Extract text using PyPDF"""
    if not HAS_PYPDF:
        print("❌ PyPDF not installed. Run: pip install pypdf")
        return False

    print(f"📄 Extracting with PyPDF from {pdf_path}...")

    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)

    print(f"   Total pages: {total_pages}")

    all_text = []

    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        all_text.append(f"\n{'='*80}\nPAGE {i}\n{'='*80}\n{text}")

        if i % 10 == 0:
            print(f"   Processed {i}/{total_pages} pages...")

    output = Path(output_path)
    with open(output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_text))

    print(f"✅ Extracted to {output_path}")
    print(f"   Total characters: {len(''.join(all_text))}")

    return True


def extract_with_pdfplumber(pdf_path: str, output_path: str):
    """Extract text using pdfplumber (better layout preservation)"""
    if not HAS_PDFPLUMBER:
        print("❌ pdfplumber not installed. Run: pip install pdfplumber")
        return False

    print(f"📄 Extracting with pdfplumber from {pdf_path}...")

    all_text = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"   Total pages: {total_pages}")

        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            all_text.append(f"\n{'='*80}\nPAGE {i}\n{'='*80}\n{text}")

            if i % 10 == 0:
                print(f"   Processed {i}/{total_pages} pages...")

    output = Path(output_path)
    with open(output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_text))

    print(f"✅ Extracted to {output_path}")
    print(f"   Total characters: {len(''.join(all_text))}")

    return True


def find_general_conditions_pages(pdf_path: str):
    """Scan PDF to find where General Conditions section starts"""
    print(f"\n🔍 Scanning PDF for General Conditions section...")

    if HAS_PDFPLUMBER:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    # Look for General Conditions markers
                    if 'General Conditions' in text and 'Clause 1' in text:
                        print(f"   ✓ Found 'General Conditions' on page {i}")

                    # Look for first clause
                    if '1.1' in text and 'Definitions' in text:
                        print(f"   ✓ Found '1.1 Definitions' on page {i}")
                        print(f"   Preview: {text[:200]}...")

    elif HAS_PYPDF:
        reader = pypdf.PdfReader(pdf_path)
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text:
                if 'General Conditions' in text and 'Clause 1' in text:
                    print(f"   ✓ Found 'General Conditions' on page {i}")

                if '1.1' in text and 'Definitions' in text:
                    print(f"   ✓ Found '1.1 Definitions' on page {i}")
                    print(f"   Preview: {text[:200]}...")


def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_extractor.py <pdf_file> [output_file]")
        print("\nThis script will:")
        print("  1. Scan the PDF to find General Conditions section")
        print("  2. Extract all text from PDF with page markers")
        print("  3. Save to text file for parsing")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "fidic-complete-extracted.txt"

    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        sys.exit(1)

    print("🚀 FIDIC PDF Text Extractor")
    print(f"   Source: {pdf_path}")
    print(f"   Output: {output_path}")

    # First, scan to find General Conditions
    find_general_conditions_pages(pdf_path)

    # Then extract full text
    print("\n" + "="*80)

    if HAS_PDFPLUMBER:
        success = extract_with_pdfplumber(pdf_path, output_path)
    elif HAS_PYPDF:
        success = extract_with_pypdf(pdf_path, output_path)
    else:
        print("\n❌ No PDF library available!")
        print("   Install one of:")
        print("   - pip install pdfplumber (recommended)")
        print("   - pip install pypdf")
        sys.exit(1)

    if success:
        print("\n✅ Extraction complete!")
        print(f"   Next step: Run parser on {output_path}")


if __name__ == "__main__":
    main()
