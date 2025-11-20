# 🎥 Video Tutorial Script: Setting Up CLA with Docker

**Target Audience**: New team members (Devs, QA).
**Goal**: Get them from "Cloned Repo" to "Running App" in under 5 minutes.

---

## 1. Introduction (0:00 - 0:30)
*   **Visual**: Screen sharing the GitHub repository.
*   **Audio**: "Hi everyone! This is a quick guide on how to spin up the local development environment for the Construction Legal AI project. We're using Docker Compose to make this super easy, so you don't need to install Python, Node, or databases manually."

## 2. Prerequisites (0:30 - 1:00)
*   **Visual**: Show Docker Desktop dashboard running.
*   **Audio**: "First, make sure you have Docker Desktop installed and running. You'll see the little whale icon in your taskbar. That's it for prerequisites!"

## 3. Running the Stack (1:00 - 2:00)
*   **Visual**: Terminal window.
*   **Action**:
    1.  **Ollama**: "First, make sure Ollama is running natively. Run `ollama serve` in one terminal."
    2.  **Docker**: "In another terminal, go to the project folder and run `docker-compose up --build`."
*   **Audio**: "We run Ollama natively to get full GPU speed on your Mac. Then, Docker handles the rest—Python backend, Streamlit frontend, and databases."

## 4. Verifying the Setup (2:00 - 3:00)
*   **Visual**: Split screen or switching browser tabs.
*   **Action**:
    1.  Open `http://localhost:8501` -> Show the **Streamlit** interface.
    2.  Open `http://localhost:8000/docs` -> Show the Swagger UI.
    3.  Open `http://localhost:7474` -> Show Neo4j login.
*   **Audio**: "Head to localhost 8501. You'll see our Streamlit app ready for legal queries. Localhost 8000 has the API docs, and 7474 is the graph database."

## 5. Outro (3:00 - 3:15)
*   **Visual**: Back to IDE/Code.
*   **Audio**: "That's it! If you run into issues, check the `SETUP_GUIDE.md` file or ping me on Slack. Happy coding!"
