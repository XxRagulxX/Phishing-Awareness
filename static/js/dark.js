// theme.js

function toggleTheme() {
    const body = document.body;
    const form = document.querySelector('.container'); // Use the container class

    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        form.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light'); // Save the theme preference in local storage
    } else {
        body.classList.add('dark-theme');
        form.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark'); // Save the theme preference in local storage
    }
}
