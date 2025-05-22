const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;

// Set up storage for uploaded files
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadDir = path.join(__dirname, 'uploads');
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir);
        }
        cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
        const ext = path.extname(file.originalname);
        const newFileName = `bild${ext}`;
        cb(null, newFileName);
    }
});

const upload = multer({ storage });

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: true })); // Middleware to parse URL-encoded bodies
app.use(express.json()); // Middleware to parse JSON bodies

// Store the result temporarily
let productResults = '';

// Handle file upload
app.post('/upload', upload.single('file'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('No file uploaded.');
    }

    // Path to the uploaded file
    const filePath = path.join(__dirname, 'uploads', req.file.filename);

    // Call the Python script to process the file
    exec(`python process_file.py`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error}`);
            return res.status(500).send('Error processing file.');
        }
        
        // Store the result for later retrieval
        productResults = stdout.trim();
        
        // Redirect to the results page
        res.redirect('/recipes.html');
    });
});

// Route to get the results
app.post('/getRecipe', (req, res) => {
    console.log(req.body); // Log the entire body to see its structure
    
    const results = req.body.results; // Access the textarea input

    if (results) {
        // Define the path where you want to save the file
        const filePath = path.join(__dirname, 'productList.txt');

        // Write the results to a text file
        fs.writeFile(filePath, results, (err) => {
            if (err) {
                console.error('Error writing to file:', err);
                return res.status(500).send('Error saving results.');
            }
        });
        exec(`python generate_recipes.py`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing Python script: ${error}`);
                return res.status(500).send('Error processing file.');
            }
            
            // Redirect to the results page
            res.redirect('/');
        });
    } else {
        res.status(400).send('No results received.');
    }
});

// Route to get the results
app.get('/productResults', (req, res) => {
    res.json({ result: productResults });
});


// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
//ideas: generate an editing page, so that items invisible or outside of the fridge can be added
