function openModal(imgSrc) {
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("img01");
    modal.style.display = "block";
    modalImg.src = imgSrc;
    modalImg.style.width = "100%";
    modalImg.style.height = "auto";

    // Close the modal if clicked outside the image
    modal.onclick = function (event) {
        if (event.target === modal) {
            closeModal();
        }
    };
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

function toggleTheme() {
    var body = document.body;
    var form = document.querySelector('form');

    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        form.classList.remove('dark-theme');
    } else {
        body.classList.add('dark-theme');
        form.classList.add('dark-theme');
    }
}

function submitForm() {
    document.querySelector('form').submit();
}