import openai
from config import OPENAI_API_KEY
from utils import load_json

openai.api_key = OPENAI_API_KEY

def summarize_profile(data):
    full_text = f"""
    Name: {data['name']}
    Headline: {data['headline']}
    About: {data['about']}
    Experience: {' | '.join(data['experience'])}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're an HR assistant summarizing LinkedIn profiles."},
            {"role": "user", "content": f"Summarize this profile:\n{full_text}"}
        ],
        temperature=0.6
    )
    return response.choices[0].message['content']

if __name__ == "__main__":
    profile_data = load_json("profiles/raw_profile.json")
    summary = summarize_profile(profile_data)
    print("\n🧠 Summary:\n", summary)
