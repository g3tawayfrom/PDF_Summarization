window.addEventListener('load', () => {
    const width = window.innerWidth;
    const name = document.getElementById("h_name");

    if (width <= 635) {
        name.textContent =  "САБТ";
    } else {
        name.textContent =  "СИСТЕМА АНАЛИЗА БОЛЬШИХ ТЕКСТОВ";
    }
})

window.addEventListener('resize', () => {
    const width = window.innerWidth;
    const name = document.getElementById("h_name");

    if (width <= 635) {
        name.textContent =  "САБТ";
    } else {
        name.textContent =  "СИСТЕМА АНАЛИЗА БОЛЬШИХ ТЕКСТОВ";
    }
})

async function uploadFunc() {
    const dropZone = document.getElementById('dropZone');
    const button = document.getElementById("f_button");
    const upload = document.getElementById("f_upload");
    const label = document.getElementById("f_label");
    const fileField = document.getElementById("f_file");

    upload.textContent = "обрабатываем файл...";

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
