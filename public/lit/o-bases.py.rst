Obsidian Bases
==============

Move Markdown files in an Obsidian vault that contain a given string/pattern to a specified folder.

::

  import argparse
  import os
  import re
  import shutil
  from pathlib import Path


  def is_within(child: Path, parent: Path) -> bool:
      try:
          child.resolve().relative_to(parent.resolve())
          return True
      except ValueError:
          return False


  def safe_move(src: Path, dst_dir: Path) -> Path:
      """
      Move src into dst_dir. If a file with the same name exists, append a numeric suffix.
      Returns the final destination path.
      """
      dst_dir.mkdir(parents=True, exist_ok=True)
      target = dst_dir / src.name
      if not target.exists():
          shutil.move(str(src), str(target))
          return target

      stem = target.stem
      suffix = target.suffix
      i = 1
      while True:
          candidate = dst_dir / f"{stem} ({i}){suffix}"
          if not candidate.exists():
              shutil.move(str(src), str(candidate))
              return candidate
          i += 1


  def file_contains_pattern(
      file_path: Path,
      pattern: str,
      ignore_case: bool = True,
      use_regex: bool = False,
  ) -> bool:
      """
      Returns True if the file contains the pattern.
      - By default, treats pattern as a plain substring (not regex).
      - Set use_regex=True to interpret pattern as a regular expression.
      """
      if use_regex:
          flags = re.IGNORECASE if ignore_case else 0
          rx = re.compile(pattern, flags)
          try:
              with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                  for line in f:
                      if rx.search(line):
                          return True
          except Exception:
              return False
          return False
      else:
          needle = pattern.lower() if ignore_case else pattern
          try:
              with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                  if ignore_case:
                      for line in f:
                          if needle in line.lower():
                              return True
                  else:
                      for line in f:
                          if needle in line:
                              return True
          except Exception:
              return False
          return False


  def move_matching_markdown(
      vault_path: Path,
      pattern: str,
      target: Path,
      ignore_case: bool = True,
      use_regex: bool = False,
      dry_run: bool = False,
  ) -> None:
      """
      Move .md files under vault_path that contain pattern to target.
      - target may be absolute or relative; if relative, it's created under vault_path.
      - Skips files already inside target directory.
      """
      if not vault_path.exists() or not vault_path.is_dir():
          raise ValueError(f"Vault path does not exist or is not a directory: {vault_path}")

      # Resolve target directory: if not absolute, create inside the vault
      if not target.is_absolute():
          target = (vault_path / target).resolve()
      else:
          target = target.resolve()

      total_scanned = 0
      total_matched = 0
      total_moved = 0
      total_skipped_in_target = 0

      for md_file in vault_path.rglob("*.md"):
          if not md_file.is_file():
              continue
          # Skip files already inside the target folder
          if is_within(md_file, target):
              total_skipped_in_target += 1
              continue

          total_scanned += 1

          if file_contains_pattern(md_file, pattern, ignore_case=ignore_case, use_regex=use_regex):
              total_matched += 1
              if dry_run:
                  relative_path = md_file.relative_to(vault_path)
                  print(f"[DRY-RUN] {relative_path}")
              else:
                  final_path = safe_move(md_file, target)
                  print(f"Moved: {md_file} -> {final_path}")
                  total_moved += 1

      print("\nSummary:")
      print(f"  Scanned .md files: {total_scanned}")
      print(f"  Matched pattern:   {total_matched}")
      print(f"  Moved files:       {total_moved}{' (dry-run)' if dry_run else ''}")
      print(f"  Already in target: {total_skipped_in_target}")
      print(f"  Target directory:  {target}")

Parse arguments

::

  def parse_args() -> argparse.Namespace:
      parser = argparse.ArgumentParser(
          description="Move Markdown files in an Obsidian vault that contain a given string/pattern to a specified folder."
      )
      parser.add_argument(
          "--vault",
          required=True,
          type=Path,
          help='Path to your Obsidian vault directory (e.g., "/path/to/ObsidianVault").',
      )
      parser.add_argument(
          "--pattern",
          required=True,
          type=str,
          help='String to search for in files (default: plain substring; use --regex for regex). Example: "ipqs".',
      )
      parser.add_argument(
          "--target",
          required=True,
          type=Path,
          help='Target folder to move matched files into. If relative (e.g., "ipqs"), it will be created under the vault.',
      )
      parser.add_argument(
          "--case-sensitive",
          action="store_true",
          help="Make the search case-sensitive (default is case-insensitive).",
      )
      parser.add_argument(
          "--regex",
          action="store_true",
          help="Treat pattern as a regular expression (default is plain substring).",
      )
      parser.add_argument(
          "--dry-run",
          action="store_true",
          help="Show what would be moved without making changes.",
      )
      return parser.parse_args()


  if __name__ == "__main__":
      args = parse_args()
      move_matching_markdown(
          vault_path=args.vault,
          pattern=args.pattern,
          target=args.target,
          ignore_case=not args.case_sensitive,
          use_regex=args.regex,
          dry_run=args.dry_run,
      )

  """
  Examples:

  1) Move all .md files containing 'ipqs' (case-insensitive) into an 'ipqs' folder inside the vault:
     python script.py --vault "/path/to/ObsidianVault" --pattern "ipqs" --target "ipqs"

  2) Dry-run (no changes):
     python script.py --vault "/path/to/ObsidianVault" --pattern "ipqs" --target "ipqs" --dry-run

  3) Using a regex pattern (case-insensitive):
     python script.py --vault "/path/to/ObsidianVault" --pattern "\\bipqs\\b" --target "ipqs" --regex
  """