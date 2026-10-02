let currentIndex = 0;
const slides = document.querySelectorAll(".slides img");
const totalSlides = slides.length;

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.remove("active");
    if (i === index) {
      slide.classList.add("active");
    }
  });
}

function nextSlide() {
  currentIndex = (currentIndex + 1) % totalSlides;
  showSlide(currentIndex);
}

// Show first slide
showSlide(currentIndex);

// Change every 5s
setInterval(nextSlide, 5000);
