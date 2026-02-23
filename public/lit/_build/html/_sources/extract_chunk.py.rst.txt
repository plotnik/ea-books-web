Log Chunk
=========

::

  import argparse
  import os
  import sys


  def truncate_filename(filename: str, max_length: int = 16) -> str:
      """
      Truncate filename (without extension) to max_length characters.
      """
      base = os.path.basename(filename)
      name, _ = os.path.splitext(base)
      return name[:max_length]


  def extract_chunk(source_file: str, start: int, number: int) -> str:
      """
      Extract a chunk of lines from source_file starting at 'start'
      and taking 'number' lines.
      Returns the output file name.
      """
      if start < 0:
          raise ValueError("Start line cannot be negative")
      if number <= 0:
          raise ValueError("Number of lines must be positive")

      output_base = truncate_filename(source_file)
      output_file = f"chunk-{output_base}.log"

      with open(source_file, "r", encoding="utf-8", errors="replace") as src:
          with open(output_file, "w", encoding="utf-8") as dst:
              for current_line_number, line in enumerate(src):
                  if current_line_number < start:
                      continue
                  if current_line_number >= start + number:
                      break
                  dst.write(line)

      return output_file


  def main():
      parser = argparse.ArgumentParser(
          description="Extract a chunk of lines from a log file."
      )

      parser.add_argument(
          "logfile",
          help="Path to the source log file"
      )

      parser.add_argument(
          "-s", "--start",
          type=int,
          default=0,
          help="Start line (0-based). Default: 0"
      )

      parser.add_argument(
          "-n", "--number",
          type=int,
          default=100,
          help="Number of lines to extract. Default: 100"
      )

      args = parser.parse_args()

      if not os.path.isfile(args.logfile):
          print(f"Error: File not found: {args.logfile}", file=sys.stderr)
          sys.exit(1)

      try:
          output_file = extract_chunk(args.logfile, args.start, args.number)
          print(f"Chunk written to: {output_file}")
      except Exception as e:
          print(f"Error: {e}", file=sys.stderr)
          sys.exit(1)


  if __name__ == "__main__":
      main()
