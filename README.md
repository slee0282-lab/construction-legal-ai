# 🏗️ Construction Legal AI (CLA)

**Version:** v1.0 (Skeleton Build)

**Status:** Active Development (Private Alpha)

**Focus:** Contract-Centric Conflict Resolution

**Legal Framework:** FIDIC Red Book (1999)

## 💡 1. Project Vision

**Construction Legal AI (CLA)** is a comprehensive, governance-ready solution designed to resolve bottlenecks in construction projects.

Unlike generic chatbots, CLA is a **Contract-Centric Reasoning Engine**. It grounds every decision, claim assessment, and compliance check in the specific clauses of the project contract, using the **FIDIC Red Book (Conditions of Contract for Construction)** as the foundational ontology for legal terms and rules.

### **Core Mandates**

1. **Private Cloud First:** No client data touches public LLM APIs (OpenAI/Anthropic). We run entirely on-premise or in a private VPC.
    
2. **FIDIC-Grounded Reasoning:** The system's logic and ontology are built upon **FIDIC Red Book 1999** definitions (e.g., _Sub-Clause 20.1 "Contractor's Claims"_, _Sub-Clause 8.4 "Extension of Time"_). All reasoning is validated against these standard conditions plus the client's Particular Conditions.
    
3. **Policy Adaptive:** The system checks internal governance rules (Policy Packs) _before_ and _after_ generating a response to ensure commercial alignment.
    

## 🧱 2. System Architecture

CLA operates as a **Modular Monolith** within a Dockerized environment, designed for eventual deployment to an AWS Private VPC.

### **Logical Components**

- **Presentation Layer (Frontend):** A React-based web dashboard for Construction Managers to submit claims and Legal Admins to upload contracts.
    
- **Orchestration Layer (Backend):** A Python-based "Brain" using **LangGraph**. It manages the flow between the database, the policy engine, and the LLM.
    
- **Parsing Layer (Doc Parser):** A dedicated module (`unstructured` + `pdfminer`) that parses raw PDF contracts and maps them to the **FIDIC Ontology** in Neo4j.
    
- **Inference Layer (Compute):** A local, containerized LLM engine (**Ollama/vLLM**) running Llama 3.1 70B.
    

### **Physical Stack (Docker Services)**

|   |   |   |   |
|---|---|---|---|
|**Service Name**|**Technology**|**Port**|**Purpose**|
|`backend`|**FastAPI + Python 3.14** (Managed by **UV**)|`8000`|The core API, Orchestrator, and Doc Parser. Built with UV for blazing fast dependency resolution.|
|`frontend`|**React (Node 18)**|`3000`|The user interface.|
|`neo4j`|**Neo4j Community**|`7474` / `7687`|The Legal Knowledge Graph (Stores FIDIC Clauses + Particular Conditions).|
|`postgres`|**PostgreSQL 15**|`5432`|Audit logs, User sessions, Policy Pack storage.|
|`llm_engine`|**Ollama**|`11434`|Local LLM Inference Server.|

## 🚀 3. Quick Start (Local Dev)

**Prerequisites:**

- Docker & Docker Compose installed.
    
- Standard GPU (Nvidia) OR Apple Silicon (M1/M2/M3) recommended for local inference.
    

### **Step 1: Clone & Setup**

```
git clone [https://github.com/your-org/cla-system.git](https://github.com/your-org/cla-system.git)
cd cla-system
```

### **Step 2: Run the Stack**

We use a single compose file to orchestrate the entire system. The backend build utilizes **UV** to rapidly resolve Python 3.14 dependencies.

```
docker-compose up --build
```

_Wait for all containers to show "Healthy" or "Started"._

### **Step 3: Initialize the AI Model**

On the first run, you need to pull the Llama 3 model into your local Ollama container.

Open a new terminal window:

```
docker exec -it cla_llm_engine ollama run llama3
```

_This may take a few minutes depending on your internet speed (4GB download)._

### **Step 4: Access the System**

- **Frontend UI:** [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000 "null")
    
- **Backend API Docs:** [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs "null")
    
- **Neo4j Browser:** [http://localhost:7474](https://www.google.com/search?q=http://localhost:7474 "null") (User: `neo4j`, Pass: `password`)
    

## 📂 4. Repository Structure

```
cla-system/
├── docker-compose.yml          # The Master Orchestrator
├── .env                        # Environment Secrets (Not in Git)
├── backend/                    # The Python Core (Monolith)
│   ├── Dockerfile              # Multi-stage build using Astral UV + Python 3.14
│   ├── requirements.txt
│   ├── src/
│   │   ├── main.py             # API Entry Point
│   │   ├── api/                # FastAPI Routes (Endpoints)
│   │   ├── orchestrator/       # LangGraph Reasoning Logic
│   │   ├── parser/             # Logic to parse PDFs into FIDIC Structure
│   │   └── db/                 # Database Connectors (Neo4j/PG)
├── frontend/                   # The React UI
│   ├── Dockerfile
│   ├── public/
│   └── src/
├── neo4j/                      # Persistent Graph Data
└── postgres/                   # Persistent SQL Data
```

## 👥 5. Team Roles & Responsibilities

|   |   |   |
|---|---|---|
|**Role**|**Owner**|**Focus Area**|
|**Infrastructure Lead**|**Andy**|Docker, AWS, Security, CI/CD, Scrum Master|
|**Backend & AI Lead**|**Eunice**|Python Logic, LangGraph, Doc Parsing, API Dev|
|**Domain & Data Lead**|**Vince**|**FIDIC Ontology Mapping**, Policy Packs, Gold Standard Testing|

## 📅 6. Current Sprint Goals (Skeleton Build)

**Target Date:** Dec 4, 2025

1. **Infrastructure:** A runnable `docker-compose` environment on all developer machines.
    
2. **Ingestion:** A functional **Doc Parser** that extracts clauses from a PDF and maps them to the **FIDIC Graph Schema**.
    
3. **Reasoning:** A basic **LangGraph** workflow that takes a user query (e.g., "Claim for EOT"), references **FIDIC 8.4**, and returns a dummy response.
    

_For detailed documentation, architecture diagrams, and API specs, please refer to the [Project Notion Wiki]._