import requests
from bs4 import BeautifulSoup
import json

url = "https://www.jne.co.id/bantuan"

html = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
).text

soup = BeautifulSoup(
    html,
    "html.parser"
)

faq_data = []

for item in soup.select(".accordion"):

    question = item.select_one(".head")
    answer = item.select_one(".content")

    if question and answer:

        faq_data.append({
            "category": "jne",
            "question": question.get_text(strip=True),
            "answer": answer.get_text(" ", strip=True)
        })

with open(
    "data/common_info_dataset.json",
    "r",
    encoding="utf-8"
) as file:

    existing = json.load(file)

existing.extend(faq_data)

with open(
    "data/common_info_dataset.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        existing,
        file,
        ensure_ascii=False,
        indent=4
    )

print(f"{len(faq_data)} FAQ berhasil ditambahkan")