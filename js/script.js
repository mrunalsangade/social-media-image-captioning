document.getElementById('upload-form').onsubmit = function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result-image').src = data.image;
        document.getElementById('caption').textContent = data.caption;
        document.getElementById('result-section').classList.remove('hidden');
    })
    .catch(error => console.error('Error:', error));
};
