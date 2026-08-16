from datetime import date

from core.config_loader import load_topics


# ============================================================
# 10 MIXED TOPIC GROUPS
# ============================================================
#
# Every group contains topics from different categories.
#
# Rotation:
#
#   1  -> Group 1
#   2  -> Group 2
#   ...
#   10 -> Group 10
#   11 -> Group 1
#   12 -> Group 2
#   ...
#
# The topic names below must exist in topics.json.
# ============================================================

MIXED_TOPIC_GROUPS = [

    # ========================================================
    # GROUP 1
    # ========================================================
    [
        ("AI", "AI"),
        ("Programming", "C++"),
        ("Web", "Web Development"),
        ("Cybersecurity", "Cybersecurity"),
        ("DevOps / Cloud", "DevOps"),
        ("System Design / CS", "System Design"),
        ("Blockchain", "Blockchain"),
        ("Mobile", "Android"),
        ("Game Development", "Game Development"),
        ("Developer Tools", "Git"),
    ],

    # ========================================================
    # GROUP 2
    # ========================================================
    [
        ("AI", "Machine Learning"),
        ("Programming", "Python"),
        ("Web", "Frontend"),
        ("Cybersecurity", "Ethical Hacking"),
        ("DevOps / Cloud", "Docker"),
        ("System Design / CS", "Software Architecture"),
        ("Blockchain", "Web3"),
        ("Mobile", "Flutter"),
        ("Game Development", "Unity"),
        ("Learning", "DSA"),
    ],

    # ========================================================
    # GROUP 3
    # ========================================================
    [
        ("AI", "Deep Learning"),
        ("Programming", "JavaScript"),
        ("Web", "Backend"),
        ("Cybersecurity", "Penetration Testing"),
        ("DevOps / Cloud", "Kubernetes"),
        ("System Design / CS", "Distributed Systems"),
        ("Blockchain", "Ethereum"),
        ("Mobile", "React Native"),
        ("Game Development", "Unreal Engine"),
        ("Developer Tools", "Testing"),
    ],

    # ========================================================
    # GROUP 4
    # ========================================================
    [
        ("AI", "Generative AI"),
        ("Programming", "TypeScript"),
        ("Web", "Full Stack"),
        ("Cybersecurity", "Web Security"),
        ("DevOps / Cloud", "CI/CD"),
        ("System Design / CS", "Operating Systems"),
        ("Blockchain", "Smart Contracts"),
        ("Mobile", "iOS"),
        ("Game Development", "Godot"),
        ("Learning", "Competitive Programming"),
    ],

    # ========================================================
    # GROUP 5
    # ========================================================
    [
        ("AI", "LLM"),
        ("Programming", "Go"),
        ("Web", "React"),
        ("Cybersecurity", "Application Security"),
        ("DevOps / Cloud", "Linux"),
        ("System Design / CS", "Computer Networks"),
        ("Blockchain", "DeFi"),
        ("Mobile", "Kotlin Multiplatform"),
        ("Game Development", "Game Engines"),
        ("Developer Tools", "Debugging"),
    ],

    # ========================================================
    # GROUP 6
    # ========================================================
    [
        ("AI", "AI Agents"),
        ("Programming", "Rust"),
        ("Web", "Next.js"),
        ("Cybersecurity", "Network Security"),
        ("DevOps / Cloud", "AWS"),
        ("System Design / CS", "Database Systems"),
        ("Blockchain", "Distributed Ledger"),
        ("Mobile", "Mobile Development"),
        ("Game Development", "Graphics Programming"),
        ("Learning", "Programming Tutorials"),
    ],

    # ========================================================
    # GROUP 7
    # ========================================================
    [
        ("AI", "RAG"),
        ("Programming", "Java"),
        ("Web", "Vue"),
        ("Cybersecurity", "Cloud Security"),
        ("DevOps / Cloud", "Azure"),
        ("System Design / CS", "Compilers"),
        ("Blockchain", "Blockchain"),
        ("Mobile", "Android"),
        ("Game Development", "OpenGL"),
        ("Developer Tools", "Automation"),
    ],

    # ========================================================
    # GROUP 8
    # ========================================================
    [
        ("AI", "MCP"),
        ("Programming", "C#"),
        ("Web", "Angular"),
        ("Cybersecurity", "OSINT"),
        ("DevOps / Cloud", "Google Cloud"),
        ("System Design / CS", "Algorithms"),
        ("Blockchain", "Web3"),
        ("Mobile", "Flutter"),
        ("Game Development", "Vulkan"),
        ("Learning", "CS Fundamentals"),
    ],

    # ========================================================
    # GROUP 9
    # ========================================================
    [
        ("AI", "Computer Vision"),
        ("Programming", "Kotlin"),
        ("Web", "Svelte"),
        ("Cybersecurity", "Digital Forensics"),
        ("DevOps / Cloud", "Terraform"),
        ("System Design / CS", "Data Structures"),
        ("Blockchain", "Ethereum"),
        ("Mobile", "React Native"),
        ("Game Development", "DirectX"),
        ("Developer Tools", "Developer Productivity"),
    ],

    # ========================================================
    # GROUP 10
    # ========================================================
    [
        ("AI", "NLP"),
        ("Programming", "Zig"),
        ("Web", "Node.js"),
        ("Cybersecurity", "Vulnerability Research"),
        ("DevOps / Cloud", "Observability"),
        ("System Design / CS", "Parallel Computing"),
        ("Blockchain", "Smart Contracts"),
        ("Mobile", "Mobile Development"),
        ("Game Development", "Graphics Programming"),
        ("Learning", "Interview Preparation"),
    ],
]


def _get_topic_config() -> dict:
    """
    Load topic configuration.

    Supports both:
        {"categories": {...}}

    and:
        {"AI": [...], ...}
    """

    topic_config = load_topics()

    if "categories" in topic_config:
        topic_config = topic_config["categories"]

    return topic_config


def get_daily_group_index(
    target_date: date | None = None,
) -> int:
    """
    Return zero-based daily group index.

    Calendar rotation:

        1  -> 0 -> Group 1
        2  -> 1 -> Group 2
        ...
        10 -> 9 -> Group 10
        11 -> 0 -> Group 1
    """

    if target_date is None:
        target_date = date.today()

    return (
        target_date.day - 1
    ) % len(MIXED_TOPIC_GROUPS)


def get_daily_topics(
    target_date: date | None = None,
) -> list[str]:
    """
    Return the topics that should be searched today.
    """

    topic_config = _get_topic_config()

    group_index = get_daily_group_index(
        target_date
    )

    selected_group = MIXED_TOPIC_GROUPS[
        group_index
    ]

    topics = []

    for category, topic_name in selected_group:

        category_topics = topic_config.get(
            category,
            [],
        )

        if topic_name not in category_topics:

            print(
                f"⚠️ Topic not found: "
                f"{category} -> {topic_name}"
            )

            continue

        if topic_name not in topics:
            topics.append(topic_name)

    return topics


def get_daily_topic_group_name(
    target_date: date | None = None,
) -> str:
    """
    Return the current group name.
    """

    group_index = get_daily_group_index(
        target_date
    )

    return (
        f"Mixed Topic Group "
        f"{group_index + 1}/"
        f"{len(MIXED_TOPIC_GROUPS)}"
    )


def get_daily_topic_info(
    target_date: date | None = None,
) -> dict:
    """
    Return complete information about today's
    topic rotation.
    """

    if target_date is None:
        target_date = date.today()

    group_index = get_daily_group_index(
        target_date
    )

    topics = get_daily_topics(
        target_date
    )

    return {
        "date": target_date.isoformat(),
        "day": target_date.day,
        "group": group_index + 1,
        "total_groups": len(
            MIXED_TOPIC_GROUPS
        ),
        "group_name": (
            f"Mixed Topic Group "
            f"{group_index + 1}/"
            f"{len(MIXED_TOPIC_GROUPS)}"
        ),
        "topics": topics,
    }