function submitComment() {
    const comment = document.getElementById('comment-box').value;
    fetch('/submit_comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ comment }),
    })
        .then((response) => response.json())
        .then((data) => {
            document.getElementById('comments-list').innerHTML = data.comments_html;
        })
        .catch((error) => console.error('Error:', error));
}
