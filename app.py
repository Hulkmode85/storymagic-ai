import os
from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic

app = Flask(__name__)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/docs")
def docs():
    return render_template("landing.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    child_name = data.get("child_name", "")
    age = data.get("age", "5")
    theme = data.get("theme", "")
    favorites = data.get("favorites", "")
    length = data.get("length", "medium")
    style = data.get("style", "adventure")

    length_map = {"short": "about 300 words", "medium": "about 600 words", "long": "about 1000 words"}
    word_count = length_map.get(length, "about 600 words")

    prompt = f"""Write a personalized children's bedtime story with these details:
- Main character name: {child_name}
- Child's age: {age} years old
- Lesson/theme to teach: {theme}
- Child's favorite things to include: {favorites}
- Story style: {style}
- Length: {word_count}

Guidelines:
- Use age-appropriate vocabulary for a {age}-year-old
- Include a clear moral/lesson woven naturally into the story
- Make {child_name} the hero of the story
- Include vivid but gentle imagery suitable for bedtime
- End on a warm, peaceful note perfect for falling asleep
- Include the child's favorite things as story elements
- Use short paragraphs and simple sentences for younger children
- Add a title at the top
- End with "The End" and a one-line moral summary

Make it magical, warm, and memorable."""

    try:
        message = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"story": message.content[0].text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5036)
