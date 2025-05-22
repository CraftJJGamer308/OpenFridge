# import time
import openai
import asyncio
import aiohttp
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
        for i in range(5):
            response = ask_openai(
                "Create a simple recipe using only the items in the list: " + content + 
                ". Format the recipe using basic HTML tags (use <h1>, <h2>, <ul>, <li>, <p>, etc.). Do NOT wrap the output in code blocks like ```html. The first line should contain some of the given categries: " +
                joined_categories + " The first line should be plain text, just comma seperated categories. Start the recipe with time needed for cooking, difficulty level (from 1 to 5) and number of portions from the recipe. No introduction or conclusion. Make sure that the recipe is unique, other than the ones already created.")
            filename = f"./public/recipes/recipe{i+1}.html"
            with open(filename, "w") as file:
                file.write(response)
            print("\nRecipe " + str(i+1) + " saved to " + filename)

        for i in range(5):
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

async def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

async def generate_image(prompt, session, save_path):
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        image_url = response.data[0].url

        async with session.get(image_url) as img_response:
            if img_response.status == 200:
                content = await img_response.read()
                with open(save_path, "wb") as f:
                    f.write(content)
                print(f"Image saved successfully to {save_path}!")
            else:
                print(f"Error downloading image: Status code {img_response.status}")
    except Exception as e:
        print(f"Error generating or downloading image: {e}")

async def process_recipe(file_path, output_path, session):
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
        html_content = await file.read()

    plain_text = await html_to_text(html_content)
    prompt = "Give me a photography of the dish described in the recipe: " + plain_text

    await generate_image(prompt, session, output_path)

async def main():
    tasks = []

    async with aiohttp.ClientSession() as session:
        # Process recipes without extra ingredients
        for i in range(1, 6):
            file_path = f'./public/recipes/recipe{i}.html'
            output_path = f'./public/recipes/recipe{i}.jpg'
            tasks.append(process_recipe(file_path, output_path, session))

        # Process recipes with extra ingredients
        for i in range(1, 6):
            file_path = f'./public/recipes/recipe_extra{i}.html'
            output_path = f'./public/recipes/recipe_extra{i}.jpg'
            tasks.append(process_recipe(file_path, output_path, session))

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import aiofiles
    asyncio.run(main())
