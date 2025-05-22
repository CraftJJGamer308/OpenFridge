
// const form = document.getElementById('uploadForm');
// const loadingDiv = document.getElementById('loading');

// form.addEventListener('submit', function () {
//     loadingDiv.style.display = 'block'; // Show loading screen
// });

// Function to load HTML files and corresponding images from the /recipes directory
async function loadRecipes() {
    const recipesContainer = document.getElementById('recipes-container');
    const recipeFiles = [
        { html: 'recipe1.html', img: 'recipe1.jpg' },
        { html: 'recipe2.html', img: 'recipe2.jpg' },
        { html: 'recipe3.html', img: 'recipe3.jpg' },
        // { html: 'recipe4.html', img: 'recipe4.jpg' },
        // { html: 'recipe5.html', img: 'recipe5.jpg' },
        { html: 'recipe_extra1.html', img: 'recipe_extra1.jpg' },
        { html: 'recipe_extra2.html', img: 'recipe_extra2.jpg' },
        // { html: 'recipe_extra3.html', img: 'recipe_extra3.jpg' },
        // { html: 'recipe_extra4.html', img: 'recipe_extra4.jpg' },
        // { html: 'recipe_extra5.html', img: 'recipe_extra5.jpg' }
    ]; // List your recipe files and corresponding images here

    for (const recipe of recipeFiles) {
        try {
            // Load the HTML content
            const response = await fetch(`recipes/${recipe.html}`);
            if (!response.ok) throw new Error(`Could not load ${recipe.html}`);
            const text = await response.text();

            // Parse the HTML and extract the first <h1>
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');
            const h1 = doc.querySelector('h1');
            const tags = doc.querySelector('p');

            const content = `<a href="/recipes/${recipe.html}">`+(h1 ? h1.innerHTML : '')+'</a>'; // Store the inner HTML of the first <h1> or an empty string if not found


            // Create a new div for the recipe
            const recipeDiv = document.createElement('div');
            recipeDiv.className = 'recipe';

            // Create an image element
            const img = document.createElement('img');
            img.src = `recipes/${recipe.img}`;
            img.alt = `Image for ${recipe.html}`;
            img.width = "400";

            // Insert the image and content into the recipe div
            recipeDiv.appendChild(img);
            recipeDiv.innerHTML += content; // Append the HTML content

            // Append the recipe div to the container
            recipesContainer.appendChild(recipeDiv);
        } catch (error) {
            console.error(error);
        }
    }
}

// Load recipes when the page is fully loaded
window.onload = loadRecipes;