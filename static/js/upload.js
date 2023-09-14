document.addEventListener('DOMContentLoaded', function () {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');


    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        sendFilesToServer(files);
    });

    dropArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const files = e.target.files;
        sendFilesToServer(files);
    });

    function sendFilesToServer(files) {
        const formData = new FormData();

        for (let i = 0; i < files.length; i++) {
            const file = files[i];

            if (file.type === 'application/json' || file.type === 'application/zip') {
                formData.append('json_files', file);
            } else {
                alert('Please drop only JSON or ZIP files.');
                return;
            }
        }
        fetch('/process_json', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Files sent successfully to the server.');
                window.location.href = "/success_page";
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
