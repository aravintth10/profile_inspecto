import os
import openai
import requests
from dotenv import load_dotenv
from config import OPENAI_API_KEY, SERPAPI_KEY

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def web_search(name, company):
    query = f"{name} {company} site:linkedin.com OR site:twitter.com OR site:github.com OR site:medium.com"
    url = f"https://serpapi.com/search.json?q={query}&api_key={SERPAPI_KEY}&num=10"

    resp = requests.get(url)
    results = resp.json().get("organic_results", [])
    snippets = []

    for r in results:
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        link = r.get("link", "")
        snippets.append(f"{title} - {snippet} ({link})")

    return "\n".join(snippets)

def summarize_profile_from_web(name, company):
    print("🔍 Searching the web...")
    raw_data = web_search(name, company)

    if not raw_data.strip():
        return "No relevant public information found."

    print("🧠 Summarizing...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are an HR analyst summarizing a person's public web presence."},
            {"role": "user", "content": f"Summarize this person’s background based on the following info:\n{raw_data}"}
        ],
        temperature=0.5
    )
    return response.choices[0].message["content"]

# Example usage
if __name__ == "__main__":
    name = input("Full Name: ").strip()
    company = input("Company: ").strip()
    summary = summarize_profile_from_web(name, company)
    print("\n📄 Summary:\n", summary)
