# 🌟 MAGIC-Repo2LLM

<div align="center">
  <img src="assets/logo.png" alt="MAGIC Research Logo" width="200"/>

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
  [![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)
  [![Powered by MAGIC](https://img.shields.io/badge/Powered%20by-MAGIC%20Research-purple)](https://researchmagic.com)

  **Transform GitHub repositories into AI-ready single files for LLM analysis**

  [Website](https://researchmagic.com) • [Documentation](#documentation) • [Docker Hub](https://hub.docker.com/r/magicresearch/repo2llm) • [Report Bug](https://github.com/Research-MAGIC/MAGIC-Repo2LLM/issues)

</div>

---

## 🎯 Overview

**MAGIC-Repo2LLM** is a powerful tool designed to concatenate all Python source files from any GitHub repository into a single file, making it perfect for Large Language Model (LLM) analysis, code review, and documentation purposes. This tool intelligently filters out test files, configuration files, and other non-essential code to provide clean, analyzable output optimized for AI consumption.

### ✨ Key Features

- 🚀 **Fast Processing**: Efficiently downloads and processes repositories
- 🎯 **Smart Filtering**: Automatically excludes test files, configs, and documentation
- 📊 **Token Counting**: Built-in token counter using OpenAI's cl100k_base encoding
- 🎨 **Beautiful UI**: Modern, responsive interface with MAGIC Research branding
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 📋 **One-Click Copy**: Instantly copy processed output to clipboard
- 🔄 **Real-time Logs**: Live processing updates and progress tracking

## 👨‍💻 Created By

**Dr. Rodrigo Masini de Melo**  
*Chief AI Officer at MAGIC Research*

Dr. Masini leads MAGIC Research's AI initiatives, focusing on innovative solutions that bridge the gap between complex AI technologies and practical applications. This tool represents MAGIC's commitment to open-source contributions and advancing AI research accessibility.

## 🚀 Quick Start

### Option 1: Run with Python

```bash
# Clone the repository
git clone https://github.com/Research-MAGIC/MAGIC-Repo2LLM.git
cd MAGIC-Repo2LLM

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Navigate to `http://localhost:8080` in your browser.

### Option 2: Run with Docker

```bash
# Using Docker directly
docker build -t magic-repo2llm .
docker run -p 8080:8080 magic-repo2llm

# Or using Docker Compose
docker-compose up
```

### Option 3: Pull from Docker Hub

```bash
docker pull magicresearch/repo2llm:latest
docker run -p 8080:8080 magicresearch/repo2llm:latest
```

## 📖 Documentation

### How It Works

1. **Input Repository URL**: Enter any public GitHub repository URL
2. **Specify Branch/Tag**: Choose the branch or tag to analyze (default: master)
3. **Process**: The tool downloads and intelligently filters Python files
4. **Analyze**: View token count and copy the concatenated output

### File Filtering Logic

The analyzer intelligently filters files by:

- ✅ **Including**: Main source code files (`.py`)
- ❌ **Excluding**: 
  - Test files and directories
  - Configuration files (`setup.py`, `hubconf.py`)
  - Documentation and examples
  - Hidden files and directories
  - `__pycache__` directories

### Token Counting

Uses OpenAI's `cl100k_base` encoding to calculate token counts, helping you:

- Estimate API costs for AI analysis
- Ensure content fits within model context windows
- Optimize file selection for analysis

## 🛠️ Development

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/Research-MAGIC/MAGIC-Repo2LLM.git
cd MAGIC-Repo2LLM

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies in development mode
pip install -r requirements.txt

# Run the application
python app.py
```

### Project Structure

```
MAGIC-Repo2LLM/
├── app.py                 # Main application file
├── assets/               # Assets and branding
│   └── logo.png         # MAGIC Research logo
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── README.md            # Project documentation
├── LICENSE              # MIT License
├── .gitignore          # Git ignore rules
└── .github/            # GitHub Actions workflows
    └── workflows/
        ├── ci.yml      # Continuous Integration
        └── docker.yml  # Docker build and push
```

## 🐳 Docker Configuration

### Building the Image

```bash
docker build -t magic-repo2llm:latest .
```

### Running with Custom Environment Variables

```bash
docker run -p 8080:8080 \
  -e NICEGUI_PORT=8080 \
  -e NICEGUI_HOST=0.0.0.0 \
  magic-repo2llm:latest
```

### Docker Compose with Volume Mounting

```yaml
version: '3.8'
services:
  analyzer:
    image: magicresearch/repo2llm:latest
    ports:
      - "8080:8080"
    volumes:
      - ./logs:/app/logs  # For persistent logging
```

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add tests for new features
- Update documentation as needed
- Ensure Docker builds pass

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MAGIC Research Team** - For continuous support and innovation
- **NiceGUI** - For the excellent Python web framework
- **OpenAI** - For tiktoken library and tokenization standards
- **Open Source Community** - For inspiration and contributions

## 📞 Support

For support, questions, or feedback:

- 📧 Email: [support@researchmagic.com](mailto:support@researchmagic.com)
- 🌐 Website: [researchmagic.com](https://researchmagic.com)
- 🐛 Issues: [GitHub Issues](https://github.com/Research-MAGIC/MAGIC-Repo2LLM/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/Research-MAGIC/MAGIC-Repo2LLM/discussions)

## 🚀 Roadmap

- [ ] Support for multiple programming languages (JavaScript, Go, Rust)
- [ ] Advanced filtering options and customization
- [ ] Batch processing for multiple repositories
- [ ] API endpoint for programmatic access
- [ ] Integration with popular AI platforms
- [ ] Export to various formats (JSON, XML, Markdown)
- [ ] Repository statistics and visualization
- [ ] Private repository support with authentication

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Research-MAGIC/MAGIC-Repo2LLM&type=Date)](https://star-history.com/#Research-MAGIC/MAGIC-Repo2LLM&Date)

---

<div align="center">
  <b>Built with 💜 by MAGIC Research</b><br>
  <sub>Empowering AI Research and Development</sub>
</div>
