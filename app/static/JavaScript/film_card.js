document.addEventListener('DOMContentLoaded', function() {
    const sessionButtons = document.querySelectorAll('.session-button');

    sessionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sessionId = this.dataset.sessionId;
            window.location.href = '/';
        });
    });
});