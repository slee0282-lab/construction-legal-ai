# 🐳 Docker Environment Setup Guide

This guide will help you set up the Construction Legal AI (CLA) development environment using Docker Compose.

## Prerequisites

1.  **Docker Desktop**: Install from [docker.com](https://www.docker.com/products/docker-desktop/).
    *   Ensure it is running.
2.  **Git**: Ensure you have cloned the repository.

## Quick Start

1.  **Install & Run Ollama (Native)**:
    *   **Install**: `brew install ollama`
    *   **Start Server**: `ollama serve`
    *   **Pull Model**: Open a new terminal and run `ollama run llama3`.
    *   *Why?* This runs the LLM natively on your Mac's GPU (Metal) for maximum speed, instead of slowing it down inside Docker.

2.  **Navigate to the project root**:
    ```bash
    cd cla-system
    ```

3.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```
    *   This starts the **Backend (FastAPI)**, **Frontend (Streamlit)**, **Neo4j**, and **Postgres**.

4.  **Verify Services**:
    *   **Frontend (Streamlit)**: [http://localhost:8501](http://localhost:8501)
    *   **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs)
    *   **Neo4j**: [http://localhost:7474](http://localhost:7474) (User: `neo4j`, Password: `password`)
    *   **Redis**: Running on port `6379` (Internal).

## Troubleshooting

*   **Port Conflicts**: If a port is already in use, check if you have other services running (e.g., another Postgres instance).
*   **LLM Engine**: If you don't have a GPU, you may need to comment out the `deploy` section in `docker-compose.yml` for the `llm_engine` service.

## Useful Commands

*   **Stop all services**: `Ctrl+C` or `docker-compose down`
*   **Rebuild a specific service**: `docker-compose up --build backend`
*   **View logs**: `docker-compose logs -f`
