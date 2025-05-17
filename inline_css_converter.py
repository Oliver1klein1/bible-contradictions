import re
from bs4 import BeautifulSoup

# File paths
INPUT_FILE = 'index.html'
OUTPUT_FILE = 'index_inlined.html'

# Inline style for content images
IMAGE_INLINE_STYLE = (
    'width: 50%; max-width: 100%; display: block; margin: 1.5em auto; '
    'box-shadow: 0 6px 24px rgba(44,50,80,0.13), 0 1.5px 6px rgba(44,50,80,0.08); '
    'border-radius: 10px; background: #fff; height: auto;'
)

# Inline style for cover image
COVER_IMAGE_STYLE = (
    'display: block; margin: 0 auto 1.5em auto; width: 100%; max-width: 400px; height: auto; '
    'border-radius: 10px; box-shadow: 0 6px 24px rgba(44,50,80,0.13), 0 1.5px 6px rgba(44,50,80,0.08); background: #fff;'
)

# Inline style for tables
TABLE_STYLE = (
    'width: 100%; border-collapse: collapse; margin: 1.5em 0; font-size: 1.05em; background-color: #fff;'
    'border-radius: 8px; overflow: hidden;'
)
TH_STYLE = (
    'background-color: #4a4e69; color: #fff; text-align: left; padding: 0.75em 1em;'
    'border-bottom: 1px solid #e0e0e0;'
)
TD_STYLE = (
    'padding: 0.75em 1em; border-bottom: 1px solid #e0e0e0;'
)
TR_EVEN_STYLE = 'background-color: #f9f6f2;'
CAPTION_STYLE = 'caption-side: top; font-weight: bold; font-size: 1.15em; color: #4a4e69; margin-bottom: 0.5em; letter-spacing: 0.5px;'

# Inline style for TOC
TOC_SECTION_STYLE = 'margin: 3em auto; max-width: 700px; background: #f8f8fa; border-radius: 10px; box-shadow: 0 2px 12px #4a4e691a; padding: 2em;'
TOC_H2_STYLE = 'text-align: center; font-size: 2em; color: #4a4e69; margin-bottom: 1em;'
TOC_H3_STYLE = 'text-align: center; font-size: 1.3em; color: #9a8c98; margin-bottom: 0.7em;'
TOC_UL_STYLE = 'list-style-type: none; padding-left: 0;'
TOC_LI_STYLE = 'margin-bottom: 0.5em;'
TOC_A_STYLE = 'color: #4a4e69; text-decoration: none; font-weight: normal; font-size: 1.05em; padding: 0.2em 0; display: inline-block;'

# Inline style for main container (soft cream background, Georgia font, larger size)
CONTAINER_STYLE = (
    'max-width: 900px; margin: 0 auto; padding: 2em; background: #fcfbf7; '
    'box-shadow: 0 0 20px #0001; border-radius: 18px; font-family: Georgia, \'Times New Roman\', Times, serif; font-size: 1.15em;'
)

# Inline style for title/cover section
COVER_STYLE = (
    'text-align: center; margin-bottom: 3rem; padding: 3rem 0 2rem 0; background: #f8f8fa; border-radius: 16px;'
)
COVER_H1_STYLE = 'font-size: 2.5rem; margin: 1rem 0; font-weight: bold; letter-spacing: 0.08em;'
COVER_H2_STYLE = 'font-size: 1.8rem; margin: 0.8rem 0; font-weight: bold;'
COVER_H3_STYLE = 'font-size: 1.4rem; margin: 1.5rem 0 0.5rem; font-style: italic;'
COVER_P_STYLE = 'margin-bottom: 1.2rem; font-size: 1.1em;'

# Inline style for copyright section
COPYRIGHT_STYLE = 'text-align: center; font-size: 1em; color: #9a8c98; margin: 1.5em 0 0.5em 0; font-style: italic;'

# Contradiction heading style
CONTRADICTION_H3_STYLE = 'color: #2a4e9a; font-size: 1.5em; font-weight: bold; letter-spacing: 0.02em; margin-top: 2em;'
# Introduction heading style
INTRO_H2_STYLE = 'color: #2a4e9a; font-size: 1.5em; font-weight: bold; letter-spacing: 0.02em; margin-top: 2em;'

# Inline style for navigation button
NAV_BTN_STYLE = (
    'display: inline-block; background: linear-gradient(90deg, #4e54c8 0%, #8f94fb 100%); color: #fff; '
    'font-size: 1.1em; font-weight: bold; padding: 0.7em 2.2em; border-radius: 2em; '
    'box-shadow: 0 4px 16px rgba(78,84,200,0.15); text-decoration: none; margin: 2em auto 0 auto; '
    'letter-spacing: 0.04em; text-align: center;'
)
NAV_BTN_WRAPPER_STYLE = 'width: 100%; display: flex; justify-content: center;'

# Justified paragraph style for contradiction, key, and introduction
JUSTIFY_P_STYLE = 'text-align: justify; text-justify: inter-word;'

# Insert media-specific CSS for page breaks
MEDIA_CSS = '''<style>
@media print {
  .cover {
    page-break-after: always;
    break-after: page;
  }
  .copyright,
  #table-of-contents,
  #introduction,
  #part-one,
  #part-two,
  #conclusion,
  .key,
  article {
    page-break-before: always;
    break-before: page;
  }
  .cover:first-of-type,
  .copyright:first-of-type,
  #table-of-contents:first-of-type,
  #introduction:first-of-type,
  #part-one:first-of-type,
  #part-two:first-of-type,
  #conclusion:first-of-type,
  .key:first-of-type,
  article:first-of-type {
    page-break-before: auto;
    break-before: auto;
  }
  .nav-btn-wrapper,
  .toc-nav-btn-wrapper {
    display: none !important;
  }
  footer a[href="#top"] {
    display: none !important;
  }
}
@media screen {
  .cover,
  .copyright,
  #table-of-contents,
  #introduction,
  #part-one,
  #part-two,
  #conclusion,
  .key,
  article {
    page-break-before: auto;
    break-before: auto;
  }
}
@page {
  @bottom-center {
    content: counter(page);
    font-size: 12pt;
    font-family: Georgia, 'Times New Roman', Times, serif;
  }
}
</style>'''

# Read the HTML
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Remove <link rel="stylesheet"> and <style> blocks
for tag in soup.find_all(['link', 'style']):
    if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
        tag.decompose()
    elif tag.name == 'style':
        tag.decompose()

# Inline styles for images
for img in soup.find_all('img'):
    # Check if this is the cover image (inside .cover div)
    is_cover_img = img.find_parent('div', class_='cover') is not None
    is_content_img = 'content-image' in (img.get('class') or [])
    is_article_img = img.find_parent('article') is not None
    if is_cover_img:
        img['style'] = COVER_IMAGE_STYLE
        if 'class' in img.attrs:
            del img['class']
    elif is_content_img or is_article_img:
        img['style'] = IMAGE_INLINE_STYLE
        if 'class' in img.attrs:
            del img['class']

# Inline styles for tables
for table in soup.find_all('table'):
    table['style'] = TABLE_STYLE
    if 'class' in table.attrs:
        del table['class']
    caption = table.find('caption')
    if caption:
        caption['style'] = CAPTION_STYLE
    for th in table.find_all('th'):
        th['style'] = TH_STYLE
    for td in table.find_all('td'):
        td['style'] = TD_STYLE
    for i, tr in enumerate(table.find_all('tr')):
        if i % 2 == 1:
            tr['style'] = TR_EVEN_STYLE

# Inline styles for Table of Contents
# Find the TOC section by id
toc_section = soup.find(id='table-of-contents')
if toc_section:
    toc_section['style'] = TOC_SECTION_STYLE
    h2 = toc_section.find('h2')
    if h2:
        h2['style'] = TOC_H2_STYLE
    for h3 in toc_section.find_all('h3'):
        h3['style'] = TOC_H3_STYLE
    for ul in toc_section.find_all('ul'):
        ul['style'] = TOC_UL_STYLE
    for li in toc_section.find_all('li'):
        li['style'] = TOC_LI_STYLE
    for a in toc_section.find_all('a'):
        a['style'] = TOC_A_STYLE

# Inline style for main container
def style_container():
    container_div = soup.find('div', class_='container')
    if container_div:
        container_div['style'] = CONTAINER_STYLE
        if 'class' in container_div.attrs:
            del container_div['class']
style_container()

# Inline styles for cover/title page
cover_div = soup.find('div', class_='cover')
if cover_div:
    cover_div['style'] = COVER_STYLE
    for h1 in cover_div.find_all('h1'):
        h1['style'] = COVER_H1_STYLE
    for h2 in cover_div.find_all('h2'):
        h2['style'] = COVER_H2_STYLE
    for h3 in cover_div.find_all('h3'):
        h3['style'] = COVER_H3_STYLE
    for p in cover_div.find_all('p'):
        p['style'] = COVER_P_STYLE

# Inline styles for copyright page/section
for copyright_p in soup.find_all('p', class_='copyright'):
    copyright_p['style'] = COPYRIGHT_STYLE
    if 'class' in copyright_p.attrs:
        del copyright_p['class']

# Prominent contradiction headings
for article in soup.find_all('article', class_='contradiction'):
    h3 = article.find('h3')
    if h3:
        h3['style'] = CONTRADICTION_H3_STYLE
        if 'class' in h3.attrs:
            del h3['class']
    if 'class' in article.attrs:
        del article['class']

# Prominent introduction heading
intro_section = soup.find(id='introduction')
if intro_section:
    h2 = intro_section.find('h2')
    if h2:
        h2['style'] = INTRO_H2_STYLE

# Stylish navigation button for Back to Table of Contents
for article in soup.find_all('article'):
    # Find a link to #table-of-contents at the end of the article
    links = article.find_all('a', href='#table-of-contents')
    for a in links:
        # Check if the link text contains 'Back to Table of Contents'
        if 'back to table of contents' in a.get_text(strip=True).lower():
            a['style'] = NAV_BTN_STYLE
            if 'class' in a.attrs:
                del a['class']
            # Wrap in a centered div
            wrapper = soup.new_tag('div')
            wrapper['style'] = NAV_BTN_WRAPPER_STYLE
            a.insert_before(wrapper)
            wrapper.append(a.extract())

# Add class='contradiction' to all contradiction articles
for article in soup.find_all('article'):
    article_id = article.get('id', '')
    if article_id.startswith('contradiction'):
        article['class'] = (article.get('class', []) + ['contradiction'])

# Justify paragraphs in contradiction and key articles
for article in soup.find_all('article'):
    article_class = article.get('class') or []
    if 'contradiction' in article_class or 'key' in article_class:
        for p in article.find_all('p'):
            # Remove any previous text-align
            style = p.get('style', '')
            style = re.sub(r'text-align\s*:\s*[^;]+;?', '', style)
            style = re.sub(r'text-justify\s*:\s*[^;]+;?', '', style)
            p['style'] = (style + ' ' + JUSTIFY_P_STYLE).strip()

# Justify paragraphs in the introduction section
intro_section = soup.find(id='introduction')
if intro_section:
    for p in intro_section.find_all('p'):
        style = p.get('style', '')
        style = re.sub(r'text-align\s*:\s*[^;]+;?', '', style)
        style = re.sub(r'text-justify\s*:\s*[^;]+;?', '', style)
        p['style'] = (style + ' ' + JUSTIFY_P_STYLE).strip()

# After parsing HTML, insert the style block in <head>
head = soup.find('head')
if head:
    head.append(BeautifulSoup(MEDIA_CSS, 'html.parser'))

# Write the output
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print(f"Inlined CSS for images, tables, TOC, main container, title, copyright, prominent headings, and navigation buttons. Output: {OUTPUT_FILE}") 