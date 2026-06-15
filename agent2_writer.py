from groq import Groq
import json
import os
import re

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def slugify(keyword):
    return re.sub(r'[^a-z0-9-]', '', keyword.lower().replace(' ', '-'))

def generate_article(keyword):
    prompt = f"""Write a complete SEO-optimized blog article for the keyword: "{keyword}"

Requirements:
- Exactly 800 to 1000 words — count carefully, this is critical
- One H1 heading at the top (the title)
- At least 4 H2 subheadings throughout
- Expand each section with detailed explanations, examples, and practical tips to reach the word count
- Natural, readable, informative content
- Include the placeholder [AFFILIATE_LINK] exactly twice, woven naturally into the text where a product/service link would fit
- Write in a helpful, professional tone
- No introduction or conclusion labels - just the article itself

Return the article as plain markdown text, nothing else."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def write_articles():
    with open("keywords.json") as f:
        keywords = json.load(f)

    os.makedirs("articles", exist_ok=True)

    for keyword in keywords:
        print(f"Writing article for: {keyword}")
        article = generate_article(keyword)
        filename = f"articles/{slugify(keyword)}.md"
        with open(filename, "w") as f:
            f.write(article)
        print(f"  Saved to {filename}")

    print("\nAll articles written.")

if __name__ == "__main__":
    write_articles()
