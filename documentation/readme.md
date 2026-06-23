
# Devops Documentation

This is the folder contains the documentation required to implement or to make changes in the devops practices of the current repo.

## Project Description

So basically this is an simple chatbot application with document upload capabilities.**This project is built using python entierly and frameworks used is *fastapi*, streamlit there is also requirement file with dependencies to run this project**


## Structure

- runbooks/ → Step-by-step operational procedures
- cicd/ → CI/CD pipelines and workflows
-  *security-implemented.md* security steps in implemented



## Repository File Structure

```text
Chatbot/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── backend/
│   ├── routers/
│   ├── services/
│   ├── tests/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── requirements.txt
├── documentation/
│   └── README.md
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── azure-pipelines.yml
├── docker-compose.yml
└── README.md
```

## Environment

- Development
- Staging
- Production

## Main Technologies

- Docker
- GitHub Actions
- azure
- Git

## Tech stack
- Frontend: React
- Backend: FastAPI
- Database: SQLite
- Authentication: JWT
- Vector Store: ChromaDB
- LLM: Gemini