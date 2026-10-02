const slidess = document.querySelectorAll(".slide");
let counter = 0;

slidess.forEach((slide, index) => {
  slide.style.left = `${index * 100}%`;
});

const goPrev = () => {
  counter--;
  if (counter < 0) {
    counter = slidess.length - 1; 
  }
  slideImage();
};

const goNext = () => {
  counter++;
  if (counter >= slidess.length) {
    counter = 0; 
  }
  slideImage();
};

const slideImage = () => {
  slidess.forEach((slide) => {
    slide.style.transform = `translateX(-${counter * 100}%)`;
  });
};
