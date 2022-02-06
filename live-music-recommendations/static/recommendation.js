form = document.getElementById('form');
form.addEventListener('submit', (e) => {
    console.log(e.target.getAttribute('action'))
    if (!e.target.getAttribute('action')) {
        e.preventDefault();
        displayError()
    }
}, true)

playlistButton = document.getElementById('playlist');
playlistButton.addEventListener('click', buttonPressed);

artistButton = document.getElementById('artist');
artistButton.addEventListener('click', buttonPressed);

genreButton = document.getElementById('genre');
genreButton.addEventListener('click', buttonPressed);

selectionInput = document.getElementById('selection');

function buttonPressed(e) {
    selection = e.target.innerText.toLowerCase()
    selectionInput.setAttribute('value', selection)
    form.setAttribute('action', `/${selection}`)
}

function displayError() {
    // TODO
    console.log('make selection')
}