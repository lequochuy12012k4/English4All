document.addEventListener('DOMContentLoaded', function() { // Ensure DOM is fully loaded

    const link = document.getElementById('my-link');

    if (link) { // Check if the link exists
        link.addEventListener('click', function(event) {
            // Prevent the link from actually navigating (if you want to handle the navigation differently)
            // event.preventDefault();

            const newTitle = this.dataset.title; // Get the title from the data-title attribute
            document.title = newTitle;

            // Optionally, perform other actions like redirecting to the link's URL
            // window.location.href = this.href; // This is how you navigate
        });
    } else {
        console.warn("Link with ID 'my-link' not found.");
    }
});