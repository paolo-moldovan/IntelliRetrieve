# IntelliRetrieve

IntelliRetrieve is a powerful document retrieval and question-answering system that uses hybrid ranking and RAG (Retrieval-Augmented Generation) to provide accurate answers from your document collection.

## Features

- **Multi-Format Document Support**
  - PDF files
  - Text files
  - DOCX files (coming soon)
  - JSON documents (coming soon)

- **Advanced Document Processing**
  - Intelligent text chunking with NLTK
  - Overlapping chunks for context preservation
  - Automatic handling of document structure

- **Hybrid Search & Ranking**
  - Vector similarity search using ChromaDB
  - Semantic ranking with Sentence Transformers
  - TF-IDF based lexical matching
  - Configurable weights for semantic and lexical scores

- **Interactive CLI Interface**
  - Rich terminal UI with progress bars
  - Easy document indexing
  - Interactive chat-like Q&A interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/IntelliRetrieve.git
cd IntelliRetrieve
```

2. Install PyTorch based on your system:

For Apple Silicon (M1/M2/M3) Macs:
```bash
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

For Intel Macs:
```bash
pip3 install torch torchvision torchaudio
```

For other systems:
```bash
pip3 install torch
```

3. Install other dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Select input type (folder or single file) when prompted

3. Enter the path to your document(s)

4. Start asking questions about your documents

## Configuration

Key settings can be adjusted in `src/config.py`:

```python
# API Settings
API_HOST: str = "0.0.0.0"
API_PORT: int = 8000

# Model Settings
DEFAULT_MODEL: str = "phi4"  # Ollama model to use
RANKING_MODEL: str = "all-MiniLM-L6-v2"  # Sentence transformer model

# Ranking Settings
SEMANTIC_WEIGHT: float = 0.7  # Weight for semantic similarity
LEXICAL_WEIGHT: float = 0.3   # Weight for lexical matching

# Chunking Settings
DEFAULT_CHUNK_SIZE: int = 500
DEFAULT_CHUNK_OVERLAP: int = 50
```

## Architecture

The system consists of several key components:

- **DataLoader**: Handles document loading and text extraction
- **Chunker**: Splits documents into manageable pieces while preserving context
- **VectorDB**: Manages document storage and initial retrieval using ChromaDB
- **Ranker**: Implements hybrid ranking combining semantic and lexical matching
- **Generator**: Handles response generation using Ollama
- **CLI**: Provides the user interface and interaction flow

## Requirements

- Python 3.8+
- PyTorch 2.0+
- See requirements.txt for full list

## Development

To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [ChromaDB](https://github.com/chroma-core/chroma)
- Uses [Sentence Transformers](https://github.com/UKPLab/sentence-transformers)
- Terminal UI powered by [Rich](https://github.com/Textualize/rich)