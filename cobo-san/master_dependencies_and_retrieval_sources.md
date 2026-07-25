# 📚 UAO Master Dependencies & Retrieval Source Links Inventory

**System Identity:** UAO (Unified Architecture & Operations / Cobo-San Master Build)  
**Target Repository:** [https://github.com/Cobo-san/UAO](https://github.com/Cobo-san/UAO)  
**GCP Account & Project:** `sounddharma@gmail.com` | `anaconda-google-project-sounddharma`  
**Financial Spend Target:** `$0.00 / Month` (100% Free Tier Guaranteed)  
**Hardware Protection:** 100% Read-Only NVMe Preservation (`:ro` Mount / `chmod 444`)

---

## 🤖 1. GGUF Master Model Weights & Hugging Face Retrieval Repositories

All master model weights are downloaded exclusively to the primary `C:` NVMe hub and replicated to `D:` and `E:` drives via zero-network internal PCIe copy.

| Model Name | File Size | Hugging Face Repository | Direct Source Link | Primary Storage Target Path |
| :--- | :---: | :--- | :--- | :--- |
| **`Llama-3.3-70B-Instruct`** | **39.60 GB** | `bartowski/Llama-3.3-70B-Instruct-GGUF` | [Hugging Face Model Link](https://huggingface.co/bartowski/Llama-3.3-70B-Instruct-GGUF) | `C:\AI_Dedicated_Storage_1TB\models_gguf\Llama-3.3-70B-Instruct-Q4_K_M.gguf` |
| **`Qwen-2.5-Coder-32B`** | **21.66 GB** | `Qwen/Qwen2.5-Coder-32B-Instruct-GGUF` | [Hugging Face Model Link](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct-GGUF) | `C:\AI_Dedicated_Storage_1TB\models_gguf\Qwen-2.5-Coder-32B-Instruct-Q5_K_M.gguf` |
| **`DeepSeek-R1-Distill-70B`** | **39.60 GB** | `unsloth/DeepSeek-R1-Distill-Llama-70B-GGUF` | [Hugging Face Model Link](https://huggingface.co/unsloth/DeepSeek-R1-Distill-Llama-70B-GGUF) | `C:\AI_Dedicated_Storage_1TB\models_gguf\DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf` |
| **`Codestral-22B-v0.1`** | **14.64 GB** | `bartowski/Codestral-22B-v0.1-GGUF` | [Hugging Face Model Link](https://huggingface.co/bartowski/Codestral-22B-v0.1-GGUF) | `C:\AI_Dedicated_Storage_1TB\models_gguf\Codestral-22B-v0.1-Q5_K_M.gguf` |

---

## 🎧📺🎨 2. Multi-Modal AI Engines & Retrieval Sources (Ports 8094 - 8099)

| Modality | Engine / Model Name | Source Repository | Direct Source Link | Primary Storage Folder |
| :--- | :--- | :--- | :--- | :--- |
| **Speech STT (Port 8094)** | `whisper.cpp` (`medium.en`) | `ggerganov/whisper.cpp` | [Whisper.cpp Repository](https://github.com/ggerganov/whisper.cpp) | `...\AI_Dedicated_Storage_MultiModaludio_stt_tts\` |
| **Voice TTS (Port 8095)** | `Piper TTS Engine` | `rhasspy/piper` | [Piper TTS Repository](https://github.com/rhasspy/piper) | `...\AI_Dedicated_Storage_MultiModaludio_stt_tts\` |
| **Vision OCR (Port 8096)** | `LLaVA-v1.6-7B` / `Qwen2-VL` | `haotian-liu/LLaVA` | [LLaVA Vision Repository](https://github.com/haotian-liu/LLaVA) | `...\AI_Dedicated_Storage_MultiModalisual_ocr\` |
| **Image Gen (Port 8097)** | `FLUX.1-schnell` / `SDXL` | `black-forest-labs/FLUX.1-schnell` | [FLUX.1 Model Link](https://huggingface.co/black-forest-labs/FLUX.1-schnell) | `...\AI_Dedicated_Storage_MultiModalisual_image_gen\` |
| **Audio & SFX (Port 8098)** | `Meta MusicGen` + `AudioGen` | `facebook/musicgen-small` | [MusicGen Model Link](https://huggingface.co/facebook/musicgen-small) | `...\AI_Dedicated_Storage_MultiModaludio_sound_gen\` |
| **Video Motion (Port 8099)**| `Stable Video Diffusion (SVD)`| `stabilityai/stable-video-diffusion` | [SVD Model Link](https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt) | `...\AI_Dedicated_Storage_MultiModalisual_video_gen\` |

---

## 🐍 3. Anaconda AI Platform & Environmental Stacks

| Framework / Service | Category | Integration Status | Official Documentation / Source Link |
| :--- | :--- | :---: | :--- |
| **Anaconda AI Studio API** | **Local Studio Server** | `http://localhost:8090/v1` | [Anaconda AI Studio](https://www.anaconda.com/products/ai-studio) |
| **GCP Cloud Integration** | **Cloud Integration** | `anaconda-google-project-sounddharma` | [Google Cloud Console](https://console.cloud.google.com/) |
| **PyTorch** | **Deep Learning Tensor Math** | `v2.4.0 (Conda Base)` | [PyTorch Official Portal](https://pytorch.org) |
| **TensorFlow** | **Graph ML Engine** | `v2.17.0 (Conda Base)` | [TensorFlow Official Portal](https://www.tensorflow.org) |
| **Scikit-learn** | **Predictive Analytics** | `v1.5.0 (Conda Base)` | [Scikit-learn Portal](https://scikit-learn.org) |
| **LangChain** | **Multi-Agent Orchestration** | `v0.3.0 (Conda Base)` | [LangChain Documentation](https://www.langchain.com) |
| **LlamaIndex** | **RAG Vector Data Indexer** | `v0.11.0 (Conda Base)` | [LlamaIndex Documentation](https://www.llamaindex.ai) |
| **Hugging Face Transformers**| **Model Tokenization & Loaders**| `v4.44.0 (Conda Base)` | [Hugging Face Docs](https://huggingface.co/docs/transformers) |
| **OpenCV** | **Visual Screenshot Capture** | `v4.10.0 (Conda Base)` | [OpenCV Official Portal](https://opencv.org) |

---

## 🛠️ 4. System Utility & Infrastructure Dependencies

* **Python Runtime**: Python 3.12 (`Python Software Foundation / Conda Base`).
* **Inference Server**: `llama.cpp` native server (`https://github.com/ggerganov/llama.cpp`).
* **Linux Kernel & WSL2**: Ubuntu 24.04 LTS WSL2 Kernel (`https://ubuntu.com/wsl`).
* **Database WAL Engine**: SQLite3 C-Library (`https://www.sqlite.org/wal.html`).
* **Version Control**: Git & GitHub CLI (`https://github.com/cli/cli`).

---

## 📦 5. Master Recovery Package

All dependencies, configuration manifests, and script blueprints are embedded inside the master golden package:

* **Master Build Package**: [cobo-san_master_unified_all_in_one_build.json](file:///C:/Users/Monica%20Fugazi/.antigravity-ide/living_repository/cobo-san/cobo-san_master_unified_all_in_one_build.json)
* **Master Manifest**: [cobo-san_manifest.json](file:///C:/Users/Monica%20Fugazi/.antigravity-ide/living_repository/cobo-san/cobo-san_manifest.json)
