# FIDIC Red Book 1999 Contract Clause Parser

A Python-based parser to convert FIDIC Red Book 1999 clauses into structured JSON Contract Clause Nodes.

## Project Status: ⚠️ Partially Complete

**Progress**: 40% - Parser framework complete, awaiting General Conditions source document

## Critical Issue: Missing General Conditions

The provided PDF/HTML/TXT files contain **only** the Guidance, Forms, and Annexes sections.

**The actual General Conditions (Clause 1-20 contract text) are NOT included.**

### What We Have:
- ✅ Guidance for Particular Conditions (how to modify clauses)
- ✅ Forms (Letter of Tender, Contract Agreement, etc.)
- ✅ Annexes A-G (Security/Guarantee templates)

### What's Missing:
- ❌ General Conditions - The actual contract clauses (Clause 1-20 full text)
  - e.g., Actual definitions in "1.1 Definitions"
  - e.g., Actual obligations in "4.1 Contractor's General Obligations"

## Quick Start

### Parse Guidance Sections
```bash
cd src
python3 fidic_parser.py ../data/source/fidic.txt ../output/guidance
```

### Extract PDF to Text
```bash
cd src
python3 pdf_extractor.py ../data/source/FIDIC-Red-Book-1999.pdf ../data/extracted/output.txt
```

## Project Structure

```
KOM/
├── README.md                      # This file
├── src/                           # Source code
│   ├── fidic_parser.py           # Main parser
│   └── pdf_extractor.py          # PDF extraction tool
├── data/
│   ├── source/                   # Original documents
│   │   ├── FIDIC-Red-Book-1999.pdf
│   │   ├── FIDIC-Red-Book-1999.html
│   │   └── fidic.txt
│   └── extracted/                # Extracted/processed data
│       └── fidic-complete-extracted.txt
├── output/                       # Generated JSON files
│   └── guidance/                 # Guidance section outputs (20 files)
│       ├── clause-01-general-provisions.json
│       ├── clause-02-the-employer.json
│       └── ... (18 more)
└── docs/                         # Documentation
    └── TECHNICAL_ANALYSIS.md     # Detailed technical analysis
```

## Features

### Completed ✅
- **Parser Framework**: Full implementation with dataclass-based schema
- **Pattern Recognition**: Regex-based clause, party, and obligation extraction
- **Metadata Generation**: Auto-categorization, importance levels, keywords
- **JSON Output**: Structured Contract Clause Nodes
- **PDF Extraction**: Text extraction with page markers
- **Guidance Parsing**: 20 JSON files generated for Guidance sections

### Pending ⏳
- General Conditions parsing (blocked - source document needed)
- Forms parsing (Letter of Tender, Appendix, Agreements)
- Annexes parsing (Security templates A-G)
- Sub-clause hierarchy parsing
- Complete cross-reference mapping

## JSON Schema

Each clause is exported as:

```json
{
  "clauseId": "1",
  "clauseNumber": "1",
  "title": "General Provisions",
  "level": 1,
  "summary": "Brief description...",
  "fullText": "Complete clause text...",
  "obligations": [
    {
      "party": "Contractor|Employer|Engineer",
      "action": "shall|must|may",
      "description": "What must be done",
      "condition": "if/when applicable"
    }
  ],
  "relatedClauses": ["1.1", "4.1"],
  "keywords": ["contract", "works", "payment"],
  "parties": ["Employer", "Contractor", "Engineer"],
  "metadata": {
    "section": "General Conditions",
    "importance": "high|medium|low",
    "category": "administrative|technical|financial|legal",
    "hasSubClauses": true,
    "references": {
      "crossReferences": ["Sub-Clause 1.1"],
      "externalDocs": ["Specification", "Appendix to Tender"]
    }
  },
  "subClauses": []
}
```

## Next Steps

### Option 1: Obtain General Conditions (Recommended)
- Source from FIDIC.org (official)
- Check university library (Monash)
- Request from construction/engineering firms using FIDIC contracts

### Option 2: Continue with Available Content
- Complete Forms parsing
- Complete Annexes parsing
- Build reference model from Guidance

## Technical Stack

- **Language**: Python 3.9+
- **Libraries**:
  - `pdfplumber` - PDF text extraction
  - `pypdf` - PDF processing
  - Built-in: `re`, `json`, `dataclasses`, `pathlib`
- **Output**: JSON (UTF-8)

## Requirements

```bash
pip install pdfplumber pypdf
```

## Usage Examples

### Basic Parsing
```bash
python3 src/fidic_parser.py data/source/fidic.txt output/guidance
```

### PDF Extraction
```bash
python3 src/pdf_extractor.py data/source/FIDIC-Red-Book-1999.pdf data/extracted/output.txt
```

### Future Modes (To Be Implemented)
```bash
# Parse specific sections
python3 src/fidic_parser.py --mode forms data/source/fidic.txt output/forms
python3 src/fidic_parser.py --mode annexes data/source/fidic.txt output/annexes
python3 src/fidic_parser.py --mode general_conditions data/source/gc.txt output/gc
```

## Current Outputs

**Location**: `output/guidance/`

**Files**:
- 20 clause JSON files (clause-01 through clause-20)
- 1 master index (fidic-red-book-index.json)

**Note**: Current outputs contain Guidance text (how to modify clauses), not actual General Conditions contract text.

## Contributing

This is a structured parser designed for extensibility:
- Add new parsing modes in `fidic_parser.py`
- Extend `ClauseNode` schema for additional metadata
- Implement specialized parsers for Forms/Annexes

## License

This parser is for academic/research purposes. FIDIC Red Book content is copyrighted by FIDIC.

---

**Last Updated**: 2025-01-15
**Status**: Framework complete, awaiting General Conditions source document
