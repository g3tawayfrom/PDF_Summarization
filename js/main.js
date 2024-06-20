/*function waitingFile() {
    let temp = 0;
    while (temp === 0) {
        const fileInput = document.getElementById("f_file");
        if (fileInput.length === undefined) {
            temp = 1;
        }
    }
}*/

async function uploadFunc() {
    /*await waitingFile()

    const fileInput = document.getElementById("f_file");
    for (const file of fileInput.files) {
        alert(file.name);
    }*/

    const dropZone = document.getElementById('dropZone')
    const button = document.getElementById("f_button");
    const upload = document.getElementById("f_upload");
    const label = document.getElementById("f_label");
    const fileField = document.getElementById("f_file");

    /*upload.textContent = "готово"*/
    upload.textContent = "обрабатываем файл..."

    button.style.display = 'none';
    upload.style.display = 'block';
    label.style.display = 'none';

    fileField.disabled = 'disabled';

    const loadBox = document.createElement('div');
    loadBox.className = "f_load_box";

    const load = document.createElement('div');
    load.className = "f_load";
    loadBox.appendChild(load);

    dropZone.appendChild(loadBox);
}