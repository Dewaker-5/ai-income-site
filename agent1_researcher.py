from groq import Groq
import json
import os

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def research_keywords(topic):
    prompt = f"""
    Give me 10 low competition high search volume keywords related to: {topic}
    
    Return ONLY a JSON array like this:
    ["keyword 1", "keyword 2", "keyword 3"]
    
    Nothing else. Just the JSON array.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    keywords = json.loads(response.choices[0].message.content)
    
    with open("keywords.json", "w") as f:
        json.dump(keywords, f, indent=2)
    
    print("Keywords saved to keywords.json")
    print(keywords)

research_keywords("AI productivity tools")
