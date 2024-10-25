 
let allShows = [];
let currentSort = { column: null, direction: 'asc' };

function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

async function fetchTVShows() {
    try {
        console.log("Fetching TV shows...");
        showLoading();
        const response = await fetch('/media/get_tvshows/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Fetched data:", data);
        allShows = data.tvshows;
        displayShows(allShows);
        updateCollectionInfo(data.totalShows, data.totalSize);
    } catch (error) {
        console.error("Error fetching TV shows:", error);
        const showList = document.getElementById("show-list");
        showList.innerHTML = `<tr><td colspan="6" class="px-4 py-2 text-red-500">Error: ${error.message}. Please try again later.</td></tr>`;
    } finally {
        hideLoading();
    }
}

function updateCollectionInfo(totalShows, totalSize) {
    document.getElementById("show-count").textContent = totalShows;
    document.getElementById("total-size").textContent = totalSize;
}

function displayShows(shows) {
    const showList = document.getElementById("show-list");
    showList.innerHTML = "";

    shows.forEach((show, index) => {
        const row = document.createElement("tr");
        row.className = "border-b hover:bg-gray-50";
        row.innerHTML = `
            <td class="px-4 py-2">
                <button class="toggle-details" data-index="${index}">▼</button>
            </td>
            <td class="px-4 py-2">${show.title}</td>
            <td class="px-4 py-2">${show.year}</td>
            <td class="px-4 py-2">${show.seasons}</td>
            <td class="px-4 py-2">${show.episodes}</td>
            <td class="px-4 py-2">${show.fileSizeGB.toFixed(2)} GB</td>
        `;
        showList.appendChild(row);

        // Add a hidden row for episode details
        const detailRow = document.createElement("tr");
        detailRow.className = "hidden";
        detailRow.innerHTML = `
            <td colspan="6">
                <div class="p-4 bg-gray-100">
                    ${show.seasonDetails.map(season => `
                        <h3 class="font-bold mb-2">${season.title || `Season ${season.number}`}</h3>
                        <table class="w-full mb-4">
                            <thead>
                                <tr>
                                    <th class="px-2 py-1 text-left">Episode</th>
                                    <th class="px-2 py-1 text-left">Title</th>
                                    <th class="px-2 py-1 text-left">Size</th>
                                    <th class="px-2 py-1 text-left">Resolution</th>
                                    <th class="px-2 py-1 text-left">Video Codec</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${season.episodes.map(episode => `
                                    <tr>
                                        <td class="px-2 py-1">${episode.index}</td>
                                        <td class="px-2 py-1">${episode.title}</td>
                                        <td class="px-2 py-1">${episode.fileSizeGB} GB</td>
                                        <td class="px-2 py-1">${episode.videoResolution}</td>
                                        <td class="px-2 py-1">${episode.videoCodec}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    `).join('')}
                </div>
            </td>
        `;
        showList.appendChild(detailRow);
    });

    // Add event listeners for toggle buttons
    document.querySelectorAll('.toggle-details').forEach(button => {
        button.addEventListener('click', function() {
            const detailRow = this.closest('tr').nextElementSibling;
            detailRow.classList.toggle('hidden');
            this.textContent = detailRow.classList.contains('hidden') ? '▼' : '▲';
        });
    });
}

function searchShows() {
    const searchTerm = document.getElementById("search-input").value.toLowerCase();
    const filteredShows = allShows.filter(show => 
        show.title.toLowerCase().includes(searchTerm) ||
        show.year.toString().includes(searchTerm)
    );
    displayShows(filteredShows);
}

function sortShows(column) {
    if (currentSort.column === column) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.direction = 'asc';
    }

    allShows.sort((a, b) => {
        let valueA = a[column];
        let valueB = b[column];

        if (column === 'fileSizeGB' || column === 'year' || column === 'seasons' || column === 'episodes') {
            valueA = parseFloat(valueA);
            valueB = parseFloat(valueB);
        } else {
            valueA = valueA.toString().toLowerCase();
            valueB = valueB.toString().toLowerCase();
        }

        if (valueA < valueB) return currentSort.direction === 'asc' ? -1 : 1;
        if (valueA > valueB) return currentSort.direction === 'asc' ? 1 : -1;
        return 0;
    });

    displayShows(allShows);
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

async function updateTVShows() {
    try {
        console.log("Updating TV shows...");
        showLoading();
        const response = await fetch('/media/update_tvshows/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Update response:", data);
        
        // Update the TV show list with the new data
        allShows = data.tvshows;
        displayShows(allShows);
        updateCollectionInfo(data.totalShows, data.totalSize);
    } catch (error) {
        console.error("Error updating TV shows:", error);
        alert(`Error updating TV shows: ${error.message}. Please try again later.`);
    } finally {
        hideLoading();
    }
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
    fetchTVShows();

    // Add event listeners for sorting
    document.querySelectorAll('.sort-header').forEach(header => {
        header.addEventListener('click', () => sortShows(header.dataset.sort));
    });

    // Add event listener for search input
    document.getElementById("search-input").addEventListener("input", searchShows);

    // Add event listener for update TV shows button
    const updateTVShowsButton = document.getElementById('update-tvshows');
    if (updateTVShowsButton) {
        updateTVShowsButton.addEventListener('click', updateTVShows);
    }
});