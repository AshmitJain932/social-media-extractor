import pandas as pd
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}


def normalize_url(url):

    if pd.isna(url):
        return None

    url = str(url).strip()

    if not url:
        return None

    if not url.startswith(
        ("http://", "https://")
    ):
        url = "https://" + url

    return url


def scrape_website(website):

    result = {
        "LinkedIn": "",
        "Facebook": "",
        "Instagram": "",
        "Amazon URL": "",
        "Amazon Found": "No"
    }

    try:

        response = requests.get(
            website,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            return result

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = set()

        for tag in soup.find_all(
            "a",
            href=True
        ):

            href = tag["href"]

            full_link = urljoin(
                website,
                href
            )

            links.add(full_link)

        for link in links:

            lower = link.lower()

            if (
                "linkedin.com" in lower
                and result["LinkedIn"] == ""
            ):
                result["LinkedIn"] = link

            elif (
                "facebook.com" in lower
                and result["Facebook"] == ""
            ):
                result["Facebook"] = link

            elif (
                "instagram.com" in lower
                and result["Instagram"] == ""
            ):
                result["Instagram"] = link

            elif (
                "amazon.com" in lower
                or "amazon.in" in lower
                or "amzn.to" in lower
            ):
                result["Amazon URL"] = link
                result["Amazon Found"] = "Yes"

        return result

    except:
        return result


def process_row(row):

    website = normalize_url(
        row["Website"]
    )

    if not website:

        return {
            "LinkedIn": "",
            "Facebook": "",
            "Instagram": "",
            "Amazon URL": "",
            "Amazon Found": "No"
        }

    return scrape_website(
        website
    )


def process_dataframe(df):

    df.columns = (
        df.columns
        .str.strip()
    )

    if "Website" not in df.columns:

        raise Exception(
            "Excel must contain a Website column"
        )

    rows = df.to_dict(
        "records"
    )

    with ThreadPoolExecutor(
        max_workers=30
    ) as executor:

        results = list(
            executor.map(
                process_row,
                rows
            )
        )

    result_df = pd.DataFrame(
        results
    )

    return pd.concat(
        [
            df.reset_index(
                drop=True
            ),
            result_df
        ],
        axis=1
    )