# WhatsApp Transcriber

A Python script to transcribe WhatsApp audio messages using OpenAI Whisper.

## 📝 Description

This project allows you to automatically transcribe audio messages from exported WhatsApp conversations. The script:

- Extracts ZIP files exported from WhatsApp
- Identifies audio messages (.opus)
- Transcribes audio using OpenAI's Whisper model
- Integrates transcriptions into the conversation history
- Generates a final file with the chat including transcriptions

## 🚀 Features

- ✅ Automatic transcription of audio messages
- ✅ Support for multiple Whisper model sizes
- ✅ Automatic GPU/CPU detection
- ✅ Detailed process logging
- ✅ Preservation of original chat format
- ✅ Portuguese language support

## 📋 Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Installing uv

If you don't have `uv` installed yet:

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/felipe0liveira/whatsapp-transcriber.git
cd whatsapp-transcriber
```

2. **Create a virtual environment:**
```bash
uv venv
```

3. **Activate the virtual environment:**
```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

4. **Install dependencies:**
```bash
uv sync
```

## 📱 How to export WhatsApp chat

1. Open WhatsApp on your phone
2. Go to the conversation you want to transcribe
3. Tap the three dots (⋮) in the top right corner
4. Select "More" → "Export chat"
5. Choose "Include media"
6. Save the generated ZIP file

## 🎯 How to use

1. **Place the exported ZIP file in the `data/` folder:**
```bash
mkdir -p data
# Copy your .zip file to the data/ folder
```

2. **Edit the `main.py` file (if necessary):**
Modify the final line to point to your ZIP file:
```python
if __name__ == "__main__":
    main(zip_path="data/YOUR_FILE.zip", model_size="medium")
```

3. **Run the script:**
```bash
make run
```

## ⚙️ Configuration

### Available model sizes

You can choose different Whisper model sizes:

- `tiny` - Fastest, lower accuracy
- `base` - Balanced
- `small` - Good accuracy, reasonable speed
- `medium` - **Default** - Good accuracy
- `large` - Best accuracy, slower

### System Monitoring

To check system resources:

```bash
make monitor
```

## 📁 Output structure

After execution, you will find:

```
output/
├── chat.txt                    # Chat with integrated transcriptions
└── whatsapp_chat/             # Files extracted from ZIP
    ├── _chat.txt              # Original chat
    ├── *.opus                 # Audio files
    └── *.jpg                  # Images (if any)
```

## 🔧 Troubleshooting

### GPU/CUDA Error

If you have CUDA issues, the script will automatically use CPU:

```
🖥️ Running on CPU
```

### Encoding Error

If there are issues with special characters, check that files are in UTF-8.

### Dependencies

If there are dependency issues, try:

```bash
uv sync --reinstall
```

## 📊 Execution Log

The script generates detailed logs in:
- Console (stdout)
- File `transcription.log`

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is under the MIT license. See the `LICENSE` file for more details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Audio transcription model
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager