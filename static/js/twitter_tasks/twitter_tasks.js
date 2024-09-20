document.getElementById('taskForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const hashtag = document.getElementById('hashtag').value;

    fetch('/check_and_register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, hashtag: hashtag })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Обработка ответа
    });
});