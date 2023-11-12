from pathlib import Path

p = Path("P:/projects")

for r in p.rglob('**/*'):
    if r.name == "hgrc":
        text = r.read_text()
        for item in text.split("\n"):
            if item.startswith("default = "):
                repo = Path(item.replace("default = ", ""))
                print(f"{repo.exists()} {str(repo)}")
