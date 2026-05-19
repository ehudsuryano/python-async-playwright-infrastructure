from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_dir = next((parent for parent in script_dir.parents if (parent / "requirements.txt").exists()), None)
reports_dir = project_dir / "reports"

DEMOQA_BASE_URL = "https://demoqa.com"
DEMOQA_API_BASE_URL = "https://demoqa.com"
API_DEFAULT_TIMEOUT_MS = 15000
BROWSER = "chrome"
TRACE_PATH = f"{reports_dir}/performance_trace"
REPORT_PATH = reports_dir