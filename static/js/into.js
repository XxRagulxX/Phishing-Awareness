document.getElementById('intro-form').addEventListener('submit', function (event) {
    event.preventDefault();
    document.getElementById('intro').style.animation = 'fadeOut 1s';
    setTimeout(function () {
        window.location.href = "/questions/0";
    }, 1000);
});

// Check for theme preference in local storage
const savedTheme = localStorage.getItem('theme');
const body = document.body;
const form = document.querySelector('form');

if (savedTheme === 'dark') {
    body.classList.add('dark-theme');
    form.classList.add('dark-theme');
}

function toggleTheme() {
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        form.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light'); // Save the preference
    } else {
        body.classList.add('dark-theme');
        form.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark'); // Save the preference
    }
}
