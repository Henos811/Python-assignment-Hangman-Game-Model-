# Python-assignment-Hangman-Game-Model (Section 18)

# Description
  This project is a fun take on the classic Hangman game, where players guess letters to uncover a hidden word. The game will have a simple and user-friendly            interface, showing the word as a series of blanks and updating with each correct guess. Players will need to guess within a limited number of tries.

# Complete Project Setup Guide 
  ## 1. System Requirements  
  - **Python 3.8+** ([Download Python](https://www.python.org/downloads/))  
  - **Git** ([Download Git](https://git-scm.com/))  
  - **Pip** (Comes with Python)  

  * (Recommended: 64-bit OS for better compatibility.)*  

  ## **📥 2. Clone the Repository**  
    1. Open **Terminal (Mac/Linux)** or **Command Prompt/PowerShell (Windows)**.  
    2. Run:  
      git clone https://github.com/Henos811/Python-assignment-Hangman-Game-Model-.git
      cd Python-assignment-Hangman-Game-Model-
      

  ## **🐍 3. Set Up a Python Virtual Environment**  

    ### **Create & Activate the Virtual Environment**  
    - **Windows (PowerShell):**  
      python -m venv .venv
      .\.venv\Scripts\activate

    - **Mac/Linux (Terminal):**  
      python3 -m venv .venv
      source .venv/bin/activate
      
    ✅ **Success?** You should see `(.venv)` in your terminal prompt.  


  ## **📦 4. Install Dependencies**  
  The project uses `requirements.txt` to manage dependencies.  

    1. Make sure your virtual environment is **activated**.  
    2. Run:  
      pip install -r requirements.txt
      *(This installs Pygame and all other required packages.)*  


  ## **🚀 6. Run the Project**  
  1. Ensure the virtual environment is **activated**.  
  2. Run the main script:  
      python main.py 


  ## **❌ Common Mistakes to Avoid**  
  - **Don’t commit `.venv/`** (add it to `.gitignore`).  
  - **Don’t modify `requirements.txt` manually** (always use `pip freeze`).  
  

# Features
  In our Hangman game project, each letter of the alphabet is displayed as a button on the screen. This setup lets players simply click on their guesses instead of      typing them out. The buttons are easy to see and clearly labeled, making it simple to identify which letters are still available. The game randomly selects a word     from a predefined list for each round, ensuring a fresh challenge every time. When a player clicks on a button, their guess is registered, and the game updates        accordingly. If they guess correctly, the corresponding letters appear in the word, while incorrect guesses add to the hangman graphic. 

# Group Members
  1. Henos Tadesse........UGR/9772/17
  2. Lydia Ayele...............UGR/8704/17
  3. Kidus Yared...............UGR/2659/17
  4. Khalid Sefyu..............UGR/9391/17






