# 🧪 ApothecaryAI

**An AI agent for detecting adversarial prompts and poisoned data in generative AI pipelines.**

ApothecaryAI is a proactive defense layer for generative AI systems. It screens real-time prompts and training/fine-tuning data for signs of adversarial manipulation or data poisoning — flagging suspicious content, explaining *why* it was flagged, and improving over time as new threats are confirmed.

> Built as a final project for MSDS 680 (Maxwell Guevarra), vibe-coded with heavy use of KIMI AI for iterative code generation.

---

## The Problem

Generative AI models are increasingly deployed in production, yet they remain vulnerable to two classes of attack:

- **Adversarial Inputs** — subtly crafted prompts or content that cause a model to misbehave, leak sensitive information, or bypass safety constraints.
- **Data Poisoning** — maliciously modified training/fine-tuning data that implants backdoors or bias, leading to unsafe or inaccurate outputs.

Most current mitigations are fragmented: manual audits, after-the-fact filters, and one-off checks that don't scale as models and datasets grow. ApothecaryAI aims to close that gap with an automated, explainable, continuously-learning screening agent.

## What It Does

- **Real-time Guard** — intercepts and analyzes user prompts before they reach the model, flagging or blocking malicious instructions.
- **Data Hygiene Monitor** — inspects training/fine-tuning datasets for poisoning indicators (backdoor triggers, anomalous labels, label flips).
- **Explainability & Alerts** — every flag comes with a transparent rationale so a human reviewer can understand *why* something was blocked.
- **Continuous Learning** — the detection model can be retrained on confirmed threats to improve accuracy over time.

## How It Works

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.11 | Core implementation |
| Web Layer | FastAPI + Uvicorn | Scanning service / API |
| Detection Engine | scikit-learn 1.5 (TF-IDF + Logistic Regression) | Classify prompts as adversarial vs. benign |
| Data Handling | Pandas, NumPy | Ingestion and vectorized heuristics |
| Front-End | Plain HTML5 | Minimal demo console |
| Containerization | Docker + Docker Compose | Reproducible runtime |
| Dev Assistance | KIMI AI | Code generation for agent modules |

**Training data:**
- [JailbreakV-28K](https://huggingface.co/datasets) — ~28,000 adversarial vs. benign prompts
- Self-generated poison sets — backdoor triggers, label flips, distribution skew
- Open anomaly-detection benchmark datasets

## Repository Structure

```
apothecaryAI/
├── apothecary/          # Core application package (scanner, detector, API)
├── data/                 # Training / evaluation datasets
├── notebooks/             # Exploration and model development notebooks
├── static/                # Front-end assets for the demo console
├── tests/                 # Test suite
├── generate_big.py        # Dataset generation script
├── train_offline.py       # Offline model training script
├── docker-compose.yml
├── dockerfile
├── requirements.txt
└── .env.example
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11 (if running outside Docker)

### Run with Docker

```bash
# Build and start the service
docker compose up --build

# Stop / restart
docker compose down
```

Once running, the demo console is available at:

```
http://0.0.0.0:8000
```

### Configuration

Copy `.env.example` to `.env` and set any required environment variables before starting the service.

## Training the Detector

The detection model (TF-IDF + Logistic Regression) can be retrained offline using confirmed threat data:

```bash
python train_offline.py
```

Synthetic/expanded training data can be generated with:

```bash
python generate_big.py
```

## Roadmap

- [ ] Support for additional file types beyond text
- [ ] GCP deployment for scalability and centralized logging
- [ ] Multi-modal support (images, not just text)
- [ ] Policy engine for configurable flagging/response rules
- [ ] Vector database (FAISS/Chroma) for attack-signature similarity search
- [ ] Observability via OpenTelemetry + Grafana

## Project Background

This project was developed for MSDS 680 to explore whether an automated agent could meaningfully reduce the manual burden of screening generative AI systems for adversarial and poisoning attacks. The current implementation focuses on a lightweight, explainable text classifier as a proof of concept, with a clear path toward multi-modal detection and production-scale deployment.

## Author

**Maxwell Guevarra**
MSDS 680 — Final Project

## License

*(Add a license file if you intend to make this project open for reuse — e.g., MIT.)*
