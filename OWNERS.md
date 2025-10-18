# GenX FX Repository Ownership

This document outlines the ownership and maintenance structure for the GenX FX repository. Understanding this structure is crucial for collaboration, code quality, and project scaling.

## Directory Owners

The following table details the primary owners for the main directories in the repository:

| Directory | Primary Owner |
|---|---|
| `api` | @Mouy-leng |
| `core` | @A6-9V |
| `ai_models` | @A6-9V |
| `client` | @A6-9V |
| `services` | @A6-9V |
| `expert-advisors` | @Mouy-leng |
| `utils` | @A6-9V |

## Ownership Rationale

The ownership structure is based on a detailed analysis of the repository's structure, commit history, and existing `CODEOWNERS` metadata in various forks.

- **@Mouy-leng**: As the original repository owner, @Mouy-leng maintains ownership of the core API (`api`) and the critical `expert-advisors` directory.
- **@A6-9V**: As a major contributor and maintainer, @A6-9V has taken ownership of the core trading logic (`core`), the AI models (`ai_models`), the client-facing code (`client`), background services (`services`), and shared utilities (`utils`).
