import re
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    p1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(p1, 'md_files/entries')

    _, filenames = default_storage.listdir(p)
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    p1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(p1, 'md_files/entries')

    filename = os.path.join(p, f"{title}.md")
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    p1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(p1, 'md_files/entries')
    try:
        f = default_storage.open(os.path.join(p, f"{title}.md"))
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def get_error(title):
    p1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(p1, 'md_files/error_pages')
    try:
        f = default_storage.open(os.path.join(p, f"{title}.md"))
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
