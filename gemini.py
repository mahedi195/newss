from google import genai
from google.genai import types

# Only run this block for Gemini Developer API
client = genai.Client(api_key='AIzaSyD6Hnqmrwe-D3Y8qlz_Q69-6ynDyf6lX44')


def generate(contents):
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=contents
    )
    return response.text



if __name__ == "__main__":
    print(generate(contents=["why is the sky blue?"]))