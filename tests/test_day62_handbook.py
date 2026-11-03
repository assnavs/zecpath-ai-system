from pathlib import Path

def test_handbook_covers_required_sections():
    text=Path("docs/day62/zecpath_ai_technical_handbook.md").read_text(encoding="utf-8")
    for term in ("Architecture","Scoring logic","API","Data models","Local setup","Developer workflow","Known limitations"):
        assert term.lower() in text.lower()
