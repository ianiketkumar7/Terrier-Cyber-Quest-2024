window.onload = () => {
    gsap.timeline()
        // .from("h1", {duration: 1, opacity: 0, y: -50, ease: "power2.out"})
        .from(".TextSection", {duration: 3, opacity: 0, x: -200, ease: "power2.out"}, "-=0.5")
        .from(".TextSection span", {duration: 1, opacity: 0, scale: 0.5, ease: "bounce.out"})
        .from(".uploaderSection", {duration: 1, opacity: 0, y: 100, ease: "power3.out"}, "-=0.5");
};

const openButton = document.querySelector('.open-button');
const closeButton = document.querySelector('.close-button');
const links = document.querySelector('.links');
const getImage = document.querySelector('.image');

// Function to open the menu
const openMenu = () => {
    gsap.to(links, {duration: 1, x: '0%', onComplete: () => {
        links.classList.add('setLinks');
        document.addEventListener('click', closeMenuOnClickOutside);  // Add event listener when menu opens
    }});
}

// Function to close the menu
const closeMenu = () => {
    gsap.to(links, {duration: 1, x: '-100%', onComplete: () => {
        links.classList.remove('setLinks');
        document.removeEventListener('click', closeMenuOnClickOutside);  // Remove event listener when menu closes
    }});
}

// Open button event listener
openButton.addEventListener('click', (event) => {
    event.stopPropagation();  // Prevent click event from propagating to document
    openButton.classList.add('setButton');
    openMenu();
    getImage.classList.remove('setImageLast');
    getImage.classList.add('setImageFirst');
});

// Close button event listener
closeButton.addEventListener('click', () => {
    getImage.classList.remove('setImageFirst');
    getImage.classList.add('setImageLast');
    closeMenu();
    openButton.classList.remove('setButton');
});

// Function to close menu if clicking outside
const closeMenuOnClickOutside = (event) => {
    if (!links.contains(event.target) && !openButton.contains(event.target)) {
        // Check if the click is outside the menu and the open button
        getImage.classList.remove('setImageFirst');
        getImage.classList.add('setImageLast');
        closeMenu();
        openButton.classList.remove('setButton');
    }
};




function checkURL() {
    var url = document.getElementById("url").value;
    fetch('/check_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({url: url}),
    })
    .then(response => response.json())
    .then(data => {
        if(data.result){
            document.getElementById("result").innerHTML = "Result: " + data.result;
        } else {
            document.getElementById("result").innerHTML = "Error: " + data.error;
        }
    })
    .catch(error => {
        document.getElementById("result").innerHTML = "Error: " + error;
    });
}

// Handle file upload response
document.getElementById('file-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    var formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.result){
            document.getElementById("result").innerHTML = "Result: " + data.result;
        } else {
            document.getElementById("result").innerHTML = "Error: " + data.error;
        }
    })
    .catch(error => {
        document.getElementById("result").innerHTML = "Error: " + error;
    });
});
