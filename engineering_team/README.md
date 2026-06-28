# EngineeringTeam Crew

Welcome to the EngineeringTeam Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.


## Features

- Multi-agent architecture using CrewAI
- Configurable agents and tasks using YAML
- Modular project structure
- Custom tool integration
- Knowledge-driven agent workflows
- Extensible architecture for new agents and tasks
- Output generation and result logging
- Unit testing support

---

## Project Structure

```text
.
├── knowledge/                 # Knowledge base used by agents
├── output/                    # Generated outputs
├── src/
│   └── coder/
│       ├── config/
│       │   ├── agents.yaml    # Agent definitions
│       │   └── tasks.yaml     # Task definitions
│       ├── tools/             # Custom tools
│       ├── crew.py            # Crew configuration
│       ├── main.py            # Entry point
│       └── __init__.py
├── tests/                     # Test cases
├── AGENTS.md                  # Agent documentation
├── pyproject.toml             # Project configuration
├── uv.lock                    # Dependency lock file
└── README.md
```

---

## Tech Stack

- Python
- CrewAI
- YAML
- UV Package Manager
- LLM APIs (OpenAI / Gemini / DeepSeek)
- Custom AI Tools

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

Install dependencies

```bash
uv sync
```

or

```bash
pip install -e .
```

---

## Configuration

Configure your API keys inside a `.env` file.

Example

```env
OPENAI_API_KEY=your_key

# or

GEMINI_API_KEY=your_key

# or

DEEPSEEK_API_KEY=your_key
```

---

## Running the Project

```bash
crewai run
```

or

```bash
python src/coder/main.py
```

---

## Customization

You can easily customize the project by modifying:

- `agents.yaml` — Agent roles, goals, and backstories
- `tasks.yaml` — Workflow and task definitions
- `tools/` — Add custom tools
- `knowledge/` — Extend the knowledge base

---

## Example Workflow

1. Load agents
2. Load tasks
3. Initialize Crew
4. Execute workflow
5. Generate results
6. Save outputs

---

## Output

Generated files and execution logs are stored in the `output/` directory.

---

## Learning Objectives

This project demonstrates:

- Multi-Agent Systems
- Agent Collaboration
- Task Orchestration
- Prompt Engineering
- CrewAI Framework
- Knowledge Integration
- Tool Calling
- AI Workflow Automation

---

## License

This project is licensed under the MIT License.

Let's create wonders together with the power and simplicity of crewAI.
