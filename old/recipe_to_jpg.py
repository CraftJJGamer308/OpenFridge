import os
from openai import OpenAI
import base64
from bs4 import BeautifulSoup
import html2text

import requests

client = OpenAI(
    # This is the default and can be omitted
    api_key="xxxxxx",
)

for i in range(1,6):
    with open('public/recipes/recipe'+str(i)+'.html', 'r', encoding='utf-8') as file:
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
        prompt="give me a realistig photo of the dish described in the recipe" + plain_text,
        n=1,  # Anzahl der Bilder, die du generieren möchtest
        size="1024x1024",  # Bildgröße (z. B. 256x256, 512x512, 1024x1024)
    )

    response = requests.get(response.data[0].url)

    # Speichere es als JPEG
    if response.status_code == 200:
        with open('public/recipes/recipe'+str(i)+'.jpg', "wb") as file:
            file.write(response.content)
        print("Bild erfolgreich gespeichert!")
    else:
        print("Fehler beim Download:", response.status_code)


for i in range(1,6):
    with open('public/recipes/recipe_extra'+str(i)+'.html', 'r', encoding='utf-8') as file:
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
        prompt="give me a realistig photo of the dish described in the recipe" + plain_text,
        n=1,  # Anzahl der Bilder, die du generieren möchtest
        size="1024x1024",  # Bildgröße (z. B. 256x256, 512x512, 1024x1024)
    )

    response = requests.get(response.data[0].url)

    # Speichere es als JPEG
    if response.status_code == 200:
        with open('public/recipes/recipe_extra'+str(i)+'.jpg', "wb") as file:
            file.write(response.content)
        print("Bild erfolgreich gespeichert!")
    else:
        print("Fehler beim Download:", response.status_code)


