import json
import csv
import io
import re
import zipfile
from db.models import Snippet

def clean_filename(name: str) -> str:
    """Cleans a string to make it safe for filenames."""
    if not name:
        return "untitled"
    # Keep only alphanumeric, space, hyphens, underscores
    cleaned = re.sub(r'[^\w\s-]', '', name).strip()
    cleaned = re.sub(r'\s+', '_', cleaned)
    return cleaned or "untitled"

def export_to_json(snippets: list[Snippet]) -> str:
    """Serializes snippets to a pretty-printed JSON string."""
    data = []
    for s in snippets:
        data.append({
            "id": s.id,
            "title": s.title,
            "content": s.content,
            "description": s.description,
            "tags": s.tags,
            "type": s.type,
            "language": s.language,
            "category": s.category,
            "created_at": s.created_at,
            "updated_at": s.updated_at
        })
    return json.dumps(data, indent=4)

def export_to_csv(snippets: list[Snippet]) -> str:
    """Serializes snippets to a CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    # Write header
    writer.writerow([
        "id", "title", "type", "language", "category", "tags", "description", "content", "created_at", "updated_at"
    ])
    for s in snippets:
        writer.writerow([
            s.id,
            s.title,
            s.type,
            s.language,
            s.category,
            s.tags_csv,
            s.description,
            s.content,
            s.created_at,
            s.updated_at
        ])
    return output.getvalue()

def export_to_markdown(snippets: list[Snippet]) -> str:
    """Compiles all snippets into a single, clean Markdown document."""
    md = ["# Snippet Vault Export\n"]
    
    # Group by category
    by_category = {}
    for s in snippets:
        cat = s.category or "Uncategorized"
        by_category.setdefault(cat, []).append(s)
    
    for category, snips in sorted(by_category.items()):
        md.append(f"## Category: {category}\n")
        for s in snips:
            md.append(f"### {s.title}")
            if s.description:
                md.append(f"*{s.description}*\n")
            
            meta_parts = []
            meta_parts.append(f"**Type:** {s.type}")
            if s.language:
                meta_parts.append(f"**Language:** `{s.language}`")
            if s.tags:
                tags_list = ", ".join([f"`{t}`" for t in s.tags])
                meta_parts.append(f"**Tags:** {tags_list}")
            
            md.append(" | ".join(meta_parts) + "\n")
            
            time_parts = [f"**Created:** {s.created_at}"]
            if s.updated_at and s.updated_at != s.created_at:
                time_parts.append(f"**Updated:** {s.updated_at}")
            md.append(" | ".join(time_parts) + "\n")
            
            # Code block
            lang = s.language.lower() if s.language else ""
            md.append(f"```{lang}\n{s.content}\n```\n")
            md.append("---")
        md.append("")
    
    return "\n".join(md)

def export_to_zip(snippets: list[Snippet]) -> bytes:
    """Creates a ZIP archive containing individual Markdown files for each snippet, organized by category."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        seen_paths = set()
        for s in snippets:
            cat_dir = clean_filename(s.category or "Uncategorized")
            base_name = clean_filename(s.title or "Snippet")
            
            filename = f"{base_name}.md"
            path = f"{cat_dir}/{filename}"
            counter = 1
            while path.lower() in seen_paths:
                filename = f"{base_name}_{counter}.md"
                path = f"{cat_dir}/{filename}"
                counter += 1
            seen_paths.add(path.lower())
            
            # Construct markdown content for this individual snippet
            md_content = []
            md_content.append("---")
            md_content.append(f"title: {s.title}")
            if s.description:
                # Escape any quotes if needed, but simple display is fine
                md_content.append(f"description: {s.description}")
            md_content.append(f"type: {s.type}")
            md_content.append(f"language: {s.language or ''}")
            md_content.append(f"category: {s.category or 'Uncategorized'}")
            if s.tags:
                md_content.append(f"tags: {s.tags}")
            md_content.append(f"created_at: {s.created_at}")
            md_content.append(f"updated_at: {s.updated_at}")
            md_content.append("---\n")
            
            if s.description:
                md_content.append(f"{s.description}\n")
                
            lang = s.language.lower() if s.language else ""
            md_content.append(f"```{lang}\n{s.content}\n```")
            
            zip_file.writestr(path, "\n".join(md_content))
            
    return zip_buffer.getvalue()
