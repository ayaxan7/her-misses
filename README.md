# Hermes Work Automation

An AI-powered, agent-based work-log automation system built using [Hermes Agent](https://github.com/NousResearch/hermes-agent) and deployed on AWS EC2. It uses Telegram as the primary interface to automate daily reporting and updates to Google Sheets and Google Docs.

## Overview

Hermes Work Automation reduces the effort involved in maintaining daily work logs by combining AI-driven task summarization, GitHub activity tracking, and Google Workspace integration.

The system is designed to:
- Collect development activity from explicitly allowlisted GitHub repositories.
- Generate professional daily work-log proposals using an AI agent.
- Deliver proposals through a Telegram bot for review and approval.
- Maintain daily work logs in Google Sheets and detailed reports in Google Docs.
- Generate a copyable email draft containing concise technical updates without sending emails automatically.

## Architecture

```text
GitHub Repositories
        |
        v
 GitHub Activity Collector
        |
        v
    Hermes Agent
  (AWS EC2 / Ubuntu)
        |
        v
   Telegram Bot
        |
   User Review
  /      |      \
Approve  Edit   Skip
  |       |
  +-------+
      |
      v
 Google Workspace
   /          \
Sheets       Docs
      |
      v
 Email Draft
 (Telegram only)
```

## Key Features

### 1. GitHub Activity Tracking
- Collects commit activity from configured repositories using GitHub CLI and the GitHub API.
- Uses an explicit repository allowlist.
- Retrieves activity remotely without cloning project source repositories onto EC2.

### 2. AI-Powered Work-Log Generation
- Converts development activity into concise, professional work-log descriptions.
- Generates detailed reports with overviews, implementation steps, challenges, and solutions.
- Avoids inventing technical accomplishments when there is insufficient activity information.

### 3. Telegram-Based Approval
- Sends daily work-log proposals through a Telegram bot.
- Supports three actions:
  - `approve` — approve the proposed entry.
  - `edit: <changes>` — request modifications.
  - `skip` — discard the proposal.
- Keeps the user involved in the reporting workflow.

### 4. Google Workspace Integration
- **Google Sheets:** Maintains a structured monthly work log.
- **Google Docs:** Maintains detailed daily development reports.
- **Google Drive:** Organizes reports in the `Hermes Work Reports` folder.

The spreadsheet uses the following columns:

| Column | Description |
| --- | --- |
| A | Date |
| B | Task Title |
| C | Description |
| D | Existing user-managed data |

Automated updates are intended to modify columns A–C while preserving column D.

### 5. Automated Scheduling
- Runs the daily work-log workflow at 7:00 PM IST, Monday through Saturday.
- Skips Sundays.
- Creates a new monthly spreadsheet and detailed report document as required.

### 6. Email Draft Generation
- Generates a concise email containing approximately 3–6 technical update bullets.
- Includes the draft in the Telegram proposal for easy copying.
- Does not send emails automatically.

## Technology Stack

| Component | Technology |
| --- | --- |
| AI Agent | Hermes Agent |
| Hosting | AWS EC2 |
| Operating System | Ubuntu |
| Interaction | Telegram Bot |
| Programming Language | Python |
| Version Control | Git, GitHub CLI |
| Activity Source | GitHub API |
| Spreadsheet | Google Sheets API |
| Documentation | Google Docs API |
| File Management | Google Drive API |
| Scheduling | Hermes Cron |

## Repository Structure

```text
hermes-work-automation/
├── config/
│   └── github_allowed_repos.example.txt
├── scripts/
│   └── github_worklog_collect.py
├── .gitignore
└── README.md
```

## Setup

### Prerequisites
- An Ubuntu-based AWS EC2 instance
- Hermes Agent installed and configured
- Python 3
- GitHub CLI (`gh`)
- A Telegram bot
- Google Workspace API credentials with the required permissions

### 1. Clone the repository

```bash
git clone https://github.com/ayaxan7/hermes-work-automation.git
cd hermes-work-automation
```

### 2. Configure GitHub access

Authenticate the GitHub CLI:

```bash
gh auth login
```

Configure the repository allowlist using the example file in `config/`. Add only the repositories that the collector is permitted to inspect.

### 3. Configure integrations

Configure the Telegram bot and Google Workspace integration through Hermes Agent. Keep all credentials, OAuth tokens, and private configuration files outside the repository.

### 4. Configure scheduling

Set up the Hermes cron job to run the work-log workflow at 7:00 PM IST, Monday through Saturday. Configure Telegram delivery and ensure that report modifications require the appropriate approval.

## Security

- Never commit API keys, OAuth tokens, Telegram bot tokens, SSH private keys, or other credentials.
- Use least-privilege GitHub access.
- Restrict GitHub activity collection to explicitly allowlisted repositories.
- Keep server-specific configuration outside the public repository.
- Enforce approval checks at the tool-permission level rather than relying solely on AI prompts.

## Current Scope

The repository contains the GitHub activity collector and an example repository allowlist. The complete automation also relies on the separately configured Hermes Agent runtime and its integrations on EC2.

## License

No license has been specified yet.
