from pathlib import Path
from typing import Optional

from src.tools import AsyncTool, ToolResult
from src.registry import TOOL
from src.utils.path_utils import assemble_project_path, get_project_root


@TOOL.register_module(name="file_writer_tool", force=True)
class FileWriterTool(AsyncTool):
    name = "file_writer_tool"
    description = "Writes text content to a file. Accepts absolute paths or project-relative paths. Creates parent directories if needed."
    parameters = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Target file path. Absolute or project-relative.",
            },
            "content": {
                "type": "string",
                "description": "Text content to write.",
            },
            "append": {
                "type": "boolean",
                "description": "Append to file if true; overwrite if false.",
                "default": False,
                "nullable": True,
            },
        },
        "required": ["file_path", "content"],
        "additionalProperties": False,
    }
    output_type = "any"

    def __init__(self):
        super().__init__()

    async def forward(self, file_path: str, content: str, append: Optional[bool] = False) -> ToolResult:
        try:
            # Resolve path (allow relative to project root)
            resolved = Path(assemble_project_path(file_path)).resolve()
            project_root = Path(get_project_root()).resolve()

            # Ensure the resolved path is inside the project directory for safety
            try:
                resolved.relative_to(project_root)
            except ValueError:
                return ToolResult(
                    output=None,
                    error=f"Refusing to write outside project root: {resolved}",
                )

            # Create parent dirs and write
            resolved.parent.mkdir(parents=True, exist_ok=True)
            mode = "a" if append else "w"
            with resolved.open(mode, encoding="utf-8") as f:
                f.write(content)

            return ToolResult(
                output=str(resolved),
                error=None,
            )
        except Exception as e:
            return ToolResult(
                output=None,
                error=str(e),
            )


