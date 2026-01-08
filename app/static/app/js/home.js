
document.addEventListener('DOMContentLoaded', function () {
    const courseItems = document.querySelectorAll('.course-item');
    const prevButton = document.getElementById('prev-course');
    const nextButton = document.getElementById('next-course');
    let currentIndex = 0;
    const itemsPerPage = 4; // Số lượng khóa học hiển thị

    function showCourses() {
        courseItems.forEach((item, index) => {
            if (index >= currentIndex && index < currentIndex + itemsPerPage) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    function updateButtons() {
        prevButton.disabled = currentIndex === 0;
        nextButton.disabled = currentIndex + itemsPerPage >= courseItems.length;
    }

    showCourses();
    updateButtons();

    prevButton.addEventListener('click', function () {
        currentIndex = Math.max(0, currentIndex - 1);
        showCourses();
        updateButtons();
        courseItems.forEach(item => {
            item.style.transition = 'transform 0.5s ease-in-out';
            item.style.transform = 'translateX(100px)'; // Di chuyển sang phải
            setTimeout(() => {
                item.style.transition = 'none';
                item.style.transform = 'translateX(0)';
                showCourses();
                updateButtons();
            }, 500); // Đợi animation kết thúc
        });
    });

    nextButton.addEventListener('click', function () {
        if (currentIndex + itemsPerPage < courseItems.length) {
            currentIndex++;
            showCourses();
            updateButtons();
        }
        courseItems.forEach(item => {
            item.style.transition = 'transform 0.5s ease-in-out';
            item.style.transform = 'translateX(-100px)'; // Di chuyển sang trái
            setTimeout(() => {
                item.style.transition = 'none';
                item.style.transform = 'translateX(0)';
                showCourses();
                updateButtons();
            }, 500); // Đợi animation kết thúc
        });
    });
    function showCourses() {
        courseItems.forEach((item, index) => {
            if (index >= currentIndex && index < currentIndex + itemsPerPage) {
                item.classList.add('active');
                setTimeout(() => item.classList.add('show'), 10); // Thêm class 'show' sau một khoảng thời gian ngắn
            } else {
                item.classList.remove('active', 'show');
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        const icon = item.querySelector('.faq-question i'); // Select the icon

        question.addEventListener('click', () => {
            // Toggle active class on question
            question.classList.toggle('active');

            // Toggle active class on answer
            answer.classList.toggle('active');

            //Toggle font awesome class to chevron
            icon.classList.toggle('fas-fa-chevron-up');

        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    // Initially set all slides to be offscreen to the right.  This makes the "cover" animation work
    slides.forEach((slide, index) => {
        slide.style.left = '100%';
        if (index === 0) {
            slide.classList.add('active');
            slide.style.left = '0'; // Make the initial slide visible.
        } else {
            slide.classList.remove('active');
        }
    });

    function showSlide(n) {
        // Remove active class from current slide
        slides[currentSlide].classList.remove('active');
        slides[currentSlide].style.left = '-100%'; // Move current slide offscreen to the left

        // Update current slide
        currentSlide = n;

        // Add active class to new slide
        slides[currentSlide].classList.add('active');
        slides[currentSlide].style.left = '0'; // Slide in from the right
    }

    function nextSlide() {
        let next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }

    setInterval(nextSlide, 3000); // Change slide every 3 seconds
});

const modal = document.getElementById('courseDetailsModal');
if (modal) { // Check if modal exists
    const modalCourseName = document.getElementById('modalCourseName');
    const modalCourseLevel = document.getElementById('modalCourseLevel');
    const modalCoursePrice = document.getElementById('modalCoursePrice');
    const modalCourseDuration = document.getElementById('modalCourseDuration');
    const modalCourseDescription = document.getElementById('modalCourseDescription');
    const modalCourseVideo = document.getElementById('modalCourseVideo');
    const modalCourseVideoContainer = document.getElementById('modalCourseVideoContainer');
    const closeButton = modal.querySelector('.close-button');

    const detailTriggers = document.querySelectorAll('.view-course-details-trigger');

    detailTriggers.forEach(button => {
        button.addEventListener('click', function () {
            const name = this.dataset.name;
            const level = this.dataset.level;
            const price = this.dataset.price;
            const description = this.dataset.description;
            const duration = this.dataset.duration;
            const videoUrl = this.dataset.videoUrl;

            if (modalCourseName) modalCourseName.textContent = name;
            if (modalCourseLevel) modalCourseLevel.textContent = level;
            if (modalCoursePrice) modalCoursePrice.textContent = price;
            if (modalCourseDuration) modalCourseDuration.textContent = duration;
            if (modalCourseDescription) modalCourseDescription.innerHTML = description; // Use innerHTML if description contains HTML formatting

            if (videoUrl && modalCourseVideo) {
                let embedUrl = videoUrl;
                if (videoUrl.includes("youtube.com/watch?v=")) {
                    embedUrl = videoUrl.replace("watch?v=", "embed/");
                } else if (videoUrl.includes("youtu.be/")) {
                    embedUrl = videoUrl.replace("youtu.be/", "youtube.com/embed/");
                }
                // Remove query parameters like list, t, etc. from YouTube embed URL
                if (embedUrl.includes("?")) {
                    embedUrl = embedUrl.substring(0, embedUrl.indexOf("?"));
                }
                modalCourseVideo.src = embedUrl;
                if (modalCourseVideoContainer) modalCourseVideoContainer.style.display = 'block';
            } else {
                if (modalCourseVideo) modalCourseVideo.src = '';
                if (modalCourseVideoContainer) modalCourseVideoContainer.style.display = 'none';
            }
            modal.style.display = 'block';
        });
    });

    if (closeButton) {
        closeButton.addEventListener('click', function () {
            modal.style.display = 'none';
            if (modalCourseVideo) modalCourseVideo.src = ''; // Stop video when closing
        });
    }

    window.addEventListener('click', function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
            if (modalCourseVideo) modalCourseVideo.src = ''; // Stop video when closing
        }
    });
}

function confirmPurchase() {
    alert("Khóa học được thêm vào phần thanh toán")
}

function showRegistrationAlert() {
    alert("Thông tin đăng ký đã được gửi vào gmail của bạn!");
    return true; // Allow the form to submit
}
