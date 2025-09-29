_base_ = './base.py'

# Codegen Config (minimal, no MCP, no image/video tools)
tag = "codegen"
concurrency = 1
workdir = "workdir"
log_path = "log.txt"
use_local_proxy = False  # True for local proxy, False for public proxy

use_hierarchical_agent = False

general_agent_config = dict(
    type="general_agent",
    name="codegen_agent",
    model_id="gpt-oss:20b",
    description="A minimal agent for simple code generation via python interpreter.",
    max_steps=10,
    template_path="src/agent/general_agent/prompts/general_agent.yaml",
    provide_run_summary=True,
    tools=["python_interpreter_tool", "file_writer_tool"],
    mcp_tools=[],
)

# Select the minimal agent
agent_config = general_agent_config

# Disable MCP servers entirely to avoid optional dependency errors
mcp_tools_config = dict(
    _delete_=True,
    mcpServers={}
)


