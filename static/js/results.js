function toggleTheme() {
    var body = document.body;

    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
    } else {
        body.classList.add('dark-theme');
    }
}
