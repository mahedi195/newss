import google.generativeai as genai

genai.configure(api_key='AIzaSyD6Hnqmrwe-D3Y8qlz_Q69-6ynDyf6lX44')

def generate(contents):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Use a valid model name
    response = model.generate_content(contents)
    return response.text

if __name__ == "__main__":
    print(generate("Why is the sky blue?"))
