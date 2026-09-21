from pathlib import Path

from langchain_core.tools import tool


def _safe_path(project_directory: Path, relative_path: str) -> Path:
    path = (project_directory / relative_path).resolve()
    if path != project_directory and project_directory not in path.parents:
        raise ValueError("Path must stay inside the project directory.")
    return path


def get_file_tools(project_directory: str) -> list:
    """Create tools restricted to one user-selected project directory."""
    project_root = Path(project_directory).expanduser().resolve()
    if not project_root.is_dir():
        raise NotADirectoryError(f"Project directory does not exist: {project_directory}")

    @tool
    def create_file(path: str, code: str) -> str:
        """Create a new project file. Fails when the file already exists."""
        target = _safe_path(project_root, path)
        if target.exists():
            raise FileExistsError(f"File already exists: {path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(code, encoding="utf-8")
        return f"Created {path}"

    @tool
    def edit_file_lines(path: str, start_line: int, end_line: int, replacement: str) -> str:
        """Replace an inclusive 1-based line range in an existing project file."""
        if start_line < 1 or end_line < start_line:
            raise ValueError("Line range must be 1-based and start_line <= end_line.")

        target = _safe_path(project_root, path)
        if not target.is_file():
            raise FileNotFoundError(f"File does not exist: {path}")

        lines = target.read_text(encoding="utf-8").splitlines(keepends=True)
        if end_line > len(lines):
            raise ValueError(f"Line range exceeds {path}, which has {len(lines)} lines.")

        replacement_lines = replacement.splitlines(keepends=True)
        if replacement_lines and not replacement_lines[-1].endswith(("\n", "\r")):
            replacement_lines[-1] += "\n"
        lines[start_line - 1:end_line] = replacement_lines
        target.write_text("".join(lines), encoding="utf-8")
        return f"Edited {path} lines {start_line}-{end_line}"

    @tool
    def delete_file_lines(path: str, start_line: int, end_line: int) -> str:
        """Delete an inclusive 1-based line range from an existing project file."""
        if start_line < 1 or end_line < start_line:
            raise ValueError("Line range must be 1-based and start_line <= end_line.")

        target = _safe_path(project_root, path)
        if not target.is_file():
            raise FileNotFoundError(f"File does not exist: {path}")

        lines = target.read_text(encoding="utf-8").splitlines(keepends=True)
        if end_line > len(lines):
            raise ValueError(f"Line range exceeds {path}, which has {len(lines)} lines.")

        del lines[start_line - 1:end_line]
        target.write_text("".join(lines), encoding="utf-8")
        return f"Deleted lines {start_line}-{end_line} from {path}"

    @tool
    def analyze_folder(path: str = ".") -> str:
        """List existing files in a folder relative to the project directory."""
        folder = _safe_path(project_root, path)
        if not folder.is_dir():
            raise NotADirectoryError(f"Folder does not exist: {path}")

        files = sorted(
            str(item.relative_to(project_root))
            for item in folder.rglob("*")
            if item.is_file() and "__pycache__" not in item.parts
        )
        return "\n".join(files) if files else "No files found."

    return [create_file, edit_file_lines, delete_file_lines, analyze_folder]
