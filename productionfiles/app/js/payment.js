function updateItem(itemId, action, itemType) {
    let url = '';
    let data = {};

    if (itemType === 'course') {
        url = '/course/mua_khoa_hoc/';
        data = {'courseId': itemId, 'action': action};
    } else if (itemType === 'book') {
        url = '/sach/mua_sach/';
        data = {'bookId': itemId, 'action': action};
    } else {
        console.error('Invalid itemType:', itemType);
        return; // Exit the function if itemType is invalid
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Data:', data);
        // Handle the response, maybe update the cart display
        location.reload(); // Simple way to update the page
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.'); // User-friendly message
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const courseButtons = document.getElementsByClassName('buy-course');
    for (let i = 0; i < courseButtons.length; i++) {
        courseButtons[i].addEventListener('click', function() {
            const courseId = this.dataset.course;
            const action = this.dataset.action;

            if (user === "AnonymousUser") {
                alert('You need to log in to add courses to your cart.');
            } else {
                updateItem(courseId, action, 'course');
            }
        });
    }

    const bookButtons = document.getElementsByClassName('buy-book');
    for (let i = 0; i < bookButtons.length; i++) {
        bookButtons[i].addEventListener('click', function() {
            const bookId = this.dataset.book;
            const action = this.dataset.action;
            
            if (user === "AnonymousUser") {
                alert('You need to log in to add books to your cart.');
            } else {
                updateItem(bookId, action, 'book');
            }
        });
    }
});