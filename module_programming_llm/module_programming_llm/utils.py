
def add_line_numbers(content: str):
    lines = content.splitlines()
    padding = len(str(len(lines)))
    return "\n".join([f"{i+1:>{padding}} {line}" for i, line in enumerate(lines)])