Сравнение папок
===============

Аналог **Synchronize Dirs** в Double Commander, но из командной строки

::

  import os
  import argparse
  from pathlib import Path
  from colorama import Fore, Style

Argparse Tutorial: 
  https://docs.python.org/3/howto/argparse.html

Argparse API: 
  https://docs.python.org/3/library/argparse.html

**Аргументы командной строки**

::

  parser = argparse.ArgumentParser(description='Compare folders.')

  parser.add_argument('alias1',
                      help='1st path to compare. Relalive to home')

  parser.add_argument('alias2',
                      help='2nd path to compare. Relalive to home')

  parser.add_argument('-home', default='.', 
                      help='Home path')

  parser.add_argument('-rel', default='', 
                      help='Constant path, relative from aliases')

  parser.add_argument('-ext', default='*', 
                      help='Extension of files to compare')

  parser.add_argument('-exclude', 
                      help='Exclude file')

  parser.add_argument("-verbose", action="store_true",
                      help="Verbose mode")

Перевести имена файлов в `Path`

::

  args = parser.parse_args()
  folder1 = os.path.join(args.home, args.alias1, args.rel)
  folder2 = os.path.join(args.home, args.alias2, args.rel)
  folder1 = Path(folder1).absolute()
  folder2 = Path(folder2).absolute()
  print(f"Folder 1: {args.alias1}")
  print(f"Folder 2: {args.alias2}")

Проверить существование папок

::

  if not os.path.exists(folder1):
      print(f"[ERROR] Folder 1 not found: {folder1}")
      exit()
  
  if not os.path.exists(folder2):
      print(f"[ERROR] Folder 2 not found: {folder1}")
      exit()

Загрузить из файла список `exclude` с окончаниями имен файлов,
которые мы исключим из сравнения

::

  exclude = None    
  if args.exclude is not None:
      with open(args.exclude, 'r') as file:
          exclude = [line.strip() for line in file]
      print(f"Exclude: {exclude}")

Начало программы

::

  print("-----------------------")

Проверить, что строка имеет одно из окончаний в массиве.

::

  def ends_with_any(s, suffix_list):
      return any(s.endswith(suffix) for suffix in suffix_list)

Сравнить 2 файла по строчкам, убрать пробелы в начале и в конце строки.

::

  def compare_files(file1_path, file2_path):
      if args.verbose:
          print('compare_files:')
          print(f'  file1: {file1_path}')
          print(f'  file2: {file2_path}')

      with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
          for line1, line2 in zip(file1, file2):
              if line1.strip() != line2.strip():
                  return False
          # Check if one file still has more lines left
          return not (next(file1, None) or next(file2, None))  

ANSI-цвета для вывода в консоль

::

  def red(s):
      return Fore.RED + Style.BRIGHT + s + Style.RESET_ALL

  def green(s):
      return Fore.GREEN + s + Style.RESET_ALL

  def blue(s):
      return Fore.BLUE + Style.BRIGHT + s + Style.RESET_ALL

Инициализация массивов для результатов

::

  equal_files = []
  not_equal_files = []
  only_in_folder1 = []
  only_in_folder2 = []
  excluded_files = []

Get all text files from both directories including subdirectories

::

  files_in_folder1 = {f for f in folder1.rglob('*.' + args.ext)}
  files_in_folder2 = {f for f in folder2.rglob('*.' + args.ext)}

  for file1 in files_in_folder1:
      relative_path = file1.relative_to(folder1)
      file2 = folder2 / relative_path
  
      if exclude is not None and ends_with_any(file1.name, exclude) :
          excluded_files.append(relative_path)
          continue

      if file2 in files_in_folder2:
          if compare_files(file1, file2): 
              equal_files.append(relative_path)
          else:
              not_equal_files.append(relative_path)
          files_in_folder2.remove(file2)
      else:
          only_in_folder1.append(relative_path)

Any remaining files in files_in_folder2 are only in folder2

::

  only_in_folder2.extend([f.relative_to(folder2) for f in files_in_folder2])

  def filter_excluded(only_in_folder2):
      result = []
      for file2 in only_in_folder2:
          if exclude is not None and ends_with_any(file2.name, exclude) :
              excluded_files.append(file2)
              continue
          else:
              result.append(file2)
      return result

  only_in_folder2 = filter_excluded(only_in_folder2)

  def printf(file):
      print(f"  - {file}")

Print the report

::

  print(f"Equal Files: {len(equal_files)}")
  # for f in equal_files:
  #     printf(f)

  if exclude is not None:
      print(f"Excluded Files: {len(excluded_files)}")

  print(red(f"\nNot Equal Files: {len(not_equal_files)}"))
  not_equal_files.sort()
  for f in not_equal_files:
      printf(f)

  print(green(f"\nOnly in {args.alias1}: {len(only_in_folder1)}"))
  only_in_folder1.sort()
  for f in only_in_folder1:
      printf(f)

  print(blue(f"\nOnly in {args.alias2}: {len(only_in_folder2)}"))
  only_in_folder2.sort()
  for f in only_in_folder2:
      printf(f)

Конец программы

::

  print("-----------------------")