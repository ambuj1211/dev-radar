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

const searchInput =
    document.getElementById("search-input");

const sortFilter =
    document.getElementById("sort-filter");

function renderRepositories(
    language = "all",
    search = "",
    sort = "score"
) {

    const searchTerm =
        search.trim().toLowerCase();

    let filtered = repositories.filter(
        repository => {

            const matchesLanguage =
                language === "all" ||
                repository.language === language;

            const searchableText = [
                repository.full_name,
                repository.description,
                repository.language
            ]
                .filter(Boolean)
                .join(" ")
                .toLowerCase();

            const matchesSearch =
                !searchTerm ||
                searchableText.includes(searchTerm);

            return (
                matchesLanguage &&
                matchesSearch
            );
        }
    );

    filtered.sort((a, b) => {

        if (sort === "stars") {
            return (
                (b.stargazers_count || 0) -
                (a.stargazers_count || 0)
            );
        }

        if (sort === "growth") {
            return (
                (b.star_change || 0) -
                (a.star_change || 0)
            );
        }

        if (sort === "new") {
            return (
                (b.change_type === "new") -
                (a.change_type === "new")
            );
        }

        return (
            (b.radar_score || 0) -
            (a.radar_score || 0)
        );
    });

    repositoryList.innerHTML = "";

    filtered.forEach(
        (repository, index) => {

            const card =
                document.createElement("article");

            card.className =
                "repository-card";

            card.innerHTML = `
                <div class="rank">
                    #${index + 1}
                </div>

                <div class="card-header">

                    <h3>
                        ${repository.full_name}
                    </h3>

                    <div class="score">
                        ${Number(
                            repository.radar_score || 0
                        ).toFixed(1)}
                    </div>

                </div>

                <p class="description">
                    ${repository.description ||
                            "No description available."
                            }
                </p>

                <div class="score-breakdown">

                    <div class="score-row">
                        <span>⭐ Popularity</span>

                        <div class="score-bar">
                            <div
                                class="score-fill"
                                style="width: ${repository.score_breakdown?.popularity || 0
                            }%"
                            ></div>
                        </div>

                        <span>
                            ${Number(
                                repository.score_breakdown?.popularity || 0
                            ).toFixed(0)
                            }
                        </span>
                    </div>
                        

                    <div class="score-row">
                        <span>⚡ Freshness</span>

                        <div class="score-bar">
                            <div
                                class="score-fill"
                                style="width: ${repository.score_breakdown?.freshness || 0
                            }%"
                            ></div>
                        </div>

                        <span>
                            ${Number(
                                repository.score_breakdown?.freshness || 0
                            ).toFixed(0)
                            }
                        </span>
                    </div>
                        

                    <div class="score-row">
                        <span>👥 Community</span>

                        <div class="score-bar">
                            <div
                                class="score-fill"
                                style="width: ${repository.score_breakdown?.community || 0
                            }%"
                            ></div>
                        </div>

                        <span>
                            ${Number(
                                repository.score_breakdown?.community || 0
                            ).toFixed(0)
                            }
                        </span>
                    </div>

                </div>
                        

                <div class="metrics">

                    <span>
                        ⭐ ${Number(
                                repository.stargazers_count || 0
                            ).toLocaleString()
                            }
                    </span>

                    <span>
                        🍴 ${Number(
                                repository.forks_count || 0
                            ).toLocaleString()
                            }
                    </span>

                    <span>
                        📈 ${Number(
                                repository.star_change || 0
                            ).toLocaleString()
                            }
                    </span>

                    <span>
                        📝 ${repository.language ||
                            "Unknown"
                            }
                    </span>

                </div>
                        

                <div class="card-footer">

                    <span class="change ${repository.change_type || "unknown"
                            }">
                        ${repository.change_type ||
                            "unknown"
                            }
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
        }
    );
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


searchInput.addEventListener(
    "input",
    () => {
        renderRepositories(
            languageFilter.value,
            searchInput.value,
            sortFilter.value
        );
    }
);

sortFilter.addEventListener(
    "change",
    () => {
        renderRepositories(
            languageFilter.value,
            searchInput.value,
            sortFilter.value
        );
    }
);


async function loadRadar() {

    try {

        const response =
            await fetch(
                `${import.meta.env.BASE_URL}data/radar.json`
            )

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