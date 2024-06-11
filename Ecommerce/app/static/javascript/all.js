document.addEventListener('DOMContentLoaded', function() {
    const carouselContainer = document.querySelector('.carouselContainer');
    const carouselInner = document.querySelector('.carouselInner');
    const carouselItems = document.querySelectorAll('.carouselItem');
    
    // Get the carousel control buttons
    const prevBtn = document.querySelector('.carouselControlPrev');
    const nextBtn = document.querySelector('.carouselControlNext');
    
    // Set the initial index
    let currentIndex = 0;
    
    // Function to move the carousel
    function moveCarousel(direction) {
      // Calculate the new index based on the direction
      if (direction === 'next') {
        currentIndex = (currentIndex + 1) % carouselItems.length;
      } else {
        currentIndex = (currentIndex - 1 + carouselItems.length) % carouselItems.length;
      }
    
      // Translate the carousel inner container
      carouselInner.style.transform = `translateX(-${currentIndex * 20}%)`;
    }
    
    // Add event listeners to the control buttons
    prevBtn.addEventListener('click', () => moveCarousel('prev'));
    nextBtn.addEventListener('click', () => moveCarousel('next'));
    
    // Automatically move the carousel every 5 seconds
    setInterval(() => moveCarousel('next'), 10000);
      });


// Get the carousel container, inner container, and items
