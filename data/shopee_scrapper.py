from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import json
import re
import time

CATEGORY_URL = input(
    "Masukkan URL kategori Shopee: "
).strip()

CATEGORY_NAME = input(
    "Masukkan nama kategori: "
).strip()

MAX_PAGE = int(
    input(
        "Masukkan jumlah halaman: "
    )
)

driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager().install()
    )
)

all_faq = []

for page in range(1, MAX_PAGE + 1):

    if "?" in CATEGORY_URL:
        url = f"{CATEGORY_URL}&page={page}"
    else:
        url = f"{CATEGORY_URL}?page={page}"

    print(f"\nMengambil halaman {page}")

    try:

        driver.get(url)

        time.sleep(3)

        soup = BeautifulSoup(
            driver.page_source,
            "html.parser"
        )

        faq_script = soup.find(
            "script",
            {"id": "faqSchema"}
        )

        if not faq_script:

            print(
                f"faqSchema tidak ditemukan di halaman {page}"
            )
            break

        faq_json = json.loads(
            faq_script.string
        )

        page_count = 0

        for item in faq_json.get(
            "mainEntity",
            []
        ):

            question = item.get(
                "name",
                ""
            ).strip()

            answer = (
                item.get(
                    "acceptedAnswer",
                    {}
                ).get(
                    "text",
                    ""
                )
            )

            answer = re.sub(
                r"<[^>]+>",
                " ",
                answer
            )

            answer = re.sub(
                r"\s+",
                " ",
                answer
            ).strip()

            if question and answer:

                all_faq.append({
                    "category": CATEGORY_NAME,
                    "question": question,
                    "answer": answer
                })

                page_count += 1

        print(
            f"{page_count} FAQ ditemukan"
        )

    except Exception as e:

        print(
            f"Error halaman {page}"
        )

        print(e)

driver.quit()

print(
    f"\nTotal FAQ ditemukan: {len(all_faq)}"
)

try:

    with open(
        "data/common_info_dataset.json",
        "r",
        encoding="utf-8"
    ) as file:

        existing_data = json.load(
            file
        )

except:

    existing_data = []

existing_questions = {
    item.get(
        "question",
        ""
    )
    for item in existing_data
}

new_data = []

for faq in all_faq:

    if faq["question"] not in existing_questions:

        new_data.append(
            faq
        )

existing_data.extend(
    new_data
)

with open(
    "data/common_info_dataset.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        existing_data,
        file,
        ensure_ascii=False,
        indent=4
    )

print(
    f"FAQ baru ditambahkan: {len(new_data)}"
)