from dataclasses import dataclass


@dataclass
class MethodNode:
    start_line: int
    stop_line: int
    source_code: str
    name: str

    def __str__(self):
        return f"MethodNode({self.name}, lines {self.start_line} to {self.stop_line})"
