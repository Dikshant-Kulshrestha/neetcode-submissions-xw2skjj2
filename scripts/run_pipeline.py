"""
The orchestrator GitHub Actions actually calls. Given a git commit range,
finds every problem folder that changed, and runs generate_notes.py +
notion_sync.py for each one, sequentially (to respect API rate limits and
avoid concurrent writes to the same Notion page).


Falls back to comparing against the previous commit if --before/--after
aren't given (useful for local testing)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR_NAME = "Data Structures & Algorithms"


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    if result.returncode != 0:
        sys.exit(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout


def get_changed_files(before: str, after: str) -> list[str]:
    output = run(["git", "diff", "--name-only", before, after])
    return [line.strip() for line in output.splitlines() if line.strip()]


def extract_problem_dirs(changed_files: list[str]) -> list[Path]:
    """From changed file paths, extract unique problem folders under the
    solutions directory. Ignores files outside it (README edits, workflow
    changes, etc.) entirely, this is the cost-control filter so we never call the API on irrelevant commits."""
    problem_dirs = set()
    for f in changed_files:
        path = Path(f)
        try:
            idx = path.parts.index(SOLUTIONS_DIR_NAME)
        except ValueError:
            continue  # not under the solutions dir, skip
        # problem folder is the next path segment after the solutions dir
        if len(path.parts) > idx + 1:
            problem_dir = Path(*path.parts[: idx + 2])
            if (REPO_ROOT / problem_dir).is_dir():
                problem_dirs.add(problem_dir)
    return sorted(problem_dirs)


def run_for_problem(problem_dir: Path) -> bool:
    """Runs generate_notes.py then notion_sync.py for one problem folder.
    Returns True on success, False on failure (failures are logged but do
    NOT stop the whole batch -- one bad problem shouldn't block others in
    the same push)."""
    print(f"\n=== Processing: {problem_dir} ===")
    note_path = REPO_ROOT / "note_tmp.json"

    gen_result = subprocess.run(
        [sys.executable, "scripts/generate_notes.py",
         "--problem-dir", str(problem_dir), "--out", str(note_path)],
        cwd=REPO_ROOT,
    )
    if gen_result.returncode != 0:
        print(f"FAILED generating notes for {problem_dir}")
        return False

    sync_result = subprocess.run(
        [sys.executable, "scripts/notion_sync.py", "--input", str(note_path)],
        cwd=REPO_ROOT,
    )
    note_path.unlink(missing_ok=True)

    if sync_result.returncode != 0:
        print(f"FAILED syncing to Notion for {problem_dir}")
        return False

    print(f"OK: {problem_dir}")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", default="HEAD^", help="Commit SHA before the push")
    parser.add_argument("--after", default="HEAD", help="Commit SHA after the push")
    args = parser.parse_args()

    changed_files = get_changed_files(args.before, args.after)
    problem_dirs = extract_problem_dirs(changed_files)

    if not problem_dirs:
        print("No problem folders changed in this push. Nothing to do.")
        return

    print(f"Found {len(problem_dirs)} changed problem folder(s):")
    for d in problem_dirs:
        print(f"  - {d}")

    failures = []
    for problem_dir in problem_dirs:
        if not run_for_problem(problem_dir):
            failures.append(str(problem_dir))

    print("\n=== Summary ===")
    print(f"Succeeded: {len(problem_dirs) - len(failures)}/{len(problem_dirs)}")
    if failures:
        print(f"Failed: {failures}")
        sys.exit(1)  # non-zero exit so GitHub Actions marks the run as failed


if __name__ == "__main__":
    main()
