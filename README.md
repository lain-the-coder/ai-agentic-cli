# AI Agentic CLI

An autonomous code agent built with Python and Google Gemini API that can navigate codebases, read and modify files, execute Python scripts, and fix bugs through iterative reasoning loops. Implements function calling, path sandboxing, and agent feedback mechanisms to create a fully autonomous coding assistant.

## Tech Stack

**Core Technologies:**
- Python 3.13
- Google Gemini API 2.5 Flash (google-genai 1.12.1)
- python-dotenv for environment management

**Architecture:**
- Function calling with structured schemas
- Agentic feedback loop (max 20 iterations)
- Sandboxed filesystem operations
- Subprocess execution with timeout controls

## What It Does

This is a command-line AI agent that autonomously performs code operations based on natural language prompts. The agent can:

- Navigate and analyze project structures
- Read and understand source code
- Create, modify, and delete files
- Execute Python scripts with arguments
- Debug and fix code issues
- Run tests and interpret results

The agent operates through an iterative reasoning loop, calling functions as needed and processing results until it completes the requested task or reaches the iteration limit.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-agentic-cli

# Install dependencies
pip install google-genai==1.12.1 python-dotenv==1.1.0

# Configure API key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## Usage

```bash
# Basic usage
python main.py "Find and fix bugs in the calculator code"

# Verbose mode (shows function calls and token usage)
python main.py "Analyze main.py and suggest improvements" --verbose
```

## Architecture

**Agent Loop Implementation:**

The system runs an iterative feedback loop that processes natural language prompts and executes functions autonomously:

1. User submits prompt via CLI
2. Gemini analyzes request and determines required operations
3. Agent calls functions (get_files_info, get_file_content, write_file, run_python_file)
4. Results are fed back into context window
5. Loop continues until task completion or 20 iteration limit

**Function Implementations:**

All functions are exposed to the LLM through `types.FunctionDeclaration` schemas and routed through a central dispatcher:

```
get_files_info(directory)
├─ Lists directory contents with file sizes and types
├─ Uses os.listdir, os.path.getsize
└─ Path validation via os.path.commonpath

get_file_content(file_path)
├─ Reads file contents with 10,000 character limit
├─ Automatic truncation for large files
└─ Security: path normalization and validation

write_file(file_path, content)
├─ Creates or overwrites files
├─ Automatic directory creation with os.makedirs
└─ Prevents directory collision and path traversal

run_python_file(file_path, args)
├─ Executes Python scripts via subprocess.run
├─ 30-second timeout protection
├─ Captures stdout/stderr
└─ Security: .py extension validation, sandboxed working directory
```

**Security Architecture:**

Multi-layer security prevents the AI from accessing unauthorized filesystem locations:

- **Path Validation:** All paths normalized with `os.path.normpath()` and validated against working directory using `os.path.commonpath()`
- **Sandbox Enforcement:** Working directory injected automatically, cannot be overridden by AI
- **Execution Controls:** Only `.py` files can be executed, 30-second timeout on all subprocess calls
- **Resource Limits:** File reads capped at 10,000 characters to prevent context window overflow

**Gemini API Integration:**

```python
# Function schema definition
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={"file_path": types.Schema(type=types.Type.STRING)}
    )
)

# Tool registration
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

# API call with function calling enabled
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
)

# Process function calls
for function_call in response.function_calls:
    result = function_map[function_call.name](**function_call.args)
    messages.append(types.Content(
        role="user",
        parts=[types.Part.from_function_response(
            name=function_call.name,
            response={"result": result}
        )]
    ))
```

## Project Structure

```
ai-agentic-cli/
├── main.py                      # CLI entry point, agent loop
├── call_function.py             # Function routing and execution
├── prompts.py                   # System prompt configuration
├── config.py                    # Configuration constants
├── functions/
│   ├── get_files_info.py        # Directory listing with metadata
│   ├── get_file_content.py      # File reading with truncation
│   ├── write_file.py            # File creation and modification
│   └── run_python_file.py       # Python script execution
├── test_*.py                    # Unit tests for each function
└── calculator/                  # Sandbox workspace
```

## Technical Highlights

**Comprehensive Function Calling Implementation:**
- Custom schema definitions using `types.FunctionDeclaration`
- Dynamic function routing with dictionary mapping
- Structured response formatting with `types.Content` and `types.Part`
- Context window management across iterations

**Robust Error Handling:**
- API response validation (checks for None in usage_metadata, candidates, parts)
- Function execution errors returned to LLM for autonomous recovery
- Maximum iteration protection against infinite loops
- Detailed error messages for debugging

**State Management:**
- Full conversation history maintained in messages list
- Function results injected as user-role messages
- Persistent context enables multi-step reasoning
- Verbose mode for debugging shows token usage and function call details

## Testing

```bash
python test_get_files_info.py      # Directory listing, security checks
python test_get_file_content.py    # File reading, truncation, path validation
python test_write_file.py          # File creation, directory handling
python test_run_python_file.py     # Script execution, timeout, error handling
```

Tests validate normal operations, security boundaries, and edge cases.

## Example Session

```bash
$ python main.py "Find any bugs in calculator.py and fix them"

Response:
 - Calling function: get_files_info
 - Calling function: get_file_content
 - Calling function: run_python_file
 - Calling function: write_file
 - Calling function: run_python_file

Fixed division by zero bug in calculator.py. The divide function now checks 
if the denominator is zero and raises a ValueError with a clear message. 
Tests are now passing.
```

## Key Features

- **Autonomous Operation:** No human intervention required after initial prompt
- **Iterative Reasoning:** Agent can plan, execute, evaluate, and retry operations
- **Security-First Design:** Multiple layers of path validation and execution controls
- **Production-Ready Error Handling:** Comprehensive validation and graceful failure modes
- **Scalable Architecture:** Easy to add new functions by extending the function map

---

Built with Python 3.13, Google Gemini API (gemini-2.5-flash), and the google-genai SDK for production-grade function calling and conversational AI.
