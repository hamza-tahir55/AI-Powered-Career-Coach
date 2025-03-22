
# !pip install langchain_google_genai
# !pip install python-docx
# !pip install pymupdf
# !pip install crewai crewai-tools
import sys
import pysqlite3

sys.modules["sqlite3"] = pysqlite3


from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
import litellm
import fitz
import docx
import crewai
import crewai_tools
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
import streamlit as st

os.environ["SERPER_API_KEY"] = "2fff7596aaa8d12d0cadd0cacc9a1fb9a34cb4e3"
search_tool = SerperDevTool()




load_dotenv()

# Configure litellm with Gemini
os.environ["OPENAI_API_KEY"] = "AIzaSyCSq35o-1vLYe3bKjKRoGNezTJNRmDMEx0"  # Your Gemini API key
litellm.api_key = "AIzaSyCSq35o-1vLYe3bKjKRoGNezTJNRmDMEx0"  # Your Gemini API key

# Initialize the model
llm = ChatOpenAI(
    model_name="gemini/gemini-1.5-flash",
    temperature=0.5,
    openai_api_key="Your API Key",  # Your Gemini API key
)

def extract_text_from_pdf(file):
    """Extracts text from pdf"""
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None

def extract_text_from_docx(file_path):
    """Extracts text from docx"""
    doc = docx.Document(file_path)
    full_text = ""
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return "\n".join(full_text)

def extract_text_from_resume(file_path):
    """Extracts text from resume"""
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file type"
    
res1 = extract_text_from_resume("/Users/hamzatahir/Documents/MHamza_Resume1.pdf")
print(res1)





resume_feedback_agent = Agent(
    role="Professional Resume Advisor",
    goal="Give professional feedback on the resume to make it stand out in the job market",
    backstory="with a strategic mind and an eye for detail, you excel at providing constructive feedbackon resumes to highlight the most relevant skills and experiencest",
    verbose=True,
    llm=llm,
)

resume_feedback_task = Task(
    description=(
        """Give feedback on the following resume to make it stand out for recruiters and hiring manager.
        Review every section, including summary, skills, experience, education, and certifications. Suggest improvements for each section.
        Also give overall score for the resume out of 10. This is the resume:{resume}"""
    ),

    expected_output="The overall score of the resume followed by feedback in bullet points",
    agent= resume_feedback_agent
)




resume_advisor_agent = Agent(
    role= "Professional Resume Writer",
    goal = "Based on the feedback recieved from the Resume Advisor, make changes to the resume and make it stand out in the job market.",
    backstory="With a strategic mind and an eye for detail, you excel at refining refining resumes based on feedback to highlight the most relevant experience and skills.",
    verbose=True,
    llm = llm 
    

)

resume_advisor_task = Task(
    description=(
        """Rewrite the resume based on the feedback to make it stand out for recruiters. You can adjust and enhance the resume but dont make up facts. 
        Review and update every section, including summary, skills, experience, education, and certifications.
        This is the resume:{resume}"""
    ),

    expected_output="Resume in markdown format that Effectively highlights the candidate's qualification and experiences",
    context=[resume_feedback_task],
    agent= resume_advisor_agent
)

job_researcher_agent = Agent(
    role="Senior Recruitment Consultant",
    goal = " Find the 5 most relevant, recently posted jobs based on the improved resume recieved from resume advisor and the location preference",
    tools= [search_tool],
    backstory=" As a senior recruitment consultant your process in finding the most relevant jobs based on the resume and location preference is unmatched. You can scan the resume efficiently, identify the most suitable job roles and search for the best suited recently posted open job positions at the preferred location,",
    verbose= True,
    llm = llm
)

research_task = Task(
    description=
        """Find the **5 most recent and relevant job openings** based on the improved resume received from the resume advisor and location preference.
        This is preferred location: {location}.
        Use the tools to gather job postings, and **only return Job Title and Link** for each job.
        Do not include descriptions — just **bullet points** with Title + Link.
        Dont say you can't list you have to list it no matter what
        """,

    expected_output=("A bullet points list of 5 job openings with the following format:\n"
    "- **Job Title**\n"
    "- [Apply Here](Job_URL)"),
    agent=job_researcher_agent
)

roadmap_agent = Agent(
    role="Education Consultant",
    goal="Create a weekly learning roadmap by researching the most relevant roadmaps available on the internet.",
    tools=[search_tool],
    backstory=(
        "You're a top-tier education consultant who finds and organizes learning roadmaps for any skill. "
        "You know how to find the best, up-to-date roadmaps and convert them into detailed 6-8 week study plans."
    ),
    verbose=True,
    llm=llm
)

roadmap_task = Task(
    description=(
        "Search for the best online roadmaps for {skill}. "
        "Select the most comprehensive roadmap and break it down into a 6-8 week structured study plan. "
        "Each week should cover 3-5 key topics with links to learning resources."
    ),
    expected_output=(
        "Weekly Study Plan in markdown format with topics, resources, and learning objectives."
    ),
    agent=roadmap_agent,
)


Interview_agent = Agent(
    role="Interview Preparation Coach",
    goal="Generate 10-15 tailored interview questions along with detailed, high-quality sample answers based on the user's skills and the provided job description.",
    backstory="You are an experienced Interview Preparation Coach specializing in helping candidates excel in job interviews. Your role is to craft relevant, industry-specific questions and model answers to guide users in their preparation, boosting their confidence and readiness.",
    verbose=True,
    llm=llm
)


Interview_task = Task(
    description=
        """Based on the user's skills, job description, and the improved resume received from the Resume Advisor, generate 10-15 highly relevant interview questions. 
        Cover both **technical** and **behavioral** aspects of the job role.
        Provide **detailed sample answers** with best practices, ensuring the answers align with the job requirements and highlight the user's strengths.
        Format the output in **markdown** with clear headings and bullet points.
        """,

    expected_output=(
        "A markdown-formatted: \n"
        "- 10-15 interview questions (divided into Technical and Behavioral categories).\n"
        "- Detailed sample answers for each question.\n"
        "- Tips on how to structure the answers (e.g., STAR method or Any Other Method).\n"
        "- Suggestions for improvement where necessary."
    ),
    agent=Interview_agent
)


crew = Crew(
    agents=[resume_feedback_agent, resume_advisor_agent, job_researcher_agent,roadmap_agent, Interview_agent],
    tasks= [resume_feedback_task,resume_advisor_task,  research_task, roadmap_task, Interview_task],
    verbose=True

)
# Streamlit UI
st.title("AI - Career Coach 🚀")
st.subheader("Your Personalized Job Preparation Assistant")

uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])
location = st.text_input("Preferred Job Location", placeholder="e.g. Islamabad, Lahore, Karachi")
skill = st.text_input("Preferred Skill", placeholder="e.g. DevOps, AI Engineer")

if uploaded_file and location:
    st.success("✅ Resume Uploaded Successfully!")
    resume_text = extract_text_from_pdf(uploaded_file)

    if st.button("Start Career Coaching"):
        st.info("🔍 Generating Results... Please wait")
        result = crew.kickoff(inputs={"resume": resume_text, "location": location, "skill":"AI-Engineer"})

        # Display Results
        st.subheader("1. Resume Feedback")
        st.markdown(resume_feedback_task.output.raw, unsafe_allow_html=True)

        st.subheader("2. Improved Resume")
        st.markdown(resume_advisor_task.output.raw, unsafe_allow_html=True)

        st.subheader("3. Job Openings")
        st.markdown(research_task.output.raw, unsafe_allow_html=True)

        st.subheader("4. Roadmap")
        st.markdown(roadmap_task.output.raw, unsafe_allow_html=True)

        st.subheader("4. Interview Preparation")
        st.markdown(Interview_task.output.raw, unsafe_allow_html=True)

        st.success("✅ All tasks completed successfully!")

# Footer
st.markdown("---")
st.caption("Powered by **Agentic AI** | Built with CrewAI + Gemini + Streamlit")
