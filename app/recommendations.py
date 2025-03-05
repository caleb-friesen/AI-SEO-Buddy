from typing import Dict, List

def generate_recommendations(analysis: Dict, lighthouse: Dict) -> Dict[str, List[str]]:
    """
    Generates SEO recommendations based on content analysis and Lighthouse results.
    
    Args:
        analysis (Dict): Content analysis results
        lighthouse (Dict): Lighthouse audit results
        
    Returns:
        Dict: Dictionary containing categorized recommendations
    """
    recommendations = {
        "critical": [],
        "important": [],
        "minor": []
    }
    
    # Title recommendations
    if not analysis["title"]["has_title"]:
        recommendations["critical"].append("Add a title tag to your page")
    elif not analysis["title"]["optimal_length"]:
        recommendations["important"].append(
            "Adjust title length to be between 50-60 characters for optimal display in search results"
        )
    
    # Meta description recommendations
    if not analysis["meta_description"]["has_meta"]:
        recommendations["critical"].append("Add a meta description to your page")
    elif not analysis["meta_description"]["optimal_length"]:
        recommendations["important"].append(
            "Adjust meta description length to be between 150-160 characters for optimal display"
        )
    
    # Heading structure recommendations
    if not analysis["headings"]["has_proper_structure"]:
        if analysis["headings"]["h1_count"] == 0:
            recommendations["critical"].append("Add an H1 heading to your page")
        elif analysis["headings"]["h1_count"] > 1:
            recommendations["important"].append("Use only one H1 heading per page")
    
    # Content recommendations
    if not analysis["content"]["has_sufficient_content"]:
        recommendations["important"].append(
            "Add more content to your page (aim for at least 300 words)"
        )
    
    # Keyword recommendations
    if "keywords" in analysis:
        for keyword, data in analysis["keywords"].items():
            if not data["in_title"] and not data["in_meta"] and not data["in_headings"]:
                recommendations["important"].append(
                    f"Include the keyword '{keyword}' in your title, meta description, or headings"
                )
            if data["density"] < 0.5:
                recommendations["minor"].append(
                    f"Consider increasing the usage of keyword '{keyword}' (current density: {data['density']}%)"
                )
            elif data["density"] > 3:
                recommendations["important"].append(
                    f"Reduce the usage of keyword '{keyword}' to avoid keyword stuffing (current density: {data['density']}%)"
                )
    
    # Image recommendations
    if analysis["images"]["missing_alt_count"] > 0:
        recommendations["important"].append(
            f"Add alt text to {analysis['images']['missing_alt_count']} images"
        )
    
    # Link recommendations
    if analysis["links"]["internal_count"] == 0:
        recommendations["minor"].append("Add internal links to improve site navigation")
    if analysis["links"]["external_count"] == 0:
        recommendations["minor"].append("Consider adding relevant external links")
    
    # Lighthouse performance recommendations
    if lighthouse["performance"] < 90:
        recommendations["critical"].append(
            "Improve page performance (current score: {:.0f}/100)".format(lighthouse["performance"])
        )
    elif lighthouse["performance"] < 95:
        recommendations["important"].append(
            "Consider optimizing page performance (current score: {:.0f}/100)".format(lighthouse["performance"])
        )
    
    # Lighthouse SEO recommendations
    if lighthouse["seo"] < 90:
        recommendations["important"].append(
            "Address technical SEO issues (current score: {:.0f}/100)".format(lighthouse["seo"])
        )
    
    # Lighthouse accessibility recommendations
    if lighthouse["accessibility"] < 90:
        recommendations["important"].append(
            "Improve accessibility (current score: {:.0f}/100)".format(lighthouse["accessibility"])
        )
    
    return recommendations 