
window.onload = () => {
    gsap.timeline()
        // .from("h1", {duration: 1, opacity: 0, y: -50, ease: "power2.out"})
        .from(".nav-section", {duration: 0.8, opacity: 0, x: -200, ease: "power2.out"}, "-=0.5")
        .from(".hero-section h1", {duration: 1, opacity: 0, scale: 0.5, ease: "bounce.out"})
        .from(".video-frame", {duration: 1, opacity: 0, y: 100, ease: "power3.out"}, "-=0.5");
};

document.querySelectorAll('.scroll-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const target = this.getAttribute('href');
        
        gsap.to(window, { duration: 2, scrollTo: target, ease: "power2.out" });
    });
});


gsap.from(".hero-section h1", {
    scrollTrigger: ".hero-section h1",
    duration: 1,
    text: {value: "A Deep-Fake Detection Solution", speed: 1},
    ease: "power1.inOut"
});



const tryNowButton = document.querySelector('.button-49');

tryNowButton.addEventListener('mouseenter', () => {
    gsap.to(tryNowButton, {duration: 0.5, scale: 1.1, ease: "power1.out"});
});

tryNowButton.addEventListener('mouseleave', () => {
    gsap.to(tryNowButton, {duration: 0.5, scale: 1, ease: "power1.out"});
});

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


let slideIndex = 0;
const slidesContainer = document.querySelector(".slides");
const totalSlides = document.getElementsByClassName("slide").length;

// Auto-play setup
let autoplayInterval = setInterval(function() {
    moveSlide(1); // Move to next slide every 3 seconds
}, 3000);

function moveSlide(n) {
    slideIndex += n;
    if (slideIndex >= totalSlides) {
        slideIndex = 0;
    } else if (slideIndex < 0) {
        slideIndex = totalSlides - 1;
    }
    updateSlidePosition();
    resetAutoplay(); // Reset autoplay timer after manual navigation
}

function currentSlide(n) {
    slideIndex = n;
    updateSlidePosition();
    resetAutoplay(); // Reset autoplay timer after manual navigation
}

function updateSlidePosition() {
    slidesContainer.style.transform = `translateX(-${slideIndex * 100}%)`; // Slide effect
}

function resetAutoplay() {
    clearInterval(autoplayInterval);
    autoplayInterval = setInterval(function() {
        moveSlide(1); // Restart autoplay
    }, 3000);
}




