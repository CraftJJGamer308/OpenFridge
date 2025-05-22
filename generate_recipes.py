import time
import openai

import os
import base64
from bs4 import BeautifulSoup
import html2text

import requests


client = openai.OpenAI(api_key="xxxxxx")

# Initialize a list of messages (chat history)
chat_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

categories = ["no need to buy ingredients", "need to buy ingredients", "healthy", "dessert", "breakfast", "dinner", "lunch"]
joined_categories = ",".join(categories)

def ask_openai(prompt):
    # Add the new user message to the history
    chat_history.append({"role": "user", "content": prompt})

    # Send the whole history
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    # Get assistant's reply
    reply = response.choices[0].message.content

    # Add the assistant's reply to the history too
    chat_history.append({"role": "assistant", "content": reply})

    return reply

def main():
    path = "productList.txt"
    
    try:
        with open(path, 'r') as file:
            content = file.read()
            print("File content:")
            print(content)
    except FileNotFoundError:
        print(f"The file {path} does not exist.")
        return

    if content.strip():  # Only continue if the file isn't empty
        for i in range(3):
            response = ask_openai(
                "Create a simple recipe using only the items in the list: " + content + 
                ". Format the recipe using basic HTML tags (use <h1>, <h2>, <ul>, <li>, <p>, etc.). Do NOT wrap the output in code blocks like ```html. The first line should contain some of the given categries: " +
                joined_categories + " The first line should be plain text, just comma seperated categories. Start the recipe with time needed for cooking, difficulty level (from 1 to 5) and number of portions from the recipe. No introduction or conclusion. Make sure that the recipe is unique, other than the ones already created.")
            filename = f"./public/recipes/recipe{i+1}.html"
            with open(filename, "w") as file:
                file.write(response)
            print("\nRecipe " + str(i+1) + " saved to " + filename)

        for i in range(2):
            response = ask_openai(
                "Create a simple recipe using the items in the list and some other that we could buy, or that we potentially already have at home: " + content + 
                ". Format the recipe using basic HTML tags (use <h1>, <h2>, <ul>, <li>, <p>, etc.). Divide the ingredient list ind two parts. At first the products that we already have and second the products that we need to buy. Do NOT wrap the output in code blocks like ```html. No introduction or conclusion. Make sure that the recipe is unique, other than the ones already created.")
            filename = f"./public/recipes/recipe_extra{i+1}.html"
            with open(filename, "w") as file:
                file.write(response)
            print("\nRecipe extra" + str(i+1) + " saved to " + filename)

if __name__ == "__main__":
    main()




#############################


for i in range(1,4):
    with open('./public/recipes/recipe'+str(i)+'.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    def html_to_text(html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()

    # Umwandlung durchführen
    plain_text = html_to_text(html_content)

    # Ergebnis ausgeben
    print(plain_text)

    response = client.images.generate(
        model="dall-e-3",
        prompt="give me a photography of the dish described in the recipe" + plain_text,
        n=1,  # Anzahl der Bilder, die du generieren möchtest
        size="1024x1024",  # Bildgröße (z. B. 256x256, 512x512, 1024x1024)
    )

    response = requests.get(response.data[0].url)

    # Speichere es als JPEG
    if response.status_code == 200:
        with open('./public/recipes/recipe'+str(i)+'.jpg', "wb") as file:
            file.write(response.content)
        print("Bild erfolgreich gespeichert!")
    else:
        print("Fehler beim Download:", response.status_code)


for i in range(1,3):
    with open('./public/recipes/recipe_extra'+str(i)+'.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    def html_to_text(html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()

    # Umwandlung durchführen
    plain_text = html_to_text(html_content)

    # Ergebnis ausgeben
    print(plain_text)

    response = client.images.generate(
        model="dall-e-3",
        prompt="give me a photography of the dish described in the recipe" + plain_text,
        n=1,  # Anzahl der Bilder, die du generieren möchtest
        size="1024x1024",  # Bildgröße (z. B. 256x256, 512x512, 1024x1024)
    )

    response = requests.get(response.data[0].url)

    # Speichere es als JPEG
    if response.status_code == 200:
        with open('./public/recipes/recipe_extra'+str(i)+'.jpg', "wb") as file:
            file.write(response.content)
        print("Bild erfolgreich gespeichert!")
    else:
        print("Fehler beim Download:", response.status_code)


