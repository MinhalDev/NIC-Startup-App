import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini with error handling
try:
    genai.configure(
        api_key=os.getenv("GEMINI_API_KEY"),
        transport="rest",
        client_options={"timeout": 30}  # Added timeout
    )
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated to current model
except Exception as e:
    st.error(f"Failed to initialize Gemini: {str(e)}")
    st.stop()

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
    This AI-powered tool helps you generate complete startup ideas.
    """)
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71")
    cols = st.columns(3)
    with cols[0]: st.markdown("#### 1. Input")
    with cols[1]: st.markdown("#### 2. Generate")
    with cols[2]: st.markdown("#### 3. Refine")
    footer()

@st.cache_data(show_spinner=False)
def generate_content(prompt):
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 2000
            }
        )
        return response.text
    except Exception as e:
        st.error(f"Generation failed: {str(e)}")
        return None

def idea_generator():
    st.title("Startup Idea Generator")
    input_method = st.radio(
        "Input type:",
        ["Keywords/Themes", "Problem Statement"],
        horizontal=True
    )
    
    user_input = st.text_area(
        "Describe your idea:" if input_method == "Problem Statement" else "Enter keywords:",
        placeholder="Describe a problem..." if input_method == "Problem Statement" else "e.g., AI, healthcare"
    )
    
    if st.button("Generate", type="primary") and user_input.strip():
        with st.spinner("Generating..."):
            prompt = f"""
            Create a startup plan based on: {input_method}
            Input: {user_input}
            
            Include:
            1. Startup Name  
            2. Tagline  
            3. Problem Statement  
            4. Solution  
            5. Target Market  
            6. Business Model  
            7. Competitive Advantage
            """
            
            if response := generate_content(prompt):
                st.markdown(response)
    
    footer()

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Landing Page", "Startup Idea Generator"])
    landing_page() if page == "Landing Page" else idea_generator()

if __name__ == "__main__":
    main()
