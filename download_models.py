import json
import sys
from pathlib import Path
import huggingface_hub
from huggingface_hub import hf_hub_download

# ============================================================
# Helpers
# ============================================================


def load_config():
    config_path = Path("config.json")
    if not config_path.exists():
        raise FileNotFoundError("config.json not found")
    with config_path.open("r") as f:
        return json.load(f)


def resolve_target_dir(config, directory_key):
    root = Path(config["comfy_model_root"])
    folder_name = config["folders"].get(directory_key, "custom")
    target_dir = root / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def parse_repo_and_filename(url):
    parts = url.split("/")
    repo_id = "/".join(parts[3:5])
    filename = parts[-1]
    return repo_id, filename


def download_model(entry, config):
    name = entry["name"]
    url = entry["url"]
    directory = entry["directory"]

    target_dir = resolve_target_dir(config, directory)

    if not url:
        print(f"⚠ Missing URL for model: {name}")
        return

    repo_id, filename = parse_repo_and_filename(url)

    print(f"⬇ Downloading {name} from {repo_id}")

    downloaded_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=target_dir,
        local_dir_use_symlinks=config["huggingface"]["use_symlinks"],
        cache_dir=config["huggingface"]["cache_dir"]
    )

    print(f"✔ Saved to {downloaded_path}")


# ============================================================
# Main
# ============================================================

def main():
    # Version check belongs HERE — not at the top
    required_version = (0, 25, 0)
    current_version = tuple(map(int, huggingface_hub.__version__.split(".")))

    if current_version < required_version:
        raise RuntimeError(
            f"huggingface_hub version {huggingface_hub.__version__} is too old.\n"
            f"Please run: pip install -U huggingface_hub"
        )

    if len(sys.argv) < 2:
        print("Usage: python download_models_configured.py <models.json>")
        sys.exit(1)

    manifest_path = Path(sys.argv[1])

    with manifest_path.open("r") as f:
        manifest = json.load(f)

    config = load_config()

    for entry in manifest.get("models", []):
        download_model(entry, config)


if __name__ == "__main__":
    main()
