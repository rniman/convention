"""Preserve local source links without publishing reference files."""
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def on_page_markdown(markdown, *, page, config, files):
    reference_root = (Path(config.docs_dir).parent / "ref").resolve()
    source_dir = Path(page.file.abs_src_path).parent

    def replace_reference(match):
        label, target = match.groups()
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            return match.group(0)
        resolved = (source_dir / unquote(parsed.path)).resolve()
        if resolved.is_relative_to(reference_root):
            return f"{label}（로컬 참고 자료）"
        return match.group(0)

    return re.sub(r"\[([^\]\n]+)\]\(([^\s)]+)\)", replace_reference, markdown)
