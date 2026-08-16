import json
import re
from pathlib import Path

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)


MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"

OUTPUT_FILE = Path(
    "/kaggle/working/ai_analysis.json"
)


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


def load_input() -> dict:
    """Locate and load the daily Dev Radar input."""

    expected = Path(
        "/kaggle/input/dev-radar-input/daily_input.json"
    )

    if expected.exists():
        input_file = expected

    else:
        input_files = list(
            Path("/kaggle/input").rglob(
                "daily_input.json"
            )
        )

        if not input_files:
            raise FileNotFoundError(
                "daily_input.json was not found "
                "under /kaggle/input"
            )

        input_file = input_files[0]

    print(
        f"📥 Reading input: {input_file}"
    )

    with input_file.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def build_prompt(repository: dict) -> str:
    """Build the analysis prompt."""

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


def extract_json(text: str) -> dict:
    """Extract JSON from model output."""

    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    return json.loads(text)


def analyze_repository(
    model,
    tokenizer,
    repository: dict,
) -> dict:
    """Generate structured AI analysis."""

    prompt = build_prompt(repository)

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        text,
        return_tensors="pt",
    )

    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=800,
            do_sample=False,
        )

    generated_tokens = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    result_text = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    )

    return extract_json(result_text)


def main():

    print("🚀 Dev Radar AI Worker")

    input_root = Path("/kaggle/input")

    print(
        f"📁 Kaggle input directory: "
        f"{input_root}"
    )

    if input_root.exists():

        for path in input_root.rglob("*"):
            print(
                f"INPUT: {path}"
            )

    else:

        print(
            "❌ /kaggle/input does not exist"
        )

    print(
        f"🤖 Loading model: "
        f"{MODEL_NAME}"
    )

    # -------------------------------------------------
    # Load input
    # -------------------------------------------------

    input_data = load_input()

    repositories = input_data.get(
        "repositories",
        [],
    )

    print(
        f"📦 Repositories: "
        f"{len(repositories)}"
    )

    if not repositories:
        raise RuntimeError(
            "No repositories supplied."
        )

    # -------------------------------------------------
    # CUDA information
    # -------------------------------------------------

    print(
        f"🎮 CUDA available: "
        f"{torch.cuda.is_available()}"
    )

    if not torch.cuda.is_available():

        raise RuntimeError(
            "CUDA GPU is required for this Kaggle worker."
        )

    print(
        f"🎮 GPU: "
        f"{torch.cuda.get_device_name(0)}"
    )

    print(
        f"🎮 Compute capability: "
        f"{torch.cuda.get_device_capability(0)}"
    )

    print(
        f"🔥 PyTorch: "
        f"{torch.__version__}"
    )

    print(
        f"🔥 CUDA version: "
        f"{torch.version.cuda}"
    )

    print(
        f"🔥 Supported architectures: "
        f"{torch.cuda.get_arch_list()}"
    )

    # -------------------------------------------------
    # Load tokenizer
    # -------------------------------------------------

    print("🔤 Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    # -------------------------------------------------
    # Load model
    # -------------------------------------------------

    print("🧠 Loading model...")

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype=torch.float16,
        device_map="auto",
        attn_implementation="eager",
    )

    print("✅ Model loaded successfully.")

    # -------------------------------------------------
    # Analyze repositories
    # -------------------------------------------------

    results = []

    for index, repository in enumerate(
        repositories,
        start=1,
    ):

        name = repository.get(
            "full_name",
            "Unknown",
        )

        print(
            f"\n🧠 Analyzing "
            f"{index}/{len(repositories)}: "
            f"{name}"
        )

        try:

            analysis = analyze_repository(
                model,
                tokenizer,
                repository,
            )

            results.append(
                {
                    "full_name": name,
                    "status": "success",
                    "analysis": analysis,
                }
            )

            print(
                f"✅ Completed: {name}"
            )

        except Exception as exc:

            print(
                f"❌ Failed: "
                f"{name}: {exc}"
            )

            results.append(
                {
                    "full_name": name,
                    "status": "error",
                    "error": str(exc),
                }
            )

    # -------------------------------------------------
    # Write output
    # -------------------------------------------------

    output = {
        "date": input_data.get(
            "date"
        ),
        "status": "success",
        "repositories": results,
    }

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"\n💾 Output written to: "
        f"{OUTPUT_FILE}"
    )

    print(
        "\n🎉 Dev Radar AI Worker completed successfully."
    )


if __name__ == "__main__":
    main()