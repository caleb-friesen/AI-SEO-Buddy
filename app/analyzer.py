from typing import Dict, List, Optional
from collections import Counter
import re

def analyze_content(content: Dict, keywords: Optional[List[str]] = None) -> Dict:
    """
    Analyzes the scraped content for SEO metrics.
    
    Args:
        content (Dict): Scraped content dictionary
        keywords (List[str], optional): List of target keywords to analyze
        
    Returns:
        Dict: Dictionary containing analysis results
    """
    analysis = {}
    
    # Title analysis
    title = content["title"]
    analysis["title"] = {
        "length": len(title),
        "has_title": bool(title),
        "optimal_length": 50 <= len(title) <= 60 if title else False
    }
    
    # Meta description analysis
    meta_desc = content["meta_description"]
    analysis["meta_description"] = {
        "length": len(meta_desc),
        "has_meta": bool(meta_desc),
        "optimal_length": 150 <= len(meta_desc) <= 160 if meta_desc else False
    }
    
    # Headings analysis
    analysis["headings"] = {
        "h1_count": len(content["headings"]["h1"]),
        "h2_count": len(content["headings"]["h2"]),
        "h3_count": len(content["headings"]["h3"]),
        "has_proper_structure": len(content["headings"]["h1"]) == 1
    }
    
    # Content analysis
    text = content["content"]
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    
    analysis["content"] = {
        "word_count": word_count,
        "has_sufficient_content": word_count >= 300
    }
    
    # Keyword analysis if keywords provided
    if keywords:
        keyword_analysis = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Count exact matches
            exact_matches = text.lower().count(keyword_lower)
            # Calculate keyword density
            density = (exact_matches / word_count * 100) if word_count > 0 else 0
            
            keyword_analysis[keyword] = {
                "count": exact_matches,
                "density": round(density, 2),
                "in_title": keyword_lower in title.lower(),
                "in_meta": keyword_lower in meta_desc.lower(),
                "in_headings": any(
                    keyword_lower in h.lower() 
                    for h_list in content["headings"].values() 
                    for h in h_list
                )
            }
        analysis["keywords"] = keyword_analysis
    
    # Link analysis
    internal_links = [link for link in content["links"] if link["href"].startswith(("/", content["url"]))]
    external_links = [link for link in content["links"] if link["href"].startswith(("http", "https"))]
    
    analysis["links"] = {
        "internal_count": len(internal_links),
        "external_count": len(external_links),
        "total_count": len(content["links"])
    }
    
    # Image analysis
    images_without_alt = [img for img in content["images"] if not img["alt"]]
    
    analysis["images"] = {
        "total_count": len(content["images"]),
        "missing_alt_count": len(images_without_alt)
    }
    
    return analysis 