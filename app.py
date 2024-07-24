import openai
import flask
import logging
from config import OPENAI_API_KEY

# Set up the OpenAI API client
openai.api_key = OPENAI_API_KEY

# Set up the Flask app
app = flask.Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET", "POST"])
def generate_description():
    try:
        # Get the user's input text
        input_text = flask.request.form.get("input_text")
        logging.info(f"Received input_text: {input_text}")

        if input_text:
            # Use GPT-3.5-turbo to generate a description for the Instagram post
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Give me 2 line Quotes and 10 Hashtags for an Instagram post for the following text:\n{input_text}\n\nThe description should be no more than 100 characters."}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=100,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1
            )
            logging.info(f"OpenAI API response: {response}")
            description = response["choices"][0]["message"]["content"]
        else:
            description = None

        # Render the generated description in the HTML template
        return flask.render_template("index.html", input_text=input_text, description=description)
    except Exception as e:
        logging.error(f"Error generating description: {e}")
        return flask.render_template("index.html", input_text=None, description="error generating description")

if __name__ == "__main__":
    app.run(debug=True)
