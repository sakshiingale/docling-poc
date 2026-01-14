#from docling.document_converter import DocumentConverter
#converter = DocumentConverter()
#result = converter.convert("Air (Prevention and Control of Pollution) Act, 1981-1-10.pdf")
#print(result.document.export_to_markdown())

from docling.document_converter import DocumentConverter
from pathlib import Path

# Convert PDF → Markdown
converter = DocumentConverter()
result = converter.convert(
    "Air (Prevention and Control of Pollution) Act, 1981-1-10.pdf"
)

full_markdown = result.document.export_to_markdown()

# Split markdown page-wise using Docling page separators
def split_markdown_by_page(markdown: str):
    separators = [
        "\n\n---\n\n",
        "\n---\n",
        "\n---\n\n",
    ]

    pages = [markdown]
    for sep in separators:
        if sep in markdown:
            pages = markdown.split(sep)
            break

    return [p.strip() for p in pages if p.strip()]

pages = split_markdown_by_page(full_markdown)

# Join pages with a CLEAR page-break marker
PAGE_BREAK = "\n\n==================== PAGE BREAK ====================\n\n"
final_markdown = PAGE_BREAK.join(pages)

# Save single markdown file
Path("output").mkdir(exist_ok=True)
Path("output/structured_pages.md").write_text(final_markdown, encoding="utf-8")

print(f"Pages detected: {len(pages)}")
