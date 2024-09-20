window.addEventListener('load', function() {
    setTimeout(function() {
        document.body.classList.remove('loading');
        document.documentElement.classList.remove('loading');
        document.body.classList.add('loaded');
        document.documentElement.classList.add('loaded');
        document.getElementById('loading').style.display = 'none';
    }, 900);
});

document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('loading');
    document.documentElement.classList.add('loading');
    let links = document.querySelectorAll('a');
    links.forEach(function(link) {
        link.addEventListener('click', function() {
            document.getElementById('loading').style.display = 'flex';
            document.getElementById('content').style.display = 'none';
        });
    });
});