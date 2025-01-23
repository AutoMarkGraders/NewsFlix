// Handle PDF upload
document.getElementById('upload-btn').addEventListener('click', function () {
    const fileInput = document.getElementById('pdf-upload');
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a PDF file.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Show pages section
            document.getElementById('pages-section').style.display = 'block';
            const pdfPath = data.pdf_path;

            // Fetch pages as images
            fetch(`http://127.0.0.1:5000/get-pages?pdf_path=${encodeURIComponent(pdfPath)}`)
                .then(response => response.json())
                .then(data => {
                    const pagesContainer = document.getElementById('pages-container');
                    pagesContainer.innerHTML = ''; // Clear previous images

                    data.pages.forEach(pagePath => {
                        const img = document.createElement('img');
                        img.src = `http://127.0.0.1:5000/output${pagePath}`; // This path now points to the output folder
                        img.classList.add('page-image');
                        img.addEventListener('click', () => loadImageToCanvas(pagePath));
                        pagesContainer.appendChild(img);
                    });
                });
        } else {
            alert("Error uploading PDF: " + data.error);
        }
    })
    .catch(error => {
        console.error('Error uploading PDF:', error);
        alert("An error occurred while uploading the PDF.");
    });
});

// Load selected image into canvas for cropping
function loadImageToCanvas(imagePath) {
    const cropCanvas = document.getElementById('crop-canvas');
    const ctx = cropCanvas.getContext('2d');
    
    const img = new Image();
    img.onload = function() {
        cropCanvas.width = img.width;
        cropCanvas.height = img.height;
        ctx.drawImage(img, 0, 0);
    };
    img.src = `http://127.0.0.1:5000/output${imagePath}`; // Update image path to point to output folder

    // Show crop section
    document.getElementById('crop-section').style.display = 'block';

    // Enable cropping when user clicks on the canvas
    cropCanvas.addEventListener('click', function (e) {
        const rect = cropCanvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        // Example crop: You can adjust this logic to allow selection of any region
        const width = 100;
        const height = 100;

        // Call backend to crop the image
        cropImage(imagePath, x, y, width, height);
    });
}

// Send cropping request to backend
function cropImage(imagePath, x, y, width, height) {
    const data = {
        image_path: imagePath,
        x: x,
        y: y,
        width: width,
        height: height
    };

    fetch('http://127.0.0.1:5000/crop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.cropped_image_path) {
            displayCroppedImage(data.cropped_image_path);
        } else {
            alert('Error cropping image: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error cropping image:', error);
        alert('An error occurred while cropping the image.');
    });
}

// Display cropped image
function displayCroppedImage(croppedImagePath) {
    const croppedImageContainer = document.getElementById('cropped-image-container');
    const img = document.createElement('img');
    img.src = `http://127.0.0.1:5000/output${croppedImagePath}`; // Corrected to point to output folder path
    img.classList.add('cropped-image');
    croppedImageContainer.innerHTML = ''; // Clear previous cropped image
    croppedImageContainer.appendChild(img);
}

// Handle Show Images button click
document.getElementById('show-btn').addEventListener('click', function() {
    fetch('http://127.0.0.1:5000/get-images')
        .then(response => response.json())
        .then(data => {
            const imageGallery = document.getElementById('image-gallery');
            imageGallery.innerHTML = ''; // Clear previous images
            imageGallery.style.display = 'block'; // Show the gallery

            data.forEach(imageUrl => {
                const img = document.createElement('img');
                img.src = `http://127.0.0.1:5000${imageUrl}`;
                img.classList.add('gallery-image');
                imageGallery.appendChild(img);
            });
        })
        .catch(error => {
            console.error('Error fetching images:', error);
            alert('An error occurred while loading images.');
        });
});
