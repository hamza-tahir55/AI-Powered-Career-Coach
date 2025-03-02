# AI-Powered-Career-Coach
AI-powered career assistant automating resume evaluation, job search, and learning roadmaps. Uses CrewAI, Gemini 1.5, and Serper API to score CVs, suggest improvements, find relevant job openings in real-time, and generate weekly study plans for career growth.

**AI-Powered Career Assistant for Resume Evaluation, Job Search, and Learning Roadmaps**

AI-Powered-Career-Coach is an **Agentic AI** that automates **resume evaluation, real-time job search, and weekly study roadmap generation** using cutting-edge AI technologies.

## Features
- **Resume Evaluation & Scoring:** AI-based CV assessment with detailed improvement suggestions.
- **Real-time Job Search:** Automatically fetches **top 5 relevant job listings** from the web based on resume and location preferences.
- **Weekly Study Roadmaps:** Generates **structured learning plans** for various skills using internet resources.
- **Multi-Agent System:** Powered by **CrewAI** with role-based agents for different tasks.

## Tech Stack
- **CrewAI** – Agent Orchestration Framework
- **Gemini 1.5 Flash** – Google LLM API
- **Serper API** – Real-time Web Search
- **BeautifulSoup** – Web Scraping (Optional)
- **LangChain** – LLM Integration

## How It Works
1. Upload your resume.
2. Evaluates your resume and provides improvement suggestions.
3. The job researcher agent fetches the latest **relevant job listings** in real-time.
4. The education consultant agent generates a **personalized weekly study roadmap**.

## Installation
```bash
# Clone the repository
git clone https://github.com/usernamehamza-tahir55/AI-Powered-Career-Coach.git


# Install dependencies
pip install -r requirements.txt

# Set API Keys in your environment
export GOOGLE_API_KEY=your_google_api_key
export SERPER_API_KEY=your_serper_api_key

# Run the app
jupyter notebook app.ipynb
```

## API Keys Required
- Google Gemini API
- Serper.dev API

## Roadmap
- [ ] Resume PDF Upload
- [ ] Job Alerts
- [ ] Interview Question Generation
- [ ] Skill Progress Tracking

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License
This project is licensed under the MIT License.

---

