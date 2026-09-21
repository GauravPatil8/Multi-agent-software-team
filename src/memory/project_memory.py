import json
import sqlite3
from pathlib import Path
from typing import Any


MEMORY_DIRECTORY = ".agents"
MEMORY_FILE = "project_memory.db"
LEGACY_MEMORY_DIRECTORY = ".agent"


def _memory_path(project_directory: str) -> Path:
    project_root = Path(project_directory).expanduser().resolve()
    return project_root / MEMORY_DIRECTORY / MEMORY_FILE


def _memory_paths(project_directory: str) -> list[Path]:
    project_root = Path(project_directory).expanduser().resolve()
    return [
        project_root / MEMORY_DIRECTORY / MEMORY_FILE,
        project_root / LEGACY_MEMORY_DIRECTORY / MEMORY_FILE,
    ]


def load_project_memory(project_directory: str) -> dict[str, Any]:
    project_root = str(Path(project_directory).expanduser().resolve())
    for path in _memory_paths(project_directory):
        if not path.is_file():
            continue
        with sqlite3.connect(path) as connection:
            _create_schema(connection)
            row = connection.execute(
                "SELECT memory FROM project_memory WHERE project_directory = ?",
                (project_root,),
            ).fetchone()
        if row is not None:
            return json.loads(row[0])
    return {}


def save_project_memory(project_directory: str, state: dict[str, Any]) -> None:
    path = _memory_path(project_directory)
    path.parent.mkdir(parents=True, exist_ok=True)
    memory = {
        "requirement": state.get("requirement"),
        "architecture": state.get("architecture"),
        "research": state.get("research"),
        "implementation": state.get("implementation"),
        "review": state.get("review"),
        "qa": state.get("qa"),
    }
    project_root = str(Path(project_directory).expanduser().resolve())
    with sqlite3.connect(path) as connection:
        _create_schema(connection)
        connection.execute(
            """
            INSERT INTO project_memory (project_directory, memory)
            VALUES (?, ?)
            ON CONFLICT(project_directory) DO UPDATE SET
                memory = excluded.memory,
                updated_at = CURRENT_TIMESTAMP
            """,
            (project_root, json.dumps(memory, default=str)),
        )


def _create_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS project_memory (
            project_directory TEXT PRIMARY KEY,
            memory TEXT NOT NULL,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
