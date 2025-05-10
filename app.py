import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


model = genai.GenerativeModel('gemini-2.0-flash')

st.set_page_config(
    page_title="NIC Startup Generator",
    layout="centered"
)

def footer():
    st.markdown("---")
    st.markdown("Developed by Muhammad Minhal Ghouri")

def landing_page():
    st.title("Welcome to NIC Startup Generator")
    st.markdown("""
    ## Unleash Your Entrepreneurial Potential
    
    This AI-powered tool helps you generate complete startup ideas based on your interests, 
    problems you want to solve, or industry themes you're passionate about.
    
    Get started by navigating to the **Startup Idea Generator** page from the sidebar.
    """)
    
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80", 
             caption="Innovation starts with an idea")
    
    st.markdown("### How it works:")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        #### 1. Input
        Provide keywords, themes, or describe a problem
        """)
    with cols[1]:
        st.markdown("""
        #### 2. Generate
        Our AI analyzes your input and creates a startup plan
        """)
    with cols[2]:
        st.markdown("""
        #### 3. Refine
        Adjust your input and regenerate as needed
        """)
    
    footer()

def idea_generator():
    st.title("Startup Idea Generator")
    st.markdown("""
    Generate a complete startup plan by providing:
    - Keywords or themes (e.g., "healthcare, education")
    - A specific problem you want to solve
    """)
    
    input_method = st.radio(
        "How would you like to provide input?",
        ["Keywords/Themes", "Problem Statement"],
        horizontal=True
    )
    
    user_input = ""
    
    if input_method == "Keywords/Themes":
        user_input = st.text_input(
            "Enter comma-separated keywords or themes (e.g., healthcare, education)",
            placeholder="technology, environment, mobile apps"
        )
    else:
        user_input = st.text_area(
            "Describe the problem you want to solve",
            placeholder="Many small businesses struggle with inventory management..."
        )
    
    if st.button("Generate Startup Idea", type="primary"):
        if not user_input.strip():
            st.warning("Please provide some input to generate ideas")
        else:
            with st.spinner("Generating your startup plan..."):
                try:
                    prompt = f"""
                    Create a comprehensive startup plan based on the following input:
                    
                    Input Type: {input_method}
                    User Input: {user_input}
                    
                    The startup plan should include:
                    1. Startup Name (creative and memorable)
                    2. Tagline (concise and impactful)
                    3. Problem Statement (clear description of the problem being solved)
                    4. Solution (detailed description of the proposed solution)
                    5. Target Market (specific customer segments)
                    6. Unique Value Proposition (what makes this different)
                    7. Business Model (how it will make money)
                    8. Key Features (main product/service features)
                    9. Competitive Advantage
                    10. Potential Challenges
                    11. Initial Action Steps
                    
                    Format the output in clear markdown with appropriate headings.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown("## Your Generated Startup Plan")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    footer()

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Landing Page", "Startup Idea Generator"])
    
    if page == "Landing Page":
        landing_page()
    else:
        idea_generator()

if __name__ == "__main__":
    main()
