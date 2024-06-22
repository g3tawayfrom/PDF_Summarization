window.addEventListener('load', () => {
    const width = window.innerWidth;
    const name = document.getElementById("header_name");

    if (width <= 635) {
        name.textContent =  "САБТ";
    } else {
        name.textContent =  "СИСТЕМА АНАЛИЗА БОЛЬШИХ ТЕКСТОВ";
    }
})

window.addEventListener('resize', () => {
    const width = window.innerWidth;
    const name = document.getElementById("header_name");

    if (width <= 635) {
        name.textContent =  "САБТ";
    } else {
        name.textContent =  "СИСТЕМА АНАЛИЗА БОЛЬШИХ ТЕКСТОВ";
    }
})

async function uploadFunc() {
    /*await waitingFile()

    const fileInput = document.getElementById("f_file");
    for (const file of fileInput.files) {
        alert(file.name);
    }*/

    const form = document.getElementById('form');

    const button = document.getElementById("form_button");
    const label = document.getElementById("form_label");
    const upload = document.getElementById("form_upload");
    const input = document.getElementById("form_input");

    button.style.display = 'none';
    label.style.display = 'none';

    upload.textContent = "обрабатываем файл..."
    upload.style.display = 'block';

    input.disabled = 'disabled';

    const load = document.createElement('div');
    load.className = "form_load";

    const loadLane = document.createElement('div');
    load.className = "load_lane";
    load.appendChild(loadLane);

    input.appendChild(load);
}

/*function waitingFile() {
    let temp = 0;
    while (temp === 0) {
        const fileInput = document.getElementById("f_file");
        if (fileInput.length === undefined) {
            temp = 1;
        }
    }
}*/
