# Local LLM Deployment

This project provides a simple way to deploy large language models locally with a web interface.

## Requirements

- Python 3.8 or higher
- CUDA-capable GPU (recommended) or CPU
- At least 16GB RAM (32GB recommended)
- At least 20GB free disk space

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the deployment script:
```bash
python local_llm_deploy.py
```

2. Open your web browser and navigate to:
```
http://localhost:7860
```

## Features

- Local deployment of ChatGLM2-6B model
- Web-based chat interface
- Support for conversation history
- Automatic GPU/CPU detection

## Model Information

By default, this deployment uses the ChatGLM2-6B model from THUDM. You can modify the model in the `load_model()` function to use other compatible models.

## Notes

- First run will download the model weights (about 13GB)
- GPU memory usage can be high depending on the model size
- For better performance, ensure you have enough system resources 