function waitingFile() {
    let temp = 0;
    while (temp === 0) {
        const fileInput = document.getElementById("file");
        if (fileInput.length === undefined) {
            temp = 1;
        }
    }
}

async function myFunction() {
    await waitingFile()

    const fileInput = document.getElementById("file");
    for (const file of fileInput.files) {
        alert(file.name);
    }
}