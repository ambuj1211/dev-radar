SYSTEM_PROMPT = """
You are a technical analyst creating a daily report
about GitHub repositories for software developers.

Use ONLY the supplied repository metadata and README.

Do NOT invent:
- features
- capabilities
- integrations
- benchmarks
- performance claims
- use cases
- installation commands

If information is not available in the supplied material,
write:

"Not specified in the repository."

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{
  "what_it_is": "string",
  "what_it_solves": "string",
  "why_developers_care": "string",
  "how_to_use_it": "string",
  "important_features": [
    "string",
    "string",
    "string"
  ]
}
"""


def build_prompt(repository: dict) -> str:
    """Build the analysis prompt for one repository."""

    return f"""
{SYSTEM_PROMPT}

Repository:
{repository.get("full_name", "Unknown")}

Description:
{repository.get("description") or "Not specified."}

Language:
{repository.get("language") or "Not specified."}

Stars:
{repository.get("stargazers_count", 0)}

Forks:
{repository.get("forks_count", 0)}

Radar Score:
{repository.get("radar_score", 0)}

README:
--------------------
{repository.get("readme", "")}
--------------------

Analyze this repository and return ONLY the required JSON.
"""