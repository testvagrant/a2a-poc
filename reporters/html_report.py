from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

def render_report(out_dir: str, summary: dict, sessions: list[dict]) -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(Path(__file__).parent / 'templates')), autoescape=select_autoescape())
    tmpl = env.get_template('report.html.j2')
    html = tmpl.render(summary=summary, sessions=sessions)
    path = out / 'report.html'
    path.write_text(html, encoding='utf-8')
    return str(path)
