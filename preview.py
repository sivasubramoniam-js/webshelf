from bs4 import BeautifulSoup
import csv
import json
import requests
import random
import asyncio
import glob
import os

os.makedirs("previews", exist_ok=True)

agents = [
    # --- Desktop Chrome (Windows, macOS, Linux, Chrome OS) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    # --- Desktop Firefox (Windows, macOS, Linux) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.2; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",

    # --- Desktop Safari (macOS) ---
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",

    # --- Desktop Edge (Windows, macOS) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",

    # --- Desktop Opera (Windows, macOS) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0",

    # --- Mobile Chrome (Android, iOS) ---
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.89 Mobile/15E148 Safari/604.1",

    # --- Mobile Safari (iPhone, iPad) ---
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",

    # --- Original agents list (fixed trailing Macintosh comma bug) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
]

def get_link_preview(origin):
    url = "https://" + origin
    try:
        response = requests.get(url, headers={"user-agent": random.choice(agents)}, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        
        def get_meta(name):
            tag = soup.find("meta", property=name) or soup.find("meta", attrs={"name": name})
            return tag['content'] if tag and 'content' in tag.attrs else None

        print(get_meta("og:title"))
        preview = {
            "title": soup.title.string if soup.title else get_meta("og:title"),
            "description": get_meta("og:description") or get_meta("description"),
            "image": get_meta("og:image") if get_meta("og:image") else soup.find("link", rel="icon")["href"] if (soup.find("link", rel="icon") and "href" in soup.find("link", rel="icon").attrs) else "N/A",
            "url": get_meta("og:url") or url,
            "textContent": soup.get_text()
        }

        return {
            "link": url,
            "Heading": preview.get("title"),
            "Abstract": preview.get("description"),
            "Official Site": preview.get("url"),
            "Icon": preview.get("image"),
            "Redirect": preview.get("url"),
            "AbstractSource": "BS4",
            "AbstractURL": preview.get("url"),
        }
    except Exception as e:
        return 

# Example: Get details for DuckDuckGo
# read file.csv and get the official site for each domain
# write the output to output.json
async def main():
    # read csv files from sites folder
    files = glob.glob("sites/*.csv")
    
    results = []
    for file in files:
        filename = file.split("/")[-1]
        with open(file, "r") as f:
            reader = list(csv.reader(f))
            for i in range(0, len(reader), 50):
                batch = [row for row in reader[i:i+50] if len(row) > 1]
                print(f"Processing batch {i//50 + 1} of {(len(reader) + 49) // 50}...")
        
                tasks = [asyncio.to_thread(get_link_preview, row[1]) for row in batch]
                batch_results = await asyncio.gather(*tasks)
                results.extend([res for res in batch_results if res is not None])
                await asyncio.sleep(2)
                json_output_name = f"previews/{filename.replace('.csv', f'_{i//50 + 1:03d}.json')}"
                with open(json_output_name, "w") as f:
                    json.dump(results, f, indent=4)
                results = []

if __name__ == "__main__":
    asyncio.run(main())
