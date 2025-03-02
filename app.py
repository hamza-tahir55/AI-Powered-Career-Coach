
# !pip install langchain_google_genai
# !pip install python-docx
# !pip install pymupdf
# !pip install crewai crewai-tools

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

os.environ["SERPER_API_KEY"] = "2fff7596aaa8d12d0cadd0cacc9a1fb9a34cb4e3"
search_tool = SerperDevTool()



load_dotenv()

# Configure litellm with Gemini
os.environ["OPENAI_API_KEY"] = "your key"  # Your Gemini API key
litellm.api_key = "your key"  # Your Gemini API key

# Initialize the model
llm = ChatOpenAI(
    model_name="gemini/gemini-1.5-flash",
    temperature=0.5,
    openai_api_key="your key ",  # Your Gemini API key
    max_tokens=1000
)

def extract_text_from_pdf(file_path):
    """Extracts text from pdf"""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

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
    
res1 = extract_text_from_resume("/path/to/your/file")
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
        """ Find the 5 most relevant recent job openings based on the improved resume recieved from the resume advisor and location preference. This is preferred location: {location}.
        Use the tools to gather relevant content and shortlist the 5 most relevant, recent,  job openings.
        """,

    expected_output=("A bullet points list of the 5 job openings, with the appropriate links and detailed description about each job, in markdown format."
    ),
    agent= job_researcher_agent
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


crew = Crew(
    agents=[resume_feedback_agent, resume_advisor_agent, job_researcher_agent, roadmap_agent],
    tasks= [resume_feedback_task,resume_advisor_task,  research_task, roadmap_task],
    verbose=True

)

result = crew.kickoff(inputs={"resume": res1, "location": "Islamabad", "skill":"AI-Engineer"})

from IPython.display import Markdown, display
Markdown_content = resume_feedback_task.output.raw.strip("'''markdown").strip("'''").strip()
display(Markdown(Markdown_content))

from IPython.display import Markdown, display
Markdown_content = resume_advisor_task.output.raw.strip("'''markdown").strip("'''").strip()
display(Markdown(Markdown_content))

from IPython.display import Markdown, display
Markdown_content = research_task.output.raw.strip("'''markdown").strip("'''").strip()
display(Markdown(Markdown_content))






