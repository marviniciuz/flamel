document.addEventListener('DOMContentLoaded', function() {
    M.AutoInit(); 
    setupDropzone();
});

document.body.addEventListener('htmx:afterSwap', function(evt) {
    M.AutoInit();
    setupDropzone();
});

function setupDropzone() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('id_arquivo_original');

    if (!dropzone || !fileInput) return;

    // Evita configurar mais de uma vez
    if (dropzone.classList.contains('js-dropzone-ready')) return;
    dropzone.classList.add('js-dropzone-ready');

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add('teal', 'lighten-5');
        dropzone.style.border = "2px dashed #26a69a";
    });

    dropzone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove('teal', 'lighten-5');
        dropzone.style.border = "none";
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove('teal', 'lighten-5');
        dropzone.style.border = "none";
        
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            updateDropzoneUI(fileInput);
        }
    });

    fileInput.addEventListener('change', () => {
        updateDropzoneUI(fileInput);
    });
}

function updateDropzoneUI(input) {
    if (input.files && input.files[0]) {
        const dropText = document.querySelector('#dropzone p');
        const dropIcon = document.querySelector('#dropzone i');
        
        if(dropText) {
            dropText.textContent = input.files[0].name;
            dropText.classList.remove('grey-text');
            dropText.classList.add('teal-text', 'text-darken-2');
            dropText.style.fontWeight = 'bold';
        }
        if(dropIcon) {
            dropIcon.textContent = 'check_circle';
            dropIcon.classList.remove('grey-text');
            dropIcon.classList.add('teal-text');
        }
    }
}


