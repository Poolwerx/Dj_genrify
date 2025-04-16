// Функция для раскрытия списка жанров
function toggleGenres(event, element) {
    event.stopPropagation(); // Останавливаем всплытие, чтобы не срабатывал клик на треке
    let moreGenres = element.querySelector('.more-genres');
    if (moreGenres.style.display === "none") {
        moreGenres.style.display = "inline";
    } else {
        moreGenres.style.display = "none";
    }
}

// Функция для раскрытия/скрытия информации о треке
function toggleDetails(trackItem) {
    let details = trackItem.querySelector('.track-details');
    if (details.style.display === "none" || details.style.display === "") {
        details.style.display = "block";
    } else {
        details.style.display = "none";
    }
}


function filterTracks() {
    let selectedGenre = document.getElementById('genre-filter').value.toLowerCase().trim();
    let tracks = document.querySelectorAll('.track-item');

    tracks.forEach(track => {
        let genres = track.getAttribute('data-genres')
            .split(',')
            .map(g => g.trim().toLowerCase()); // Фикс пробелов

        console.log(`Трек: ${track.querySelector('span').textContent}, Жанры: [${genres.join(' | ')}], Фильтр: ${selectedGenre}`);

        let found = false;
        for (let i = 0; i < genres.length; i++) {
            if (genres[i] === selectedGenre) {
                found = true;
                break;
            }
        }

        track.style.display = found || selectedGenre === 'all' ? '' : 'none';
    });
}

