let allMovies = [];
let currentSort = { column: null, direction: 'asc' };

function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

async function fetchMovies() {
    try {
        console.log("Fetching movies...");
        showLoading();
        const response = await fetch('/media/get_movies/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Fetched data:", data);
        allMovies = data.movies;
        displayMovies(allMovies);
        updateCollectionInfo(data.totalMovies, data.totalSize);
    } catch (error) {
        console.error("Error fetching movies:", error);
        const movieList = document.getElementById("movie-list");
        movieList.innerHTML = `<tr><td colspan="8" class="px-4 py-2 text-red-500">Error: ${error.message}. Please try again later.</td></tr>`;
    } finally {
        hideLoading();
    }
}

function updateCollectionInfo(totalMovies, totalSize) {
    document.getElementById("movie-count").textContent = totalMovies;
    document.getElementById("total-size").textContent = totalSize;
}

function displayMovies(movies) {
    const movieList = document.getElementById("movie-list");
    movieList.innerHTML = "";

    movies.forEach(movie => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td class="px-4 py-2">${movie.title}</td>
            <td class="px-4 py-2">${movie.year}</td>
            <td class="px-4 py-2">${movie.durationFormatted}</td>
            <td class="px-4 py-2">${movie.fileSizeGB.toFixed(2)} GB</td>
            <td class="px-4 py-2">${movie.videoResolution}</td>
            <td class="px-4 py-2">${movie.dimensions}</td>
            <td class="px-4 py-2">${movie.videoCodec}</td>
            <td class="px-4 py-2">${formatAudioStreams(movie.audioStreams)}</td>
        `;
        movieList.appendChild(row);
    });
}

function formatAudioStreams(audioStreams) {
    return audioStreams.map(stream => 
        `${stream.language} (${stream.codec} ${stream.channels}ch)`
    ).join(', ');
}

function searchMovies() {
    const searchTerm = document.getElementById("search-input").value.toLowerCase();
    const filteredMovies = allMovies.filter(movie => 
        movie.title.toLowerCase().includes(searchTerm) ||
        movie.year.toString().includes(searchTerm) ||
        movie.videoResolution.toLowerCase().includes(searchTerm) ||
        movie.videoCodec.toLowerCase().includes(searchTerm)
    );
    displayMovies(filteredMovies);
}

function sortMovies(column) {
    if (currentSort.column === column) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.direction = 'asc';
    }

    allMovies.sort((a, b) => {
        let valueA = a[column];
        let valueB = b[column];

        if (column === 'fileSizeGB') {
            valueA = parseFloat(valueA);
            valueB = parseFloat(valueB);
        } else if (column === 'year' || column === 'duration') {
            valueA = parseInt(valueA);
            valueB = parseInt(valueB);
        } else {
            valueA = valueA.toString().toLowerCase();
            valueB = valueB.toString().toLowerCase();
        }

        if (valueA < valueB) return currentSort.direction === 'asc' ? -1 : 1;
        if (valueA > valueB) return currentSort.direction === 'asc' ? 1 : -1;
        return 0;
    });

    displayMovies(allMovies);
    updateSortIndicators();
}

function updateSortIndicators() {
    document.querySelectorAll('.sort-header').forEach(header => {
        const sortIcon = header.querySelector('.sort-icon');
        if (header.dataset.sort === currentSort.column) {
            sortIcon.textContent = currentSort.direction === 'asc' ? '▲' : '▼';
            sortIcon.classList.remove('hidden');
        } else {
            sortIcon.classList.add('hidden');
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    fetchMovies();

    // Add event listeners for sorting
    document.querySelectorAll('.sort-header').forEach(header => {
        header.addEventListener('click', () => sortMovies(header.dataset.sort));
    });

    // Add event listener for search input
    document.getElementById("search-input").addEventListener("input", searchMovies);
});
