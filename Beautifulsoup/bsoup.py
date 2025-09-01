import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import time
import hashlib
import json

# Initialize sets and lists
visited_urls = set()
all_text = []
all_links = set()
all_metadata = []

# Base domain to restrict the crawler
base_domain = "https://www.infomagnus.com"

# Output folders
os.makedirs("scraped_data", exist_ok=True)
os.makedirs("scraped_data/images", exist_ok=True)

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) and base_domain in url

def save_text():
    with open("scraped_data/text.txt", "w", encoding="utf-8") as f:
        for line in all_text:
            f.write(line + "\n")

def save_links():
    with open("scraped_data/links.txt", "w", encoding="utf-8") as f:
        for link in all_links:
            f.write(link + "\n")

def save_metadata():
    with open("scraped_data/metadata.txt", "w", encoding="utf-8") as f:
        for meta in all_metadata:
            f.write(str(meta) + "\n")

def download_image(img_url):
    try:
        if not img_url:
            return
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(img_url, headers=headers, timeout=5)
        if response.status_code == 200:
            ext = os.path.splitext(urlparse(img_url).path)[-1].split('?')[0]
            if not ext or len(ext) > 5:
                ext = ".jpg"  # Default extension
            filename_hash = hashlib.md5(img_url.encode()).hexdigest()
            filename = f"{filename_hash}{ext}"
            filepath = os.path.join("scraped_data/images", filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"Downloaded image: {img_url} -> {filepath}")
        else:
            print(f"Failed to download image (status {response.status_code}): {img_url}")
    except Exception as e:
        print(f"Failed to download image {img_url}: {e}")

def extract_data_from_page(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract visible text
        texts = soup.stripped_strings
        page_text = "\n".join(texts)
        all_text.append(f"--- TEXT FROM: {url} ---\n{page_text}\n")

        # Extract metadata
        meta_tags = soup.find_all("meta")
        meta_info = {"url": url, "metadata": [meta.attrs for meta in meta_tags]}
        all_metadata.append(meta_info)

        # Extract and queue all links
        for link_tag in soup.find_all("a", href=True):
            full_url = urljoin(url, link_tag['href'])
            if is_valid_url(full_url) and full_url not in visited_urls:
                all_links.add(full_url)
                crawl_website(full_url)

        # Extract and download images
        for img_tag in soup.find_all("img", src=True):
            img_src = img_tag.get('src') or img_tag.get('data-src')
            if img_src:
                img_url = urljoin(url, img_src)
                download_image(img_url)

    except Exception as e:
        print(f"Error scraping {url}: {e}")

def crawl_website(url):
    if url not in visited_urls:
        visited_urls.add(url)
        print(f"Scraping: {url}")
        extract_data_from_page(url)
        time.sleep(1)  # Be polite to server

# Start crawling
crawl_website(base_domain)

# Save results
save_text()
save_links()
save_metadata()

# Collect all data per page
pages_data = []

for i, meta in enumerate(all_metadata):
    page_entry = {
        "url": meta["url"],
        "metadata": meta["metadata"],
        "text": "",      # Will fill below
        "links": [],     # Will fill below
        "images": []     # Will fill below
    }
    # Get text for this page
    for text in all_text:
        if text.startswith(f"--- TEXT FROM: {meta['url']} ---"):
            page_entry["text"] = text
            break
    # Get links for this page
    page_links = []
    for link in all_links:
        if link.startswith(meta["url"]):
            page_links.append(link)
    page_entry["links"] = page_links
    # Get images for this page (by filename hash)
    # If you want to store image URLs, you can collect them during download_image
    # For now, we leave images as empty or you can enhance this part
    pages_data.append(page_entry)

# Save to JSON file
with open("scraped_data/website_data.json", "w", encoding="utf-8") as f:
    json.dump(pages_data, f, ensure_ascii=False, indent=2)

print("✅ Data exported to scraped_data/website_data.json") 