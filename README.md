# 🏔️ skicyclerun.cdl

## Automated Model Extraction & Downloading for ComfyUI Workflows

This project provides a two‑step pipeline for analyzing a ComfyUI workflow, extracting all required model artifacts, and downloading them into the correct folder structure based on a configurable mapping.

It is designed to make complex workflows portable, reproducible, and easy to set up on new machines — without manually hunting down dozens of model files.

---

## 🚀 Features

- 🔍 Extracts all model references from a ComfyUI workflow JSON
- 🧠 Detects models from:
  - Standard `models` lists
  - `model_name`, `checkpoint_name`, `lora_name` fields
  - Embedded HuggingFace URLs
- 🗂️ Generates a clean manifest (`output.json`) with deduplicated model entries
- 📥 Downloads large model files from HuggingFace or other URLs
- 📁 Places each model into the correct folder based on `config.json`
- 🔧 Fully customizable folder mappings and model type associations

---

📦 Repository Structure
skicyclerun.cdl/
│
├── extract_all_models.py # Step 1: Extract model metadata from workflow
├── download_models.py # Step 2: Download models into correct folders
├── config.json # Folder mappings, model type map, HF settings
└── README.md # You're reading it!

🧩 How It Works
Step 1 — Extract Model Metadata
Script: extract_all_models.py
This script scans a ComfyUI workflow JSON and extracts every model reference, including:
• Model names
• Download URLs
• Node types
• Target directories (based on config)
It produces a manifest like:
{
"models": [
{
"name": "model.safetensors",
"url": "https://huggingface.co/.../model.safetensors",
"directory": "checkpoints",
"node_type": "CheckpointLoader"
}
]
}
python extract_all_models.py workflow.json manifest.json

Step 2 — Download Required Models
Script: download_models.py
This script reads the manifest produced in Step 1 and:
• Downloads each model file
• Creates folders if needed
• Places each file into the correct directory under your ComfyUI model root
• Supports HuggingFace caching and optional symlink behavior
Run it like this:

python download_models.py manifest.json

⚙️ Configuration (`config.json`)
Your config.json defines:
📁 ComfyUI Model Root
Where all downloaded models will be stored:

"comfy_model_root": "/Users/timothyhalley/ComfyUI-Shared/models"

📂 Folder Mapping
Each model type maps to a folder:

"folders": {
"checkpoints": "checkpoints",
"vae": "vae",
"controlnet": "controlnet",
"hypernetworks": "hypernetworks",
"custom": "custom"
}

🧠 Model Type Map
Maps ComfyUI node types → folder names:

"model_type_map": {
"UNETLoader": "diffusion_models",
"CLIPLoader": "text_enc",
"VAELoader": "vae",
"LoRALoader": "hypernetworks"
}

🤗 HuggingFace Settings

"huggingface": {
"use_symlinks": false,
"cache_dir": "~/.cache/huggingface"
}

🛠️ Example Workflow
1️⃣ Extract model metadata
python extract_all_models.py my_workflow.json manifest.json

2️⃣ Download all required models
python download_models.py manifest.json

3️⃣ Start ComfyUI — everything is now in the right place 🎉

🧪 Why This Exists
ComfyUI workflows often reference dozens of models scattered across:
• Checkpoints
• VAEs
• LoRAs
• ControlNets
• Diffusers
• Custom nodes
Manually collecting these is slow and error‑prone.
This project automates the entire process so you can:
• Share workflows easily
• Reproduce environments reliably
• Avoid missing‑model errors
• Speed up setup on new machines
