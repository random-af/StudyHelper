function deleteTheme(themeId) {
    fetch('/delete-theme', {
        method: 'POST',
        body: JSON.stringify({themeId: themeId})
    }).then((_res) => {
        window.location.href = '/';
    });
}
