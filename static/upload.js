document.addEventListener('DOMContentLoaded', function () {
    const dropArea = document.getElementById('drop-area');

    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        sendFilesToServer(files);
    });

    function sendFilesToServer(files) {
        const formData = new FormData();

        for (let i = 0; i < files.length; i++) {
            const file = files[i];

            if (file.type === 'application/json') {
                formData.append('json_files', file);
            } else {
                alert('Please drop only JSON files.');
                return;
            }
        }
        fetch('/process_json', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                console.log('JSON files sent successfully to the server.');
            } else {
                console.error('Error sending JSON files to the server.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
