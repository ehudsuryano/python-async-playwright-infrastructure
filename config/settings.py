from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_dir = next((parent for parent in script_dir.parents if (parent / "requirements.txt").exists()), None)
reports_dir = project_dir / "reports"

DEMOQA_BASE_URL = "https://demoqa.com"
BROWSER = "chrome"
TRACE_PATH = f"{reports_dir}/performance_trace"
REPORT_PATH = reports_dir