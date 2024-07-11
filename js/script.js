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

    const button = document.getElementById("button");
    const label = document.getElementById("label");
    const upload = document.getElementById("upload");
    const input = document.getElementById("input");

    button.style.display = 'none';
    label.style.display = 'none';

    upload.textContent = "обрабатываем файл..."
    upload.style.display = 'block';

    input.disabled = 'disabled';

    const load = document.createElement('div');
    load.className = "form_load";

    const loadLane = document.createElement('div');
    loadLane.className = "load_lane";
    load.appendChild(loadLane);

    form.appendChild(load);
}

async function textShowcase() {
    const select_header = document.getElementById('select_header');
    const form_select = document.getElementById('form_select');

    const form = document.getElementById('form');
    const subtext = document.getElementById('subtext');

    const scroll = document.getElementById('scroll');
    const buttons = document.getElementById('buttons');

    select_header.style.display = 'none';
    form_select.style.display = 'none';

    form.style.display = 'none';
    subtext.style.display = 'none';

    scroll.style.display = 'block';
    buttons.style.display = 'flex';
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
