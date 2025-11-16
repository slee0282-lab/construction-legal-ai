#!/usr/bin/env python3
"""
FIDIC Red Book 1999 Contract Clause Parser

This script parses the FIDIC Red Book 1999 document and converts all clauses
into structured JSON Contract Clause Nodes.

Author: Claude Code
Date: 2025-01-15
"""

import re
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum


class PartyType(Enum):
    """Contract parties"""
    EMPLOYER = "Employer"
    CONTRACTOR = "Contractor"
    ENGINEER = "Engineer"
    SUBCONTRACTOR = "Subcontractor"
    DAB = "DAB"


class ActionType(Enum):
    """Obligation types"""
    SHALL = "shall"  # Mandatory
    MUST = "must"    # Mandatory
    MAY = "may"      # Optional
    WILL = "will"    # Future commitment


class CategoryType(Enum):
    """Clause categories"""
    ADMINISTRATIVE = "administrative"
    TECHNICAL = "technical"
    FINANCIAL = "financial"
    LEGAL = "legal"
    PROCEDURAL = "procedural"


class ImportanceLevel(Enum):
    """Clause importance"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Obligation:
    """Represents an obligation within a clause"""
    party: str
    action: str
    description: str
    condition: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Metadata:
    """Metadata for a clause"""
    section: str
    importance: str
    category: str
    hasSubClauses: bool
    references: Dict[str, List[str]]

    def to_dict(self):
        return asdict(self)


@dataclass
class ClauseNode:
    """Contract Clause Node structure"""
    clauseId: str
    clauseNumber: str
    title: str
    parentClause: Optional[str]
    level: int
    summary: str
    fullText: str
    obligations: List[Obligation]
    relatedClauses: List[str]
    keywords: List[str]
    parties: List[str]
    metadata: Metadata
    subClauses: List['ClauseNode']

    def to_dict(self):
        result = {
            "clauseId": self.clauseId,
            "clauseNumber": self.clauseNumber,
            "title": self.title,
            "level": self.level,
            "summary": self.summary,
            "fullText": self.fullText,
            "obligations": [ob.to_dict() for ob in self.obligations],
            "relatedClauses": self.relatedClauses,
            "keywords": self.keywords,
            "parties": self.parties,
            "metadata": self.metadata.to_dict(),
            "subClauses": [sc.to_dict() for sc in self.subClauses]
        }
        if self.parentClause:
            result["parentClause"] = self.parentClause
        return result


class FIDICParser:
    """Parser for FIDIC Red Book 1999 document"""

    def __init__(self, input_file: str):
        self.input_file = Path(input_file)
        self.content = ""
        self.clauses: Dict[str, ClauseNode] = {}

        # Regex patterns
        self.clause_pattern = re.compile(
            r'^(Clause|CLAUSE)\s+(\d+)\s+(.+?)$',
            re.MULTILINE
        )
        self.subclause_pattern = re.compile(
            r'^(Sub-Clause|SUB-CLAUSE)\s+([\d.]+)\s+(.+?)$',
            re.MULTILINE
        )
        self.numbered_item_pattern = re.compile(
            r'^\s*([\d.]+)\s+(.+?)$',
            re.MULTILINE
        )

        # Party detection patterns
        self.party_patterns = {
            PartyType.EMPLOYER: re.compile(r'\b(Employer|Employer\'s)\b'),
            PartyType.CONTRACTOR: re.compile(r'\b(Contractor|Contractor\'s)\b'),
            PartyType.ENGINEER: re.compile(r'\b(Engineer|Engineer\'s)\b'),
            PartyType.SUBCONTRACTOR: re.compile(r'\b(Subcontractor|Subcontractor\'s)\b'),
            PartyType.DAB: re.compile(r'\b(DAB|Dispute Adjudication Board)\b'),
        }

        # Obligation patterns
        self.obligation_patterns = {
            ActionType.SHALL: re.compile(r'\b(shall)\b', re.IGNORECASE),
            ActionType.MUST: re.compile(r'\b(must)\b', re.IGNORECASE),
            ActionType.MAY: re.compile(r'\b(may)\b', re.IGNORECASE),
            ActionType.WILL: re.compile(r'\b(will)\b', re.IGNORECASE),
        }

        # Reference patterns
        self.clause_ref_pattern = re.compile(
            r'(Sub-)?Clause\s+([\d.]+)|clause\s+([\d.]+)',
            re.IGNORECASE
        )
        self.external_ref_pattern = re.compile(
            r'(Appendix to Tender|Specification|Drawings?|Contract|Bill of Quantities|Schedule)',
            re.IGNORECASE
        )

    def load_content(self):
        """Load the FIDIC document content"""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            self.content = f.read()
        print(f"✓ Loaded {len(self.content)} characters from {self.input_file}")

    def extract_parties(self, text: str) -> List[str]:
        """Extract parties mentioned in the text"""
        parties = set()
        for party_type, pattern in self.party_patterns.items():
            if pattern.search(text):
                parties.add(party_type.value)
        return sorted(list(parties))

    def extract_obligations(self, text: str) -> List[Obligation]:
        """Extract obligations from text"""
        obligations = []

        # Split into sentences
        sentences = re.split(r'[.!?]\s+', text)

        for sentence in sentences:
            # Check for obligation keywords
            action_type = None
            for action, pattern in self.obligation_patterns.items():
                if pattern.search(sentence):
                    action_type = action
                    break

            if not action_type:
                continue

            # Extract party
            parties = self.extract_parties(sentence)
            if not parties:
                continue

            # Extract condition (if/unless/where clauses)
            condition = None
            condition_match = re.search(
                r'\b(if|unless|where|when|provided that)\b(.+?)(?:[.;]|$)',
                sentence,
                re.IGNORECASE
            )
            if condition_match:
                condition = condition_match.group(0).strip()

            # Create obligation for each party
            for party in parties:
                obligations.append(Obligation(
                    party=party,
                    action=action_type.value,
                    description=sentence.strip()[:200],  # Limit description length
                    condition=condition
                ))

        return obligations

    def extract_related_clauses(self, text: str) -> List[str]:
        """Extract references to other clauses"""
        references = set()

        for match in self.clause_ref_pattern.finditer(text):
            # Extract the clause number from any of the capturing groups
            clause_num = match.group(2) or match.group(3)
            if clause_num:
                references.add(clause_num)

        return sorted(list(references))

    def extract_keywords(self, text: str, title: str) -> List[str]:
        """Extract keywords from title and text"""
        keywords = set()

        # Add title words (excluding common words)
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'by', 's'}
        title_words = [w.lower() for w in re.findall(r'\w+', title) if w.lower() not in common_words]
        keywords.update(title_words)

        # Extract important terms (capitalized multi-word terms)
        important_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        keywords.update([t.lower() for t in important_terms if len(t) > 3])

        return sorted(list(keywords))[:15]  # Limit to 15 keywords

    def determine_category(self, title: str, text: str) -> str:
        """Determine the category of a clause"""
        title_lower = title.lower()
        text_lower = text.lower()

        # Financial indicators
        if any(word in title_lower or word in text_lower[:500] for word in
               ['payment', 'price', 'cost', 'money', 'financial', 'currency', 'advance']):
            return CategoryType.FINANCIAL.value

        # Legal indicators
        if any(word in title_lower or word in text_lower[:500] for word in
               ['law', 'dispute', 'arbitration', 'termination', 'liability', 'indemnit']):
            return CategoryType.LEGAL.value

        # Technical indicators
        if any(word in title_lower or word in text_lower[:500] for word in
               ['test', 'completion', 'works', 'design', 'construction', 'materials', 'plant']):
            return CategoryType.TECHNICAL.value

        # Procedural indicators
        if any(word in title_lower or word in text_lower[:500] for word in
               ['procedure', 'notice', 'claim', 'time', 'delay', 'suspension']):
            return CategoryType.PROCEDURAL.value

        return CategoryType.ADMINISTRATIVE.value

    def determine_importance(self, clause_number: str, obligations: List[Obligation]) -> str:
        """Determine the importance level of a clause"""
        # Key clauses are generally high importance
        key_clauses = ['4', '8', '10', '11', '14', '15', '16', '20']

        if clause_number.split('.')[0] in key_clauses:
            return ImportanceLevel.HIGH.value

        # Clauses with many obligations are important
        if len(obligations) > 3:
            return ImportanceLevel.HIGH.value

        if len(obligations) > 1:
            return ImportanceLevel.MEDIUM.value

        return ImportanceLevel.LOW.value

    def create_summary(self, text: str, max_length: int = 300) -> str:
        """Create a summary of the clause text"""
        # Take the first paragraph or first few sentences
        paragraphs = text.strip().split('\n\n')
        if paragraphs:
            first_para = paragraphs[0].strip()
            if len(first_para) <= max_length:
                return first_para

            # Truncate at sentence boundary
            sentences = re.split(r'[.!?]\s+', first_para)
            summary = ""
            for sentence in sentences:
                if len(summary) + len(sentence) > max_length:
                    break
                summary += sentence + ". "

            return summary.strip() or first_para[:max_length] + "..."

        return text[:max_length] + "..." if len(text) > max_length else text

    def find_section_boundaries(self) -> Dict[str, tuple]:
        """Find the start and end positions of major sections"""
        boundaries = {}

        # Find Guidance section
        guidance_start = self.content.find("Guidance for the Preparation of Particular")
        if guidance_start != -1:
            boundaries['guidance_start'] = guidance_start

        # Find Forms section
        forms_start = self.content.find("LETTER OF TENDER")
        if forms_start != -1:
            boundaries['forms_start'] = forms_start

        # Find Annexes section
        annexes_start = self.content.find("Annex A")
        if annexes_start != -1:
            boundaries['annexes_start'] = annexes_start

        return boundaries

    def extract_clause_content(self, start_pos: int, end_pos: int) -> str:
        """Extract content between two positions"""
        return self.content[start_pos:end_pos].strip()

    def parse_clause_section(self, clause_num: str, title: str, content: str,
                            parent: Optional[str] = None) -> ClauseNode:
        """Parse a single clause section into a ClauseNode"""

        # Determine level (1 = main clause, 2 = sub-clause, etc.)
        level = len(clause_num.split('.'))

        # Extract information
        parties = self.extract_parties(content)
        obligations = self.extract_obligations(content)
        related_clauses = self.extract_related_clauses(content)
        keywords = self.extract_keywords(content, title)
        summary = self.create_summary(content)
        category = self.determine_category(title, content)
        importance = self.determine_importance(clause_num, obligations)

        # Extract external references
        external_refs = []
        for match in self.external_ref_pattern.finditer(content):
            external_refs.append(match.group(0))

        # Create metadata
        metadata = Metadata(
            section="General Conditions",
            importance=importance,
            category=category,
            hasSubClauses=False,  # Will be updated later
            references={
                "crossReferences": related_clauses,
                "externalDocs": list(set(external_refs))
            }
        )

        # Create clause node
        node = ClauseNode(
            clauseId=clause_num,
            clauseNumber=clause_num,
            title=title,
            parentClause=parent,
            level=level,
            summary=summary,
            fullText=content[:5000],  # Limit full text to 5000 chars
            obligations=obligations,
            relatedClauses=related_clauses,
            keywords=keywords,
            parties=parties,
            metadata=metadata,
            subClauses=[]
        )

        return node

    def parse_general_conditions(self) -> Dict[str, ClauseNode]:
        """Parse the General Conditions section (Clauses 1-20)"""
        print("\n📋 Parsing General Conditions...")

        clauses = {}

        # For now, create placeholder clauses for the main 20 clauses
        # This will be populated with actual content parsing
        clause_titles = {
            "1": "General Provisions",
            "2": "The Employer",
            "3": "The Engineer",
            "4": "The Contractor",
            "5": "Nominated Subcontractors",
            "6": "Staff and Labour",
            "7": "Plant, Materials and Workmanship",
            "8": "Commencement, Delays and Suspension",
            "9": "Tests on Completion",
            "10": "Employer's Taking Over",
            "11": "Defects Liability",
            "12": "Measurement and Evaluation",
            "13": "Variations and Adjustments",
            "14": "Contract Price and Payment",
            "15": "Termination by Employer",
            "16": "Suspension and Termination by Contractor",
            "17": "Risk and Responsibility",
            "18": "Insurance",
            "19": "Force Majeure",
            "20": "Claims, Disputes and Arbitration"
        }

        # Find each clause in the document
        for clause_num, title in clause_titles.items():
            # Search for the clause marker
            pattern = rf'(?:Clause|CLAUSE)\s+{clause_num}\s+{re.escape(title)}'
            match = re.search(pattern, self.content, re.IGNORECASE)

            if match:
                start_pos = match.start()

                # Find the end (next clause or end of section)
                next_clause_num = str(int(clause_num) + 1)
                next_pattern = rf'(?:Clause|CLAUSE)\s+{next_clause_num}\s+'
                next_match = re.search(next_pattern, self.content[start_pos + 100:], re.IGNORECASE)

                if next_match:
                    end_pos = start_pos + 100 + next_match.start()
                else:
                    # Use a reasonable default end
                    end_pos = min(start_pos + 50000, len(self.content))

                content = self.extract_clause_content(start_pos, end_pos)

                # Create clause node
                node = self.parse_clause_section(clause_num, title, content)
                clauses[clause_num] = node

                print(f"  ✓ Clause {clause_num}: {title}")
            else:
                print(f"  ✗ Clause {clause_num}: {title} (not found)")

        return clauses

    def generate_json_files(self, output_dir: str):
        """Generate JSON files for each clause"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print(f"\n📝 Generating JSON files in {output_path}...")

        for clause_id, clause_node in self.clauses.items():
            filename = f"clause-{clause_id.replace('.', '-').zfill(2)}-{clause_node.title.lower().replace(' ', '-')}.json"
            filepath = output_path / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(clause_node.to_dict(), f, indent=2, ensure_ascii=False)

            print(f"  ✓ {filename}")

    def generate_master_index(self, output_dir: str):
        """Generate master index file"""
        output_path = Path(output_dir)
        index_file = output_path / "fidic-red-book-index.json"

        index = {
            "document": "FIDIC Red Book 1999",
            "fullTitle": "Conditions of Contract for Construction",
            "edition": "First Edition 1999",
            "isbn": "2-88432-022-9",
            "totalClauses": len(self.clauses),
            "clauses": [
                {
                    "clauseId": clause.clauseId,
                    "title": clause.title,
                    "level": clause.level,
                    "hasSubClauses": clause.metadata.hasSubClauses
                }
                for clause in self.clauses.values()
            ]
        }

        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Generated master index: {index_file}")

    def parse(self):
        """Main parsing method"""
        print("🚀 Starting FIDIC Red Book 1999 Parser...")

        self.load_content()

        # Parse different sections
        self.clauses = self.parse_general_conditions()

        print(f"\n✅ Parsing complete! Extracted {len(self.clauses)} clauses.")


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python fidic_parser.py <input_file> [output_dir]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"

    parser = FIDICParser(input_file)
    parser.parse()
    parser.generate_json_files(output_dir)
    parser.generate_master_index(output_dir)


if __name__ == "__main__":
    main()
