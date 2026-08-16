let repositories = [];

const repositoryList =
    document.getElementById("repository-list");

const repoCount =
    document.getElementById("repo-count");

const topScore =
    document.getElementById("top-score");

const newCount =
    document.getElementById("new-count");

const languageFilter =
    document.getElementById("language-filter");


function renderRepositories(language = "all") {

    const filtered = repositories.filter(
        repository =>
            language === "all" ||
            repository.language === language
    );

    repositoryList.innerHTML = "";

    filtered.forEach((repository, index) => {

        const card = document.createElement("article");

        card.className = "repository-card";

        card.innerHTML = `
            <div class="rank">
                #${index + 1}
            </div>

            <div class="card-header">
                <h3>${repository.full_name}</h3>

                <span class="score">
                    ${Number(repository.radar_score || 0).toFixed(1)}
                </span>
            </div>

            <p class="description">
                ${repository.description || "No description available."}
            </p>

            <div class="metrics">
                <span>
                    ⭐ ${Number(
                        repository.stargazers_count || 0
                    ).toLocaleString()}
                </span>

                <span>
                    🍴 ${Number(
                        repository.forks_count || 0
                    ).toLocaleString()}
                </span>

                <span>
                    📝 ${repository.language || "Unknown"}
                </span>
            </div>

            <div class="card-footer">

                <span class="change ${repository.change_type || "unknown"}">
                    ${repository.change_type || "unknown"}
                </span>

                <a
                    href="${repository.html_url}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    View Repository →
                </a>

            </div>
        `;

        repositoryList.appendChild(card);
    });
}


function updateStats() {

    repoCount.textContent =
        repositories.length;

    topScore.textContent =
        repositories.length > 0
            ? Number(
                repositories[0].radar_score || 0
            ).toFixed(1)
            : "0";

    newCount.textContent =
        repositories.filter(
            repository =>
                repository.change_type === "new"
        ).length;
}


languageFilter.addEventListener(
    "change",
    event => {
        renderRepositories(
            event.target.value
        );
    }
);


async function loadRadar() {

    try {

        const response =
            await fetch("/data/radar.json");

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data =
            await response.json();

        repositories =
            data.repositories || [];

        updateStats();
        renderRepositories();

    } catch (error) {

        console.error(
            "Failed to load radar data:",
            error
        );

        repositoryList.innerHTML = `
            <p>
                Unable to load radar data.
                Run <code>python main.py</code>
                first.
            </p>
        `;
    }
}


loadRadar();