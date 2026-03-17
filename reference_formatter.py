import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ReferenceFormat(Enum):
    GB_T_7714 = "GB/T 7714"
    IEEE = "IEEE"
    APA = "APA"
    MLA = "MLA"
    CHICAGO = "Chicago"
    SPRINGER = "Springer"
    ELSEVIER = "Elsevier"
    CUSTOM = "自定义"


@dataclass
class Reference:
    authors: List[str]
    title: str
    source: str
    year: str
    volume: str = ""
    issue: str = ""
    pages: str = ""
    publisher: str = ""
    location: str = ""
    doi: str = ""
    url: str = ""
    ref_type: str = "journal"
    number: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'authors': self.authors,
            'title': self.title,
            'source': self.source,
            'year': self.year,
            'volume': self.volume,
            'issue': self.issue,
            'pages': self.pages,
            'publisher': self.publisher,
            'location': self.location,
            'doi': self.doi,
            'url': self.url,
            'ref_type': self.ref_type,
            'number': self.number
        }


class ReferenceParser:
    @staticmethod
    def parse_single(text: str, number: int = 1) -> Optional[Reference]:
        text = text.strip()
        if not text:
            return None
        
        text = re.sub(r'^\[\d+\]\s*', '', text)
        text = re.sub(r'^\d+\.\s*', '', text)
        
        ref_type = ReferenceParser._detect_type(text)
        authors = ReferenceParser._extract_authors(text)
        title = ReferenceParser._extract_title(text)
        year = ReferenceParser._extract_year(text)
        source = ReferenceParser._extract_source(text)
        volume, issue, pages = ReferenceParser._extract_journal_info(text)
        publisher, location = ReferenceParser._extract_publisher_info(text)
        doi = ReferenceParser._extract_doi(text)
        url = ReferenceParser._extract_url(text)
        
        return Reference(
            authors=authors,
            title=title,
            source=source,
            year=year,
            volume=volume,
            issue=issue,
            pages=pages,
            publisher=publisher,
            location=location,
            doi=doi,
            url=url,
            ref_type=ref_type,
            number=number
        )
    
    @staticmethod
    def parse_multiple(text: str) -> List[Reference]:
        lines = text.strip().split('\n')
        references = []
        num = 1
        
        for line in lines:
            line = line.strip()
            if line:
                ref = ReferenceParser.parse_single(line, num)
                if ref:
                    references.append(ref)
                    num += 1
        
        return references
    
    @staticmethod
    def _detect_type(text: str) -> str:
        if re.search(r'\[M\]|专著|出版社', text, re.IGNORECASE):
            return 'book'
        elif re.search(r'\[D\]|学位论文|博士|硕士', text, re.IGNORECASE):
            return 'thesis'
        elif re.search(r'\[C\]|会议|Conference', text, re.IGNORECASE):
            return 'conference'
        elif re.search(r'\[N\]|报纸|Newspaper', text, re.IGNORECASE):
            return 'newspaper'
        elif re.search(r'\[R\]|报告|Report', text, re.IGNORECASE):
            return 'report'
        elif re.search(r'\[P\]|专利|Patent', text, re.IGNORECASE):
            return 'patent'
        elif re.search(r'\[EB/OL\]|http|www\.|网页', text, re.IGNORECASE):
            return 'online'
        else:
            return 'journal'
    
    @staticmethod
    def _extract_authors(text: str) -> List[str]:
        patterns = [
            r'^([^.]+?)\.',
            r'^([^,]+?),',
            r'^([^\d]+?)(?=\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                author_str = match.group(1).strip()
                authors = re.split(r'[,，、;；和与]', author_str)
                return [a.strip() for a in authors if a.strip()]
        
        return []
    
    @staticmethod
    def _extract_title(text: str) -> str:
        patterns = [
            r'\.\s*([^\.]+?)\s*\[',
            r'\.\s*([^\.]+?)\s*[JMCND]',
            r'\.\s*([^\.]+?)\s*\.',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return ""
    
    @staticmethod
    def _extract_year(text: str) -> str:
        match = re.search(r'\b(19|20)\d{2}\b', text)
        return match.group(0) if match else ""
    
    @staticmethod
    def _extract_source(text: str) -> str:
        patterns = [
            r'\[J\]\s*([^,，\.]+)',
            r'\[M\]\s*([^,，\.]+)',
            r'\.\s*([^,，\.]+?)\s*,?\s*\d{4}',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return ""
    
    @staticmethod
    def _extract_journal_info(text: str) -> Tuple[str, str, str]:
        volume = ""
        issue = ""
        pages = ""
        
        vol_match = re.search(r'[,，]\s*(\d+)\s*卷|Vol\.?\s*(\d+)', text, re.IGNORECASE)
        if vol_match:
            volume = vol_match.group(1) or vol_match.group(2)
        
        issue_match = re.search(r'[,，]\s*\((\d+)\)|No\.?\s*(\d+)|期\s*(\d+)', text, re.IGNORECASE)
        if issue_match:
            issue = issue_match.group(1) or issue_match.group(2) or issue_match.group(3)
        
        pages_match = re.search(r'[:：]\s*(\d+[-–]\d+|\d+)', text)
        if pages_match:
            pages = pages_match.group(1)
        
        return volume, issue, pages
    
    @staticmethod
    def _extract_publisher_info(text: str) -> Tuple[str, str]:
        publisher = ""
        location = ""
        
        pub_match = re.search(r'[:：]\s*([^,，]+?)(?:,|，|\d{4})', text)
        if pub_match:
            publisher = pub_match.group(1).strip()
        
        loc_match = re.search(r'^([^:：]+?)[:：]', text)
        if loc_match:
            location = loc_match.group(1).strip()
        
        return publisher, location
    
    @staticmethod
    def _extract_doi(text: str) -> str:
        match = re.search(r'doi[:\s]*(10\.[^\s]+)', text, re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    @staticmethod
    def _extract_url(text: str) -> str:
        match = re.search(r'https?://[^\s\]]+', text)
        return match.group(0) if match else ""


class ReferenceFormatter:
    @staticmethod
    def format_gb_t_7714(ref: Reference) -> str:
        authors_str = ReferenceFormatter._format_authors_gb(ref.authors)
        
        if ref.ref_type == 'journal':
            result = f"[{ref.number}] {authors_str}. {ref.title}[J]. {ref.source}"
            if ref.year:
                result += f", {ref.year}"
            if ref.volume:
                result += f", {ref.volume}"
            if ref.issue:
                result += f"({ref.issue})"
            if ref.pages:
                result += f": {ref.pages}"
            result += "."
        
        elif ref.ref_type == 'book':
            result = f"[{ref.number}] {authors_str}. {ref.title}[M]"
            if ref.location:
                result += f". {ref.location}"
            if ref.publisher:
                result += f": {ref.publisher}"
            if ref.year:
                result += f", {ref.year}"
            if ref.pages:
                result += f": {ref.pages}"
            result += "."
        
        elif ref.ref_type == 'thesis':
            result = f"[{ref.number}] {authors_str}. {ref.title}[D]"
            if ref.location:
                result += f". {ref.location}"
            if ref.source:
                result += f": {ref.source}"
            if ref.year:
                result += f", {ref.year}"
            result += "."
        
        elif ref.ref_type == 'online':
            result = f"[{ref.number}] {authors_str}. {ref.title}[EB/OL]"
            if ref.url:
                result += f". {ref.url}"
            if ref.year:
                result += f", {ref.year}"
            result += "."
        
        else:
            result = f"[{ref.number}] {authors_str}. {ref.title}[J]. {ref.source}, {ref.year}."
        
        return result
    
    @staticmethod
    def format_ieee(ref: Reference) -> str:
        authors_str = ReferenceFormatter._format_authors_ieee(ref.authors)
        
        if ref.ref_type == 'journal':
            result = f'[{ref.number}] {authors_str}, "{ref.title},"'
            result += f' {ref.source}'
            if ref.volume:
                result += f', vol. {ref.volume}'
            if ref.issue:
                result += f', no. {ref.issue}'
            if ref.pages:
                result += f', pp. {ref.pages}'
            if ref.year:
                result += f', {ref.year}'
            result += '.'
        
        elif ref.ref_type == 'book':
            result = f'[{ref.number}] {authors_str}, {ref.title}'
            if ref.location:
                result += f'. {ref.location}'
            if ref.publisher:
                result += f': {ref.publisher}'
            if ref.year:
                result += f', {ref.year}'
            result += '.'
        
        else:
            result = f'[{ref.number}] {authors_str}, "{ref.title}," {ref.source}, {ref.year}.'
        
        return result
    
    @staticmethod
    def format_apa(ref: Reference) -> str:
        authors_str = ReferenceFormatter._format_authors_apa(ref.authors)
        
        if ref.ref_type == 'journal':
            result = f"{authors_str} ({ref.year}). {ref.title}. {ref.source}"
            if ref.volume:
                result += f", {ref.volume}"
            if ref.issue:
                result += f"({ref.issue})"
            if ref.pages:
                result += f", {ref.pages}"
            result += "."
        
        elif ref.ref_type == 'book':
            result = f"{authors_str} ({ref.year}). {ref.title}"
            if ref.location:
                result += f". {ref.location}"
            if ref.publisher:
                result += f": {ref.publisher}"
            result += "."
        
        else:
            result = f"{authors_str} ({ref.year}). {ref.title}. {ref.source}."
        
        return result
    
    @staticmethod
    def format_mla(ref: Reference) -> str:
        if ref.authors:
            first_author = ref.authors[0]
            parts = first_author.split()
            if len(parts) >= 2:
                authors_str = f"{parts[-1]}, {' '.join(parts[:-1])}"
            else:
                authors_str = first_author
        else:
            authors_str = ""
        
        result = f'{authors_str}. "{ref.title}."'
        result += f' {ref.source}'
        if ref.volume:
            result += f', vol. {ref.volume}'
        if ref.issue:
            result += f', no. {ref.issue}'
        if ref.year:
            result += f', {ref.year}'
        if ref.pages:
            result += f', pp. {ref.pages}'
        result += '.'
        
        return result
    
    @staticmethod
    def format_springer(ref: Reference) -> str:
        authors_str = ReferenceFormatter._format_authors_ieee(ref.authors)
        
        result = f"{ref.number}. {authors_str}: {ref.title}."
        result += f" {ref.source}"
        if ref.volume:
            result += f" {ref.volume}"
        if ref.pages:
            result += f", {ref.pages}"
        if ref.year:
            result += f" ({ref.year})"
        result += "."
        
        return result
    
    @staticmethod
    def _format_authors_gb(authors: List[str]) -> str:
        if not authors:
            return ""
        
        if len(authors) <= 3:
            return ", ".join(authors)
        else:
            return f"{authors[0]}, 等"
    
    @staticmethod
    def _format_authors_ieee(authors: List[str]) -> str:
        if not authors:
            return ""
        
        formatted = []
        for author in authors:
            parts = author.split()
            if len(parts) >= 2:
                formatted.append(f"{parts[-1]} {' '.join(p[0] + '.' for p in parts[:-1])}")
            else:
                formatted.append(author)
        
        if len(formatted) <= 6:
            return ", ".join(formatted)
        else:
            return f"{formatted[0]}, et al."
    
    @staticmethod
    def _format_authors_apa(authors: List[str]) -> str:
        if not authors:
            return ""
        
        formatted = []
        for author in authors:
            parts = author.split()
            if len(parts) >= 2:
                initials = ". ".join(p[0] for p in parts[:-1]) + "."
                formatted.append(f"{parts[-1]}, {initials}")
            else:
                formatted.append(author)
        
        if len(formatted) == 1:
            return formatted[0]
        elif len(formatted) == 2:
            return f"{formatted[0]}, & {formatted[1]}"
        elif len(formatted) <= 7:
            return ", ".join(formatted[:-1]) + ", & " + formatted[-1]
        else:
            return ", ".join(formatted[:6]) + ", ... " + formatted[-1]
    
    @staticmethod
    def format_reference(ref: Reference, format_type: ReferenceFormat) -> str:
        formatters = {
            ReferenceFormat.GB_T_7714: ReferenceFormatter.format_gb_t_7714,
            ReferenceFormat.IEEE: ReferenceFormatter.format_ieee,
            ReferenceFormat.APA: ReferenceFormatter.format_apa,
            ReferenceFormat.MLA: ReferenceFormatter.format_mla,
            ReferenceFormat.SPRINGER: ReferenceFormatter.format_springer,
        }
        
        formatter = formatters.get(format_type, ReferenceFormatter.format_gb_t_7714)
        return formatter(ref)
    
    @staticmethod
    def format_all(references: List[Reference], format_type: ReferenceFormat) -> str:
        lines = []
        for ref in references:
            lines.append(ReferenceFormatter.format_reference(ref, format_type))
        return "\n".join(lines)


class ReferenceManager:
    def __init__(self):
        self.references: List[Reference] = []
        self.format_type = ReferenceFormat.GB_T_7714
    
    def parse_from_text(self, text: str):
        self.references = ReferenceParser.parse_multiple(text)
    
    def add_reference(self, ref: Reference):
        ref.number = len(self.references) + 1
        self.references.append(ref)
    
    def remove_reference(self, index: int):
        if 0 <= index < len(self.references):
            self.references.pop(index)
            self._renumber()
    
    def _renumber(self):
        for i, ref in enumerate(self.references, 1):
            ref.number = i
    
    def set_format(self, format_type: ReferenceFormat):
        self.format_type = format_type
    
    def get_formatted_output(self) -> str:
        return ReferenceFormatter.format_all(self.references, self.format_type)
    
    def get_reference_by_number(self, number: int) -> Optional[Reference]:
        for ref in self.references:
            if ref.number == number:
                return ref
        return None
    
    def validate_references(self) -> List[Dict[str, Any]]:
        issues = []
        
        for ref in self.references:
            if not ref.authors:
                issues.append({
                    'number': ref.number,
                    'field': 'authors',
                    'message': '缺少作者信息'
                })
            
            if not ref.title:
                issues.append({
                    'number': ref.number,
                    'field': 'title',
                    'message': '缺少标题'
                })
            
            if not ref.year:
                issues.append({
                    'number': ref.number,
                    'field': 'year',
                    'message': '缺少年份'
                })
            
            if ref.ref_type == 'journal' and not ref.source:
                issues.append({
                    'number': ref.number,
                    'field': 'source',
                    'message': '期刊论文缺少期刊名称'
                })
        
        return issues
    
    def export_to_bibtex(self) -> str:
        lines = []
        
        for ref in self.references:
            bib_type = {
                'journal': 'article',
                'book': 'book',
                'thesis': 'phdthesis',
                'conference': 'inproceedings',
            }.get(ref.ref_type, 'article')
            
            key = f"ref{ref.number}"
            
            lines.append(f"@{bib_type}{{{key},")
            
            if ref.authors:
                authors_str = " and ".join(ref.authors)
                lines.append(f"  author = {{{authors_str}}},")
            
            if ref.title:
                lines.append(f"  title = {{{ref.title}}},")
            
            if ref.source:
                field = 'journal' if ref.ref_type == 'journal' else 'publisher'
                lines.append(f"  {field} = {{{ref.source}}},")
            
            if ref.year:
                lines.append(f"  year = {{{ref.year}}},")
            
            if ref.volume:
                lines.append(f"  volume = {{{ref.volume}}},")
            
            if ref.issue:
                lines.append(f"  number = {{{ref.issue}}},")
            
            if ref.pages:
                lines.append(f"  pages = {{{ref.pages}}},")
            
            lines.append("}\n")
        
        return "\n".join(lines)
    
    def clear(self):
        self.references.clear()
    
    def count(self) -> int:
        return len(self.references)
