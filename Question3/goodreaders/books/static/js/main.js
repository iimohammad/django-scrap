document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    let formData = new FormData(this);
    fetch('/search/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Update UI with search results
        document.getElementById('results-container').innerHTML = data.results_html;
    })
    .catch(error => console.error('Error:', error));
});