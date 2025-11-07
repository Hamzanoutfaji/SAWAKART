# SAWAKART

FastAPI web scraping backend powered by Playwright.

## 🚀 Quick Start

### Docker 

```bash
docker pull hamzanoutfaji/sawakart:latest
docker run -d -p 10000:10000 hamzanoutfaji/sawakart:latest
```

### Local Setup

```bash
# Clone and setup
git clone https://github.com/Hamzanoutfaji/SAWAKART.git
cd SAWAKART/backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
python -m playwright install

# Run
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📚 API Docs

Visit `http://localhost:10000/docs` after starting the backend.

