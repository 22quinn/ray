import yaml
from dataclasses import dataclass, field
from typing import List
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")


@dataclass
class Depset:
    name: str
    operation: str
    requirements: List[str]
    constraints: List[str]
    output: str


@dataclass
class Config:
    depsets: List[Depset] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "Config":
        raw_depsets = data.get("depsets", [])
        depsets = [
            Depset(
                name=values.get("name"),
                requirements=values.get("requirements", []),
                constraints=values.get("constraints", []),
                operation=values.get("operation", "compile"),
                output=values.get("output"),
            )
            for values in raw_depsets
        ]

        return Config(depsets=depsets)


class Workspace:
    def __init__(self, dir: str = None):
        self.dir = (
            dir if dir is not None else os.getenv("BUILD_WORKSPACE_DIRECTORY", None)
        )
        if self.dir is None:
            raise RuntimeError("BUILD_WORKSPACE_DIRECTORY is not set")

    def load_config(self, path: str) -> Config:
        with open(os.path.join(self.dir, path), "r") as f:
            content = os.path.expandvars(f.read())
            data = yaml.safe_load(content)
            return Config.from_dict(data)
