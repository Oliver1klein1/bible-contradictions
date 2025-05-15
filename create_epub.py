import os
import zipfile

# Paths
EPUB_NAME = 'bible-contradictions.epub'
EPUB_DIR = 'epub'
MIMETYPE_PATH = os.path.join(EPUB_DIR, 'mimetype')
META_INF_DIR = os.path.join(EPUB_DIR, 'META-INF')
OEBPS_DIR = os.path.join(EPUB_DIR, 'OEBPS')

# Remove old EPUB if exists
if os.path.exists(EPUB_NAME):
    os.remove(EPUB_NAME)

with zipfile.ZipFile(EPUB_NAME, 'w') as epub:
    # 1. Add mimetype file first, uncompressed
    epub.write(MIMETYPE_PATH, 'mimetype', compress_type=zipfile.ZIP_STORED)

    # 2. Add META-INF files (compressed)
    for root, _, files in os.walk(META_INF_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, EPUB_DIR)
            epub.write(full_path, rel_path, compress_type=zipfile.ZIP_DEFLATED)

    # 3. Add OEBPS files (compressed)
    for root, _, files in os.walk(OEBPS_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, EPUB_DIR)
            epub.write(full_path, rel_path, compress_type=zipfile.ZIP_DEFLATED)

print(f"EPUB file '{EPUB_NAME}' created successfully.") 