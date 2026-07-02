import json
import sys
from pathlib import Path

# ============================================================
# Helpers
# ============================================================


def load_config():
    config_path = Path("config.json")
    if not config_path.exists():
        raise FileNotFoundError("config.json not found")
    with config_path.open("r") as f:
        return json.load(f)


def extract_model_entries(node, model_type_map):
    results = []
    props = node.get("properties", {})
    node_type = node.get("type")

    # Determine folder from config
    directory = model_type_map.get(node_type, "custom")

    # 1. Standard nodes with "models" list
    if "models" in props:
        for m in props["models"]:
            results.append({
                "name": m.get("name"),
                "url": m.get("url"),
                "directory": m.get("directory") or directory,
                "node_type": node_type
            })

    # 2. Nodes with model_name / checkpoint_name / lora_name
    for key in ["model_name", "checkpoint_name", "lora_name"]:
        if key in props:
            results.append({
                "name": props[key],
                "url": None,
                "directory": directory,
                "node_type": node_type
            })

    # 3. Custom nodes with embedded URLs
    for k, v in props.items():
        if isinstance(v, str) and "huggingface.co" in v:
            filename = v.split("/")[-1]
            results.append({
                "name": filename,
                "url": v,
                "directory": directory,
                "node_type": node_type
            })

    return results


def extract_all_models(workflow_json, config):
    model_type_map = config["model_type_map"]
    all_models = []

    for node in workflow_json.get("nodes", []):
        entries = extract_model_entries(node, model_type_map)
        all_models.extend(entries)

    # Deduplicate by name
    unique = {m["name"]: m for m in all_models}
    return {"models": list(unique.values())}


# ============================================================
# Main
# ============================================================

def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_all_models.py <workflow.json> <output.json>")
        sys.exit(1)

    workflow_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    config = load_config()

    with workflow_path.open("r", encoding="utf-8") as f:
        workflow_json = json.load(f)

    result = extract_all_models(workflow_json, config)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print(f"Model manifest written to {output_path}")


if __name__ == "__main__":
    main()
