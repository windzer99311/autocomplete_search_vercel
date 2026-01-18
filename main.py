import requests
import json
import re
from fastapi import FastAPI
app = FastAPI()
@app.get("/autocomplete/search")
def parse_google_ac(q: str):
    url = "https://suggestqueries-clients6.youtube.com/complete/search"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.youtube.com",
        "referer": "https://www.youtube.com/",
        "user-agent": (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/143.0.0.0 Mobile Safari/537.36"
        )
    }
    params = {
        "ds": "yt",
        "hl": "en",
        "gl": "in",
        "client": "youtube",
        "gs_ri": "youtube",
        "tok": "iNaG2NDGF_Ti2dPRguRNIQ",
        "h": "180",
        "w": "320",
        "ytvs": "1",
        "gs_id": "2",
        "q": f"{q}",
        "cp": f"{len(q)}",
    }

    response = requests.get(url, params=params, headers=headers)

    # 1️⃣ Extract JSON-like payload inside the function call
    match = re.search(r'window\.google\.ac\.h\((.*)\)\s*$', response.text)
    if not match:
        raise ValueError("Invalid Google AC response format")

    payload = match.group(1)

    # 2️⃣ Parse JSON safely
    data = json.loads(payload)

    raw_suggestions = data[1]

    # 4️⃣ Normalize suggestions
    suggestions = []
    for item in raw_suggestions:
        suggestions.append({"text": item[0]})

    return {
        "suggestions": suggestions
    }


