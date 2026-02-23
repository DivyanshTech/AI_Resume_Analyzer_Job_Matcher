## ✨ Features

### 📄 Resume Support
- **Format:** PDF only

### 🔍 Extraction
- Full resume text
- Skills: programming languages, frameworks, tools, soft skills
- Structured JSON output for easy processing

### 📊 Scoring System
**Weighted Average:**


**Score Interpretation:**  
- 🟢 75–100%: Strong match  
- 🟡 50–74%: Moderate match  
- 🔴 0–49%: Low match

### 📈 Output & Visualization
- Match % with color-coded indicator
- Matched skills (green), missing skills (red)
- AI-generated explanation
- Actionable recommendations

### 🌐 Language Support
- English only (extensible to 50+ languages)


## 🛠 Technology Stack

**Backend:**
- **Framework:** FastAPI (async, production-ready)
- **Database:** SQLite (lightweight local storage using SQLAlchemy ORM)
- **PDF Processing:** PyPDF2
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`) — 384-dim vectors, local, free
- **Vector Storage:** FAISS (used for embedding persistence and future scalable nearest-neighbor retrieval)
- **Skill Extraction:** Rule-based keyword extraction (regex + predefined skill list)
- **Similarity:** Cosine similarity implemented manually using NumPy

**Frontend:**
- **Framework:** React 18 + TypeScript
- **Styling:** Custom CSS
- **HTTP Client:** Axios
- **Icons:** Lucide React

**Database: SQLite:**
Core Table Structure (SQLAlchemy ORM):

- id (Integer, Primary Key)
- filename (String)
- extracted_text (Text)
- skills (JSON/Text)
- embedding_id (String reference for FAISS index)
- created_at (Timestamp)

**⚙️ Current Matching Design**
The system currently performs semantic comparison between a single resume and a single job description by:
1. Generating embeddings for both texts
2. Computing cosine similarity directly using NumPy
3. Combining semantic similarity (60%) with explicit skill overlap (40%)

FAISS is integrated for embedding storage and is structured to support future scalable multi-job nearest-neighbor retrieval.

## 📦 Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- SQLite (auto-created, no separate installation required)
- 4GB RAM (for ML models)

### Steps

1. **Clone Repository**

git clone https://github.com/yourusername/ai-resume-matcher.git
cd ai-resume-matcher


2. **Backend Setup**
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create database
createdb resume_matcher

# Configure environment
cp .env.example .env
# Edit .env for DATABASE_URL and optional OPENAI_API_KEY

3. **Frontend Setup**
cd frontend
npm install


4. **Run Application**
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm start


Access:
Frontend: http://localhost:3000
API Docs: http://localhost:8000/docs


## 🚀 Usage

**Web Interface:**
1. Upload Resume: Click upload, select PDF file
2. Automatic Skill Extraction (~3 sec)
3. Paste Job Description
4. View Results: Match %, matched/missing skills, recommendations

**API Example:**

# 1. Upload Resume
curl -X POST "http://localhost:8000/api/upload-resume" -F "file=@resume.pdf"

# 2. Extract Skills
curl -X POST "http://localhost:8000/api/extract-skills/1"

# 3. Match Resume
curl -X POST "http://localhost:8000/api/match" -H "Content-Type: application/json" \
-d '{"resume_id":1,"job_description":"Python developer with FastAPI"}'


## 📁 Folder Structure
ai-resume-matcher/
├── backend/
│ ├── app/api/routes.py # REST API endpoints
│ ├── app/models/resume.py # Database models
│ ├── app/services/pdf_extractor.py # PDF text extraction
│ ├── app/services/skill_extractor.py # AI skill extraction
│ ├── app/services/embeddings.py # Sentence-Transformers wrapper
│ ├── app/services/matcher.py # Matching algorithm
│ ├── app/utils/faiss_store.py # FAISS vector operations
│ └── app/main.py # FastAPI application
├── frontend/
│ ├── src/components/ # React components
│ ├── src/services/api.ts # API client
│ └── src/App.tsx # Main application
├── requirements.txt
├── package.json
├── .env
└── README.md


## 🤝 Contributing
- Fork the repository  
- Create a feature branch: `git checkout -b feature/YourFeature`  
- Commit changes: `git commit -m "Add YourFeature"`  
- Push to branch: `git push origin feature/YourFeature`  
- Open a Pull Request  

**Development Guidelines:**  
- Follow PEP 8 (Python) and ESLint (TypeScript)  
- Add comments for complex logic  
- Test locally before submitting PR  


## 📄 License
This project is licensed under the **MIT License**.  

**MIT License Summary:**  
- ✅ Commercial use allowed  
- ✅ Modification allowed  
- ✅ Distribution allowed  
- ✅ Private use allowed  
- ⚠️ Liability and warranty not provided  


## 👨‍💻 Author
**Divyansh Lodha**  
- GitHub: [@DivyanshTech](https://github.com/DivyanshTech)  
- LinkedIn: [Divyansh Lodha](https://www.linkedin.com/in/divyansh-lodha-506a6429a/?originalSubdomain=in-ldn)  
- Email: divyanshlodha2005@gmail.com  

---

## 🙏 Acknowledgments
- [Sentence-Transformers](https://www.sbert.net/) - Free, open-source embeddings  
- [FAISS](https://github.com/facebookresearch/faiss) - Fast similarity search  
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework

## SCREENSHOTS of APP
<div align="center">
<img src="../Screenshots/job%20description%20testing%20ui.png" width="200" alt="Job Description Testing UI" /> 
<img src="../Screenshots/Job_MAtch_analysis%20UI.png" width="200" alt="Job Match Analysis UI" /> 
<img src="../Screenshots/Skills%20extraction%20UI.png" width="200" alt="Skills Extraction UI" /> 
<img src="../Screenshots/upload%20interface.png" width="200" alt="Upload Interface UI" /> 
<br>
AI-powered resume analysis with semantic job matching | 100% Free ML Pipeline
</div>


