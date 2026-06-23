# Branching Strategy

## Purpose

This document describes the branching workflow used during development.

---

## Workflow

Development follows a feature branch model.

eg:


```text
main
  │
  ├── feature/auth-improvements
  ├── feature/rag-upload
  ├── feature/chat-history
  └── feature/security-scans
```

Each new feature or enhancement is developed in an isolated branch before being merged into the main branch.

---

## Development Flow

```text
Create Feature Branch
        ↓  
Implement Changes
        ↓
Push Changes
        ↓
CI Pipeline Executes
        ↓
Open Pull Request
        ↓
Code Review
        ↓
Merge into main
```

---

## Branch Naming Convention

Feature branches follow the format:

```text
feature/<feature-name>
```

Examples:

- feature/rag-upload
- feature/auth-refactor
- feature/security-scans

---

## Main Branch

The `main` branch represents the stable version of the application.

Direct commits to `main` should be avoided. Changes are introduced through pull requests after CI validation.

---

## CI Validation

Every push triggers automated checks, including:

- Code linting
- Formatting validation
- Security scanning
- Dependency vulnerability checks
- Automated tests

---

## Future Improvements

Planned enhancements include:

- Development environment branch
- Staging deployment workflow
- Production release process
- Release tagging strategy


