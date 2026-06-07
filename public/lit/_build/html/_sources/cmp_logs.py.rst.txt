Compare Logs
============

Compare two log files produced by the same code by matching configurable
signature substrings.

**Overview**

The script reads signature substrings from ``cmp_logs.txt``. Each non-empty line
in that file is treated as one signature.

Starting from the current position in both logs, the script searches for the next
occurrence of any configured signature in each file. The next matching signature
must be the same in both logs. 

If the signatures are different, the script prints a warning in the console 
and tries to resynchronize using a signature from the first file.

For each comparison step, the script creates a block from each log. A block
includes all lines from the current position through the line containing the
matched signature.

The resulting blocks are written side by side to an HTML report. The report uses
different highlighting for each log and additional highlighting for signature
occurrences.

**Usage**

.. code-block:: console

   python cmp_logs.py log1.txt log2.txt
   python cmp_logs.py log1.txt log2.txt -o cmp_logs.html -s cmp_logs.txt 

**Options**

``-o cmp_logs.html``
   Path to the generated HTML comparison report.

``-s cmp_logs.txt``
   Path to the signature file. Each non-empty line is treated as a signature
   substring.

----

::

  from __future__ import annotations

  import argparse
  import html
  import sys
  from dataclasses import dataclass
  from pathlib import Path
  from typing import Iterable

.. class:: SignatureHit

::

  @dataclass(frozen=True)
  class SignatureHit:
      signature: str
      line_index: int      # 0-based line index in the original log
      signature_index: int # 0-based index in the signatures file

.. class:: BlockPair

::

  @dataclass(frozen=True)
  class BlockPair:
      block_no: int
      signature: str | None
      signature_index: int | None
      log1_start_line: int
      log1_end_line: int
      log2_start_line: int
      log2_end_line: int
      log1_lines: list[str]
      log2_lines: list[str]

.. class:: LogCompareError(RuntimeError)

::

  class LogCompareError(RuntimeError):
      pass

.. function:: read_lines(path: Path) -> list[str]

::

  def read_lines(path: Path) -> list[str]:
      try:
          return path.read_text(encoding="utf-8", errors="replace").splitlines()
      except OSError as exc:
          raise LogCompareError(f"Could not read {path}: {exc}") from exc

.. function:: read_signatures(path: Path) -> list[str]

::

  def read_signatures(path: Path) -> list[str]:
      signatures = []
      try:
          raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
      except OSError as exc:
          raise LogCompareError(f"Could not read signatures file {path}: {exc}") from exc

      for line in raw_lines:
          sig = line.strip()
          if sig and not sig.startswith("#"):
              signatures.append(sig)

      if not signatures:
          raise LogCompareError(f"No signatures found in {path}")

      return signatures

.. function:: find_next_signature(lines: list[str], start_index: int, signatures: list[str]) -> SignatureHit | None

::

  def find_next_signature(
      lines: list[str],
      start_index: int,
      signatures: list[str],
  ) -> SignatureHit | None:
      """
      Return the earliest signature hit at or after start_index.

      If multiple signatures occur on the same line, the signature that appears
      earliest in the line is preferred. If still tied, the earlier signature in
      cmp_logs.txt is preferred.
      """
      best: tuple[int, int, int, str] | None = None
      # tuple is: line_index, char_position, signature_index, signature

      for line_index in range(start_index, len(lines)):
          line = lines[line_index]
          for signature_index, signature in enumerate(signatures):
              char_position = line.find(signature)
              if char_position >= 0:
                  candidate = (line_index, char_position, signature_index, signature)
                  if best is None or candidate[:3] < best[:3]:
                      best = candidate

          # Once a hit is found on this line, no later line can be earlier.
          if best is not None and best[0] == line_index:
              return SignatureHit(
                  signature=best[3],
                  line_index=best[0],
                  signature_index=best[2],
              )

      return None

.. function:: compare_logs(log1_lines: list[str], log2_lines: list[str], signatures: list[str]) -> list[BlockPair]

::

  def compare_logs(
      log1_lines: list[str],
      log2_lines: list[str],
      signatures: list[str],
  ) -> list[BlockPair]:
      blocks: list[BlockPair] = []
      pos1 = 0
      pos2 = 0
      block_no = 1

      while pos1 < len(log1_lines) or pos2 < len(log2_lines):
          hit1 = find_next_signature(log1_lines, pos1, signatures)
          hit2 = find_next_signature(log2_lines, pos2, signatures)

          if hit1 is None and hit2 is None:
              # Remaining tail after the final signature.
              if pos1 < len(log1_lines) or pos2 < len(log2_lines):
                  blocks.append(
                      BlockPair(
                          block_no=block_no,
                          signature=None,
                          signature_index=None,
                          log1_start_line=pos1 + 1,
                          log1_end_line=len(log1_lines),
                          log2_start_line=pos2 + 1,
                          log2_end_line=len(log2_lines),
                          log1_lines=log1_lines[pos1:],
                          log2_lines=log2_lines[pos2:],
                      )
                  )
              break

          if hit1 is None or hit2 is None:
              # One log has no further signature while the other still has one.
              # Put the remaining lines from BOTH logs into a final block.
              blocks.append(
                  BlockPair(
                      block_no=block_no,
                      signature=None,
                      signature_index=None,
                      log1_start_line=pos1 + 1,
                      log1_end_line=len(log1_lines),
                      log2_start_line=pos2 + 1,
                      log2_end_line=len(log2_lines),
                      log1_lines=log1_lines[pos1:],
                      log2_lines=log2_lines[pos2:],
                  )
              )
              break

          if hit1.signature != hit2.signature:
              print(f"Signatures differ: {hit1.signature} != {hit2.signature} in block {block_no}")
              # Signatures differ — try to synchronize by searching log2
              # for hit1.signature.
              synced_hit2: SignatureHit | None = None
              for line_index in range(pos2, len(log2_lines)):
                  if hit1.signature in log2_lines[line_index]:
                      synced_hit2 = SignatureHit(
                          signature=hit1.signature,
                          line_index=line_index,
                          signature_index=hit1.signature_index,
                      )
                      break

              if synced_hit2 is None:
                  # hit1.signature not found in log2 — dump remainder as tail.
                  blocks.append(
                      BlockPair(
                          block_no=block_no,
                          signature=None,
                          signature_index=None,
                          log1_start_line=pos1 + 1,
                          log1_end_line=len(log1_lines),
                          log2_start_line=pos2 + 1,
                          log2_end_line=len(log2_lines),
                          log1_lines=log1_lines[pos1:],
                          log2_lines=log2_lines[pos2:],
                      )
                  )
                  break

              hit2 = synced_hit2
        
          # if hit1 is None:
          #     raise LogCompareError(
          #         "Log 1 has no further signature, but Log 2 found "
          #         f"signature #{hit2.signature_index + 1} on line {hit2.line_index + 1}: "
          #         f"{hit2.signature!r}"
          #     )

          # if hit2 is None:
          #     raise LogCompareError(
          #         "Log 2 has no further signature, but Log 1 found "
          #         f"signature #{hit1.signature_index + 1} on line {hit1.line_index + 1}: "
          #         f"{hit1.signature!r}"
          #     )
    
          # if hit1.signature != hit2.signature:
          #     raise LogCompareError(
          #         "Next signatures differ:\n"
          #         f"  Log 1: signature #{hit1.signature_index + 1} "
          #         f"on line {hit1.line_index + 1}: {hit1.signature!r}\n"
          #         f"  Log 2: signature #{hit2.signature_index + 1} "
          #         f"on line {hit2.line_index + 1}: {hit2.signature!r}"
          #     )

          blocks.append(
              BlockPair(
                  block_no=block_no,
                  signature=hit1.signature,
                  signature_index=hit1.signature_index,
                  log1_start_line=pos1 + 1,
                  log1_end_line=hit1.line_index + 1,
                  log2_start_line=pos2 + 1,
                  log2_end_line=hit2.line_index + 1,
                  log1_lines=log1_lines[pos1 : hit1.line_index + 1],
                  log2_lines=log2_lines[pos2 : hit2.line_index + 1],
              )
          )

          pos1 = hit1.line_index + 1
          pos2 = hit2.line_index + 1
          block_no += 1

      return blocks

.. function:: highlight_signatures(text: str, signatures: Iterable[str]) -> str

::

  def highlight_signatures(text: str, signatures: Iterable[str]) -> str:
      """
      Escape text for HTML and wrap signature occurrences in <mark>.

      This intentionally uses substring matching, same as comparison.
      Longer signatures are applied first to reduce nested/partial highlighting.
      """
      escaped = html.escape(text)

      # Work on escaped signatures because the text has already been escaped.
      escaped_signatures = sorted(
          {html.escape(sig) for sig in signatures if sig},
          key=len,
          reverse=True,
      )

      for sig in escaped_signatures:
          escaped = escaped.replace(sig, f'<mark class="signature">{sig}</mark>')

      return escaped

.. function:: render_lines(lines: list[str], first_line_no: int, signatures: list[str]) -> str

::

  def render_lines(lines: list[str], first_line_no: int, signatures: list[str]) -> str:
      if not lines:
          return '<div class="empty">(no lines)</div>'

      rendered = []
      width = len(str(first_line_no + len(lines) - 1))

      for offset, line in enumerate(lines):
          line_no = first_line_no + offset
          rendered_line = highlight_signatures(line, signatures)
          rendered.append(
              '<div class="log-line">'
              f'<span class="line-no">{line_no:>{width}}</span>'
              f'<span class="line-text">{rendered_line}</span>'
              '</div>'
          )

      return "\n".join(rendered)

.. function:: render_html(blocks: list[BlockPair], log1_path: Path, log2_path: Path, signatures_path: Path, signatures: list[str]) -> str

::

  def render_html(
      blocks: list[BlockPair],
      log1_path: Path,
      log2_path: Path,
      signatures_path: Path,
      signatures: list[str],
  ) -> str:
      total_signature_blocks = sum(1 for block in blocks if block.signature is not None)

      block_html = []
      for block in blocks:
          if block.signature is None:
              title = f"Block {block.block_no}: tail after final signature"
              sig_meta = "..."
          else:
              title = f"Block {block.block_no}"
              sig_meta = (
                  '<div class="signature-title">'
                  f'Signature: {html.escape(block.signature)}'
                  '</div>'
              )

          block_class = "block tail-block" if block.signature is None else "block"

          block_html.append(
              f'''
  <section class="{block_class}">
    <header class="block-header">
      <div>
        <h2>{html.escape(title)}</h2>
        {sig_meta}
      </div>
      <!--a href="#top">top</a-->
    </header>

    <div class="columns">
      <article class="panel log1">
        <h3>{html.escape(log1_path.name)}: lines {block.log1_start_line}-{block.log1_end_line}</h3>
        <pre>{render_lines(block.log1_lines, block.log1_start_line, signatures)}</pre>
      </article>

      <article class="panel log2">
        <h3>{html.escape(log2_path.name)}: lines {block.log2_start_line}-{block.log2_end_line}</h3>
        <pre>{render_lines(block.log2_lines, block.log2_start_line, signatures)}</pre>
      </article>
    </div>
  </section>
  '''
          )

      return f'''<!doctype html>
  <html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Log comparison: {html.escape(log1_path.name)} vs {html.escape(log2_path.name)}</title>
    <style>
      :root {{
        --bg: #f6f8fa;
        --text: #1f2328;
        --muted: #57606a;
        --border: #d0d7de;
        --log1-bg: #eef6ff;
        --log1-border: #9ec5fe;
        --log2-bg: #fff3e6;
        --log2-border: #ffc078;
        --signature-bg: #ffeb3b;
        --signature-text: #111;
        --header-bg: #ffffff;
      }}

      body {{
        margin: 0;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: var(--bg);
        color: var(--text);
      }}

      header.page-header {{
        position: sticky;
        top: 0;
        z-index: 10;
        background: var(--header-bg);
        border-bottom: 1px solid var(--border);
        padding: 16px 24px;
      }}

      h1 {{
        margin: 0 0 8px;
        font-size: 22px;
      }}

      .meta {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        color: var(--muted);
        font-size: 14px;
      }}

      main {{
        padding: 20px 24px 40px;
      }}

      .block {{
        margin: 0 0 24px;
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
        background: white;
        box-shadow: 0 1px 2px rgba(31, 35, 40, 0.06);
      }}

      .block-header {{
        display: flex;
        justify-content: space-between;
        gap: 16px;
        align-items: flex-start;
        border-bottom: 1px solid var(--border);
        padding: 14px 16px;
        background: #ffffff;
      }}

      .block-header h2 {{
        margin: 0 0 6px;
        font-size: 17px;
      }}

      .signature-title {{
        font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
        font-size: 13px;
        color: var(--muted);
        word-break: break-word;
      }}

      .columns {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0;
        align-items: stretch;
      }}

      .panel {{
        min-width: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
      }}

      .panel h3 {{
        position: sticky;
        top: 75px;
        z-index: 5;
        margin: 0;
        padding: 10px 12px;
        font-size: 14px;
        border-bottom: 1px solid var(--border);
      }}

      .log1 {{
        background: var(--log1-bg);
        border-right: 1px solid var(--border);
      }}

      .log1 h3 {{
        background: var(--log1-bg);
        border-left: 4px solid var(--log1-border);
      }}

      .log2 {{
        background: var(--log2-bg);
      }}

      .log2 h3 {{
        background: var(--log2-bg);
        border-left: 4px solid var(--log2-border);
      }}

      pre {{
        margin: 0;
        padding: 12px;
        overflow-x: hidden;
        overflow-y: auto;
        font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
        font-size: 12px;
        line-height: 1.45;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        word-break: break-word;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
      }}

      .log-line {{
        display: flex;
        gap: 12px;
      }}

      .line-no {{
        user-select: none;
        color: var(--muted);
        text-align: right;
        flex: 0 0 auto;
        border-right: 1px solid rgba(0, 0, 0, 0.12);
        padding-right: 8px;
      }}

      .line-text {{
        min-width: 0;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        word-break: break-word;
      }}

      mark.signature {{
        background: var(--signature-bg);
        color: var(--signature-text);
        padding: 0 2px;
        border-radius: 3px;
        font-weight: 700;
      }}

      .tail-block pre {{
        justify-content: flex-start;
      }}

      .empty {{
        color: var(--muted);
        font-style: italic;
      }}

      a {{
        color: #0969da;
        text-decoration: none;
      }}

      a:hover {{
        text-decoration: underline;
      }}

      @media (max-width: 900px) {{
        .columns {{
          grid-template-columns: 1fr;
        }}

        .log1 {{
          border-right: 0;
          border-bottom: 1px solid var(--border);
        }}

        .panel h3 {{
          position: static;
        }}
      }}
    </style>
  </head>
  <body>
    <header id="top" class="page-header">
      <h1>Log comparison</h1>
      <div class="meta">
        <span><strong>Log 1:</strong> {html.escape(str(log1_path))}</span>
        <span><strong>Log 2:</strong> {html.escape(str(log2_path))}</span>
        <span><strong>Signatures:</strong> {html.escape(str(signatures_path))}</span>
        <span><strong>Matched signature blocks:</strong> {total_signature_blocks}</span>
        <span><strong>Total blocks:</strong> {len(blocks)}</span>
      </div>
    </header>

    <main>
      {''.join(block_html)}
    </main>
  </body>
  </html>
  '''

.. function:: parse_args(argv: list[str]) -> argparse.Namespace

::

  def parse_args(argv: list[str]) -> argparse.Namespace:
      parser = argparse.ArgumentParser(
          description="Compare two logs using signature substrings and write an HTML report."
      )
      parser.add_argument("log1", type=Path, help="First log file")
      parser.add_argument("log2", type=Path, help="Second log file")
      parser.add_argument(
          "-s",
          "--signatures",
          type=Path,
          default=Path("cmp_logs.txt"),
          help="Signature file, one substring per line. Default: cmp_logs.txt",
      )
      parser.add_argument(
          "-o",
          "--output",
          type=Path,
          default=Path("cmp_logs.html"),
          help="Output HTML file. Default: cmp_logs.html",
      )
      return parser.parse_args(argv)

.. function:: main(argv: list[str]) -> int

::

  def main(argv: list[str]) -> int:
      args = parse_args(argv)

      try:
          log1_lines = read_lines(args.log1)
          log2_lines = read_lines(args.log2)
          signatures = read_signatures(args.signatures)
          blocks = compare_logs(log1_lines, log2_lines, signatures)
          report = render_html(blocks, args.log1, args.log2, args.signatures, signatures)
          args.output.write_text(report, encoding="utf-8")
      except LogCompareError as exc:
          print(f"ERROR: {exc}", file=sys.stderr)
          return 2
      except OSError as exc:
          print(f"ERROR: Could not write output file {args.output}: {exc}", file=sys.stderr)
          return 2

      print(f"Wrote {args.output}")
      print(f"Blocks: {len(blocks)}")
      print(f"Signature blocks: {sum(1 for block in blocks if block.signature is not None)}")
      return 0


  if __name__ == "__main__":
      raise SystemExit(main(sys.argv[1:]))
