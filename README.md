# Project Name

[![Build Status](https://github.com/username/repo/actions/workflows/main.yml/badge.svg)](https://github.com//repo/actions)

![License](https://img.shields.io/badge/license-MIT-blue)

The project is a simple multi-agent RAG application using which user can get, create, update and delete todo tasks
and interact with ChatGPT to fetch any task related learning content and summaries.
---

## TODOs
- Unit test implementation (pytest).
- CI/CD pipeline.
- Enabling Github Actions.

## 🚀 Demo
<!--
TODO
([Live Demo]&#40;https://your-demo-link.com&#41; | ![Screenshot]&#40;./assets/screenshot.png&#41;) 
 -->
---

## ✨ Features
- Open the chat-ui at localhost:8000 and start interacting with it.
- Ask chat queries like "list me all my tasks", "Add a task to build end - to - end RAG pipeline and summarize required learnings "
---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, HashiCorp Vault, Docker, OpenAI, Hugging Face
- **Storage:** Chromadb (Vector)
- **Auth:** OpenAI API token Service Token, Hugging Face API Key for creating required embeddings for Chromadb
---

## 📦 Installation
1. Clone the repo
```bash
   git clone https://github.com/syedluri/news-fetch-scheduler.git
   cd todo_crew_app
```

2. Install dependencies
```bash
   pip install -r reqirements.txt
```

3. Set up environment variables
    Dockerized and secrets are stored in HashiCorp vault in docker

4. Pre Requisites:
   Installing Docker
    ```
     Follow platform specific installation steps
    ```
   Running HashiCorp Vault on Docker
   The below instruction could be different if you are working on non-Linux operating systems
    ```
    # Run vault in Docker
    1. docker run -d --name vault-server --cap-add=IPC_LOCK -p 8200:8200 -e VAULT_DEV_ROOT_TOKEN_ID=<In local machine -> Any text should work as token> hashicorp/vault:latest
    # Setup vault CLI
    2. curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp.gpg
    # Install Vault
    3. sudo apt update && sudo apt install vault
    # Point CLI to your Vault server
    4. export VAULT_ADDR=http://localhost:8200
    5. export VAULT_TOKEN= <token created in step-1
       you can set these in .bashrc file and reload with source ~/.bashrc command
    # Store ALL your secrets in one place
    6. vault kv put secret/AI OPENAI_API_KEY=<Your openai api token key value> HF_TOKEN=<Your hugging face API key value>
    # Verify secrets stored correctly
    7. vault kv get secret/AI - make sure you got keys you stored
    8. Make sure you create a docker network with name "vault-network"
        # 8.1 Check what network your vault is on
        docker inspect vault-server --format '{{json .NetworkSettings.Networks}}'
        # 8.2 If vault has no custom network — create one
        docker network create vault-network
        # 8.3 Connect existing vault container to that network
        docker network connect vault-network vault-server
    ```
    Deploy todos-api on to docker
    ```
    sudo docker compose up --build
   
    # Make sure todos-api network name is 'todos-api_default'
        # 1 inspect current available netwroks created
         docker inspect vault-server --format '{{json .NetworkSettings.Networks}}'
        # 2 if network with given name exist, no more setup is required current configuration works
        # 3 if network not exist either take the available network and update the docker_compose.yml file or create new one similar to 8.2 and 8.3. 
    ```
5. Deploying and Running Application
```bash
    sudo -E docker compose up --build
```
---

## 🔧 Environment Variables
| Variable         | Description                | Required |
|------------------|----------------------------|----------|
| `OPENAI_API_KEY` | OpenAI API key             | ✅        |
| `HF_TOKEN`       | Hugging Face API Key       | ✅        |
| `PORT`           | Server port (default 8000) | ✅        |

---

## 📖 Usage

[//]: # Not relevant
---

## Contributing
---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author
**Srini Yedluri** — [](https://twitter.com/yourtwitter) — yedlurisrinu@gmail.com



