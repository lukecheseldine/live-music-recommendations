playlistButton = document.getElementById('playlist');
playlistButton.addEventListener('click', buttonPressed);

artistButton = document.getElementById('artist');
artistButton.addEventListener('click', buttonPressed);

genreButton = document.getElementById('genre');
genreButton.addEventListener('click', buttonPressed);

selectionInput = document.getElementById('selection');

function buttonPressed(e) {
    selection = e.target.innerText
    selectionInput.setAttribute('value', selection)
}