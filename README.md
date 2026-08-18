# 🚀 Dev Radar

> **Discover 3 valuable GitHub repositories every day — automatically.**

Dev Radar is an automated developer-discovery system that searches GitHub, analyzes repositories, filters out repositories that have already been reported, ranks the best candidates, and generates a daily **Top 3 Developer Repository Radar**.

The goal is simple:

**Instead of spending time searching GitHub every day, let Dev Radar find genuinely useful projects for you.**

---

## ✨ What Dev Radar Does

Every day, Dev Radar:

1. 🔎 Discovers GitHub repositories across multiple developer-focused topics
2. 📊 Collects repository information such as stars, forks, language, activity, contributors, etc.
3. 🔍 Filters repositories based on configurable criteria
4. 🧠 Detects changes and repository activity
5. 🏆 Calculates a **Radar Score**
6. ♻️ Removes repositories that have already been reported
7. 🎯 Selects exactly **3 new repositories**
8. 📖 Downloads and preprocesses their README files
9. 🤖 Prepares data for the AI analysis worker
10. 📄 Generates a daily report
11. 🌐 Generates JSON data for the web dashboard
12. 🤖 Runs automatically using GitHub Actions

The current implementation selects three new repositories using the configured discovery, filtering, ranking, and history pipeline.

---

## 🎯 Why Dev Radar?

There are thousands of new and updated GitHub repositories every day.

Finding useful projects manually requires constantly checking:

* GitHub Trending
* GitHub Search
* AI repositories
* Developer tools
* Open-source projects
* Cloud/DevOps projects
* Security projects
* Programming frameworks
* Learning resources

Dev Radar turns this into an automated daily feed.

### Instead of:

```text
Search GitHub
     ↓
Open repositories
     ↓
Read README
     ↓
Compare projects
     ↓
Remember what you saw yesterday
     ↓
Repeat tomorrow
```

### Dev Radar does:

```text
                 GitHub
                    │
                    ▼
             🔎 Discovery
                    │
                    ▼
             🔍 Filtering
                    │
                    ▼
             📊 Enrichment
                    │
                    ▼
              🏆 Ranking
                    │
                    ▼
          ♻️ History / Changes
                    │
                    ▼
             🎯 Top 3 New
                    │
                    ▼
             📖 README Data
                    │
                    ▼
              🤖 AI Worker
                    │
                    ▼
             📄 Daily Report
                    │
                    ▼
              🌐 Web Dashboard
```

---

# 🌟 Key Features

| Feature                  | Description                                                         |
| ------------------------ | ------------------------------------------------------------------- |
| 🔎 GitHub Discovery      | Searches GitHub for relevant repositories                           |
| 🏷️ Topic Based Search   | Searches across AI, Web, Programming, DevOps, Security and more     |
| ⭐ Popularity Filtering   | Filters repositories using configurable star thresholds             |
| 🕐 Freshness Filtering   | Can filter repositories based on age/activity                       |
| 📊 Repository Enrichment | Collects additional repository information                          |
| 🏆 Radar Score           | Ranks repositories using multiple signals                           |
| ♻️ History Tracking      | Prevents previously reported repositories from being selected again |
| 🔥 Change Detection      | Detects repository changes over time                                |
| 🎯 Daily Top 3           | Selects three new repositories                                      |
| 📖 README Processing     | Downloads and preprocesses repository README files                  |
| 🤖 AI Pipeline           | Prepares repository information for AI analysis                     |
| 📄 Markdown Reports      | Generates daily reports                                             |
| 🌐 JSON API/Data         | Generates JSON for the web frontend                                 |
| ⚙️ GitHub Actions        | Supports fully automated daily execution                            |
| 🧪 Automated Tests       | Runs tests before the radar pipeline                                |
| 🖥️ Web Dashboard        | Provides a frontend for viewing radar results                       |

---

# 🧠 How the Ranking Works

Dev Radar does not simply select the repositories with the highest number of stars.

Repositories are processed through a ranking pipeline that considers signals such as:

* ⭐ Popularity
* 🕐 Freshness
* 👥 Community activity
* 📈 Repository changes
* 🍴 Forks
* 👨‍💻 Contributors
* 📊 Overall repository quality

The system exposes a score breakdown including:

```text
Popularity
Freshness
Community
```

The final ranking is then used to select new repositories.

---

# 🗂️ Supported Topics

Topics are configured in:

```text
config/topics.json
```

The current configuration includes categories such as:

### 🤖 AI

* Artificial Intelligence
* Machine Learning
* Deep Learning
* Generative AI
* LLM
* AI Agents
* RAG
* MCP
* Computer Vision
* NLP
* Multimodal AI
* MLOps
* AI Infrastructure
* AI Developer Tools

### 💻 Programming

* C
* C++
* C#
* Java
* Python
* JavaScript
* TypeScript
* Go
* Rust
* Kotlin
* Swift
* PHP
* Ruby
* Dart
* R
* Zig

### 🌐 Web Development

* Frontend
* Backend
* Full Stack
* React
* Next.js
* Vue
* Angular
* Svelte
* Node.js
* APIs
* Web Performance

### 🔐 Cybersecurity

* Cybersecurity
* Ethical Hacking
* Penetration Testing
* Web Security
* Application Security
* Network Security
* Cloud Security
* OSINT
* Digital Forensics
* Vulnerability Research
* Cryptography
* Privacy
* DevSecOps

### ☁️ DevOps / Cloud

* DevOps
* Docker
* Kubernetes
* CI/CD
* Linux
* AWS
* Azure
* Google Cloud
* Terraform
* Infrastructure as Code
* Monitoring
* Observability

### 🧩 System Design / CS

* System Design
* Software Architecture
* Distributed Systems
* Operating Systems
* Computer Networks
* Database Systems
* Compilers
* Algorithms
* Data Structures
* Parallel Computing

Additional categories include:

* Blockchain
* Mobile Development
* Game Development
* Developer Tools
* Learning

You can customize these topics yourself by editing:

```text
config/topics.json
```

---

# 🏗️ Project Structure

```text
dev-radar/
│
├── .github/
│   └── workflows/
│       ├── daily-radar.yml
│       ├── deploy-pages.yml
│       └── test-radar.yml
│
├── config/
│   ├── defaults.json
│   └── topics.json
│
├── core/
│   ├── ai/
│   ├── discovery/
│   ├── filtering/
│   ├── history/
│   ├── ranking/
│   └── reports/
│
├── data/
│
├── kaggle-worker/
│
├── scripts/
│
├── tests/
│
├── web/
│   └── ...
│
├── main.py
├── requirements.txt
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

# ⚙️ Requirements

## Software

You should have the following installed:

* Python **3.13+** recommended
* Git
* pip
* A GitHub account

The GitHub Actions workflow currently uses Python **3.13**.

Check your versions:

```bash
python --version
pip --version
git --version
```

---

# 📥 Installation

## 1. Clone the repository

```bash
git clone https://github.com/ambuj1211/dev-radar.git
```

Move into the project:

```bash
cd dev-radar
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
```

Then:

```bash
pip install -r requirements.txt
```

---

# 🔐 Credentials

Dev Radar is designed so that **you provide your own credentials**.

Never put API keys directly into Python files.

Never commit secrets to GitHub.

Use environment variables locally and **GitHub Actions Secrets** for automated execution.

---

# 🐙 GitHub Token

## Is a GitHub token required?

The project supports the `GITHUB_TOKEN` environment variable.

The GitHub API code checks for:

```text
GITHUB_TOKEN
```

and, if available, sends it as a Bearer token.

For local development, using your own GitHub token is recommended because authenticated API requests provide better API limits than anonymous requests.

---

## Create a GitHub Personal Access Token

Go to your GitHub account:

**Settings → Developer settings → Personal access tokens**

Create a token appropriate for your use case.

For the public-repository discovery performed by Dev Radar, avoid granting unnecessary permissions.

### Recommended principle

> Give the token the minimum permissions required.

You do not need to put the token inside the source code.

---

# 🖥️ Set GitHub Token Locally

Create a file:

```text
.env
```

in the root of the project:

```text
dev-radar/
├── .env
├── main.py
├── requirements.txt
└── ...
```

Add:

```env
GITHUB_TOKEN=your_github_token_here
```

The GitHub discovery module loads environment variables using `python-dotenv`.

### Example

```env
GITHUB_TOKEN=github_pat_xxxxxxxxxxxxxxxxxxxx
```

---

# 🚨 IMPORTANT: Never Commit `.env`

Make sure `.gitignore` contains:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

Never commit:

```text
.env
```

to GitHub.

If you accidentally expose an API token:

1. Revoke the token immediately.
2. Generate a new token.
3. Remove the secret from your repository history if necessary.

---

# 🤖 GitHub Actions Credentials

If you want Dev Radar to run automatically through GitHub Actions, you normally do **not** need to manually create a GitHub token for the workflow's basic GitHub API access.

The workflow already exposes GitHub's built-in:

```text
GITHUB_TOKEN
```

to the Python application.

The workflow currently contains:

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

This token is provided by GitHub Actions.

---

# 🔑 GitHub Actions Secrets

If you add additional external services in the future, store their credentials here:

```text
GitHub Repository
        ↓
Settings
        ↓
Secrets and variables
        ↓
Actions
        ↓
New repository secret
```

For example:

```text
GITHUB_TOKEN
KAGGLE_USERNAME
KAGGLE_KEY
EMAIL_USERNAME
EMAIL_PASSWORD
OPENAI_API_KEY
GEMINI_API_KEY
```

Only add the credentials required by the features you actually enable.

---

# 🤖 Kaggle AI Worker

Dev Radar prepares an input file for the Kaggle Qwen worker:

```text
kaggle-worker/input/daily_input.json
```

The Python pipeline creates this file from the three selected repositories.

The generated data contains information such as:

```json
{
  "date": "YYYY-MM-DD",
  "repositories": [
    {
      "full_name": "owner/repository",
      "description": "...",
      "language": "Python",
      "stargazers_count": 12345,
      "forks_count": 1234,
      "radar_score": 87.5,
      "readme": "..."
    }
  ]
}
```

This allows the AI worker to analyze the selected repositories without the main GitHub discovery process having to perform the AI analysis itself.

---

# 🧠 AI Credentials

If you use the project's AI/Kaggle worker, configure the credentials required by the worker in the **worker environment**, rather than hard-coding them into the repository.

For any AI provider you configure, use environment variables such as:

```env
OPENAI_API_KEY=your_key
```

or:

```env
GEMINI_API_KEY=your_key
```

or the corresponding credentials required by your selected AI/Kaggle setup.

> **Do not commit AI API keys to this repository.**

---

# ▶️ Run Dev Radar Locally

After installation and credential setup:

```bash
python main.py
```

The application will:

```text
1. Load configured topics
2. Discover repositories
3. Filter repositories
4. Enrich repository information
5. Rank repositories
6. Detect changes
7. Remove previously selected repositories
8. Select up to 3 new repositories
9. Download repository READMEs
10. Prepare AI/Kaggle input
11. Generate reports
```

The main pipeline currently uses:

```text
Minimum stars: 1000
Maximum age: 180 days
Repositories per topic: 10
Final repositories: 3
```

These values are currently passed from `main.py` and can be customized there or moved into configuration as the project evolves.

---

# 🧪 Run Tests

Run:

```bash
pytest -v
```

GitHub Actions also runs the test suite before executing the radar pipeline.

---

# ⚡ Automatic Daily Execution

Dev Radar includes:

```text
.github/workflows/daily-radar.yml
```

The workflow:

```text
GitHub Actions
      ↓
Checkout repository
      ↓
Setup Python 3.13
      ↓
Install dependencies
      ↓
Run tests
      ↓
Run main.py
      ↓
Generate radar data
      ↓
Commit updated radar.json
      ↓
Push changes
```

The current workflow is scheduled using:

```yaml
cron: "0 6 * * *"
```

GitHub Actions cron schedules are in **UTC**.

Therefore:

```text
06:00 UTC
=
11:30 AM IST
```

If you want the workflow to run at a different time, modify the cron expression in:

```text
.github/workflows/daily-radar.yml
```

The workflow also supports manual execution using:

```text
workflow_dispatch
```

so you can run it manually from the GitHub Actions interface.

---

# 🖱️ Run the Workflow Manually

Go to:

```text
GitHub Repository
        ↓
Actions
        ↓
Daily Dev Radar
        ↓
Run workflow
```

This is useful when testing changes without waiting for the scheduled execution.

---

# 🌐 Web Dashboard

Dev Radar also contains a web frontend:

```text
web/
```

The generated radar data is written to:

```text
web/public/data/radar.json
```

The GitHub Actions workflow commits this generated data back into the repository after a successful run.

This makes it possible to deploy the dashboard separately using GitHub Pages or another static hosting service.

---

# ⚙️ Customization

## Change Topics

Edit:

```text
config/topics.json
```

For example:

```json
{
  "categories": {
    "My Topics": [
      "Python",
      "FastAPI",
      "Machine Learning",
      "LLM"
    ]
  }
}
```

---

## Change Minimum Stars

In `main.py`:

```python
results = run_daily_radar(
    min_stars=1000,
    max_age_days=180,
    per_topic=10,
)
```

Change:

```python
min_stars=1000
```

to something like:

```python
min_stars=500
```

---

## Change Repository Freshness

Change:

```python
max_age_days=180
```

For example:

```python
max_age_days=365
```

---

## Change Number of Candidates

Change:

```python
per_topic=10
```

to:

```python
per_topic=20
```

This increases the candidate pool before ranking.

---

# ♻️ Repository History

One of the most important features of Dev Radar is its history system.

The goal is to prevent this:

```text
Monday
→ project-A
→ project-B
→ project-C

Tuesday
→ project-A ❌
→ project-B ❌
→ project-C ❌
```

Instead:

```text
Monday
→ project-A
→ project-B
→ project-C

Tuesday
→ project-D
→ project-E
→ project-F
```

The selection pipeline explicitly calls the history system to select new repositories.

This allows Dev Radar to become a long-running discovery system rather than a daily duplicate GitHub search.

---

# 📊 Example Daily Output

A typical radar result contains information such as:

```text
============================================================
🚀 DEV RADAR
============================================================

#1 owner/project-one

Radar Score : 92.50
⭐ Stars     : 48,200
⭐ Change    : +1,250
🍴 Forks     : 4,300
📝 Language  : Python
Change       : growing
Score Δ      : +4.20

Score Breakdown:
    Popularity : 35.00
    Freshness  : 30.00
    Community  : 27.50

🔗 URL:
https://github.com/owner/project-one
```

The application also generates machine-readable JSON for the web dashboard.

---

# 🛡️ Security Best Practices

### Never do this

```python
GITHUB_TOKEN = "github_pat_123456789"
```

### Do this instead

```python
import os

token = os.getenv("GITHUB_TOKEN")
```

And store the value in:

```text
.env
```

locally, or:

```text
GitHub Actions Secrets
```

for automation.

---

# 🔒 Credential Summary

| Credential                    |                             Required? | Where to configure                       |
| ----------------------------- | ------------------------------------: | ---------------------------------------- |
| GitHub account                |                                     ✅ | GitHub                                   |
| `GITHUB_TOKEN`                |                   Recommended locally | `.env`                                   |
| GitHub Actions `GITHUB_TOKEN` |                        ✅ for workflow | Automatically provided by GitHub Actions |
| Kaggle credentials            |           Only if using Kaggle worker | Kaggle / Actions Secrets                 |
| AI API key                    | Only if using an external AI provider | `.env` / Actions Secrets                 |
| Email credentials             |     Only if email delivery is enabled | `.env` / Actions Secrets                 |

**Never share these credentials publicly.**

---

# 🧑‍💻 For Other Developers

Anyone can create their own Dev Radar instance.

The recommended setup is:

```text
1. Fork the repository
        ↓
2. Clone your fork
        ↓
3. Create Python environment
        ↓
4. Install requirements
        ↓
5. Create .env
        ↓
6. Add your own GitHub token
        ↓
7. Customize topics
        ↓
8. Run tests
        ↓
9. Run main.py
        ↓
10. Enable GitHub Actions
```

Each user should use **their own credentials**.

You should never use the original author's credentials.

---

# 🍴 Fork Dev Radar

Open the repository:

https://github.com/ambuj1211/dev-radar

Click:

```text
Fork
```

Then clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/dev-radar.git
cd dev-radar
```

Replace:

```text
YOUR_USERNAME
```

with your GitHub username.

---

# 🔧 First-Time Setup

```bash
git clone https://github.com/YOUR_USERNAME/dev-radar.git

cd dev-radar

python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
.env
```

Add:

```env
GITHUB_TOKEN=your_github_token
```

Then run:

```bash
pytest -v
```

and:

```bash
python main.py
```

---

# 🤖 Enable Your Own Daily Automation

After forking the repository:

```text
Your GitHub Repository
        ↓
Actions
        ↓
Enable workflows
```

The included workflow can then execute the radar automatically according to its configured schedule.

The workflow has write permission for repository contents because it commits the generated radar data back to the repository.

---

# 🧩 Custom Instance

You can make Dev Radar your own by changing:

```text
Topics
   ↓
Minimum stars
   ↓
Repository age
   ↓
Ranking weights
   ↓
Number of candidates
   ↓
AI analysis
   ↓
Report format
   ↓
Web dashboard
```

For example, a user interested only in AI could configure:

```text
AI
LLM
RAG
AI Agents
MCP
Computer Vision
Generative AI
```

Another user could create a cybersecurity-only radar:

```text
Cybersecurity
OSINT
Digital Forensics
Web Security
Cloud Security
Cryptography
```

---

# 🧪 Development

Install development dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest -v
```

Run the application:

```bash
python main.py
```

Before submitting a pull request, make sure:

```text
✓ Tests pass
✓ No secrets are committed
✓ New functionality is documented
✓ Existing functionality is not broken
```

---

# 🤝 Contributing

Contributions are welcome!

You can contribute by:

* Adding new discovery sources
* Improving repository ranking
* Improving filtering
* Adding new topic categories
* Improving AI analysis
* Improving the dashboard
* Adding tests
* Improving documentation
* Fixing bugs
* Adding notification channels

Please read:

```text
CONTRIBUTING.md
```

before submitting a pull request.

---

# 🗺️ Roadmap

Potential future improvements include:

* 📧 Daily email delivery
* 📱 Telegram notifications
* 💬 Discord notifications
* 🔔 Slack notifications
* 🤖 Better AI-generated repository analysis
* 📈 Historical repository analytics
* 🔥 Trending detection
* 🧠 Personalized recommendations
* 🎯 User-specific topic preferences
* 📊 Advanced ranking models
* 🔍 Multiple discovery sources
* 🌐 Improved web dashboard
* 👤 Multiple-user support
* ⭐ Personal repository bookmarking
* 📅 Weekly and monthly developer digests

---

# 🛠️ Tech Stack

```text
Python
   │
   ├── GitHub API
   │
   ├── Repository Discovery
   │
   ├── Filtering
   │
   ├── Ranking
   │
   ├── History Tracking
   │
   ├── README Processing
   │
   └── Report Generation
          │
          ▼
     GitHub Actions
          │
          ▼
      Web Dashboard
```

Core implementation is Python-based, with GitHub Actions handling automated execution.

---

# 📄 License

This project is licensed under the **MIT License**.

See:

```text
LICENSE
```

for details.

---

# ⭐ Support the Project

If you find Dev Radar useful:

⭐ **Star the repository**

🍴 **Fork it**

🐛 **Report issues**

💡 **Suggest improvements**

🤝 **Contribute**

Repository:

https://github.com/ambuj1211/dev-radar

---

# 👨‍💻 Author

**Brilliant Ambuj**

Built with ❤️ for developers who want to discover useful open-source projects without spending hours searching GitHub.

---

## 🚀 Start Your Own Dev Radar

```bash
git clone https://github.com/YOUR_USERNAME/dev-radar.git

cd dev-radar

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt

# Create .env and add:
# GITHUB_TOKEN=your_github_token

pytest -v

python main.py
```

### Your personal developer radar is now ready. 🚀
