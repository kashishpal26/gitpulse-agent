---
name: gitpulse
description: Scans staged git diffs, catches credential leaks and debug statements, and uses open-weight Gemma models to generate semantic pull request summaries.
version: 1.0.0
license: MIT
---

# GitPulse Agent Skill

## Instructions
1. Run `python gitpulse.py audit --staged` inside any Git repository.
2. The agent evaluates git hunks for leaked secrets and debug artifacts.
3. Invokes an open-weight language model (Gemma) to write a formatted markdown changelog and pull request synopsis.