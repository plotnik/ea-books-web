Time Intervals
==============

*Process Time Intervals and Group by Task Code*

This script is used to process a list of time intervals, load the data into a Pandas DataFrame, calculate the duration of each interval, and group the intervals by task code.

Input Data Format
-----------------

The input data is a string containing a list of time intervals. Each time interval is formatted as follows:

.. code-block:: text

   {end_date_and_time}
   ; {task_code} {comment}
   {start_date_and_time}

Where:

*   ``{end_date_and_time}``:  The date and time when the task ended, in ``DD.MM.YYYY HH:MM:SS`` format (e.g., ``24.03.2025 23:29:38``).
*   ``{task_code}``: A unique identifier for the task (e.g., ``TASK-1234``).
*   ``{comment}``: A brief description of the task (e.g., ``Estimate new features``).
*   ``{start_date_and_time}``: The date and time when the task started, in ``DD.MM.YYYY HH:MM:SS`` format (e.g., ``24.03.2025 22:50:13``).

Example Input
-------------

.. code-block:: text

   24.03.2025 23:29:38
   ; TASK-1234 Estimate new features
   24.03.2025 22:50:13

   25.03.2025 10:15:00
   ; TASK-1234 Implement feature A
   25.03.2025 09:00:00

   26.03.2025 12:00:00
   ; TASK-5678 Bug fixing
   26.03.2025 11:00:00


Expected Output
---------------

The expected output is a Pandas DataFrame grouped by ``task_code``.  Optionally, the output can include aggregated duration statistics for each task code.

Processing Steps
----------------

::

  import streamlit as st
  import pandas as pd
  import re
  from datetime import datetime
  import yaml 
  import os

  st.set_page_config(
      page_title="T-Int",
      layout="wide",
  )

Print banner

::
    
  @st.cache_data
  def print_banner():
      print("""
      .___________.       __  .__   __. .___________.        
      |           |      |  | |  \\ |  | |           |       
      `---|  |----`______|  | |   \\|  | `---|  |----`       
          |  |    |______|  | |  . `  |     |  |             
          |  |           |  | |  |\\   |     |  |            
          |__|           |__| |__| \\__|     |__|            
                                                                                    
      """)
      return 1

  print_banner()

Input data

::
    
  data = st.text_area("Time Intervals", height=300)

Regular expression pattern to extract intervals

::
    
  pattern = re.compile(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})\n; ([\w\-]+):? (.*?)\n(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})', re.DOTALL)


We can highlight some tasks using ``task_colors.yml`` file in current folder that has
the following structure:

.. code:: yaml

   - task: TASK-1234
     color: yellow
   - task: TASK-5678
     color: green

.. function:: load_task_colors(path: str = "task_colors.yml") -> dict

::

  def load_task_colors(path: str = "task_colors.yml") -> dict:
      if not os.path.exists(path):
          return {}

      with open(path, "r", encoding="utf-8") as f:
          data = yaml.safe_load(f) or []
      task_colors = {}
      for item in data:
          color = str(item["color"]).strip().upper()
          task_colors[str(item["task"]).strip()] = color 
      
      return task_colors
    
.. function:: load_prev_tasks(path: str = "prev_sprint.csv") -> dict     

We can also highlight tasks from the previous sprint in ``prev_sprint.csv``.
This is essentially text file with the list of tasks, one per line.

::
    
  def load_prev_tasks(path: str = "prev_sprint.csv") -> dict:
      if not os.path.exists(path):
          return {}
      result = []    

      with open(path, "r", encoding="utf-8") as f:
          for line in f:
              task_name = line.strip()
              if task_name:  # Only add non-empty lines
                  result.append(task_name)
  
      return result 
    
.. function:: highlight_task(val)

Apply highlighting methods.

::
    
  task_colors = load_task_colors()
  prev_tasks = load_prev_tasks()

  def highlight_task(val):
      color = task_colors.get(val)
      if color:
          return f"background-color: #{color}; color: white;"
      if val in prev_tasks:  
          return f"background-color: #CCFFCC; color: black;"
      return ""
  
Process input

::
    
  def process():
      # Extract matches
      matches = pattern.findall(data)

      if len(matches) == 0:
          st.error('Time Intervals not found', icon='❌')
          # st.stop()
          return

Convert extracted data into a DataFrame

::
    
      records = []
      for end_dt, task_code, comment, start_dt in matches:
          start = datetime.strptime(start_dt, '%d.%m.%Y %H:%M:%S')
          end = datetime.strptime(end_dt, '%d.%m.%Y %H:%M:%S')
          duration = (end - start).total_seconds() / 3600
          records.append({
              'start_datetime': start,
              'end_datetime': end,
              'Task': task_code,
              'Comment': comment,
              'Hours': duration
          })

      # Create DataFrame
      df = pd.DataFrame(records)

Group by task_code, sum durations, and join comments

::
    
      st.session_state.grouped_df = df.groupby('Task', as_index=False).agg({
          'Hours': 'sum',
          'Comment': lambda x: ' // '.join(dict.fromkeys(x))
      })
      st.session_state.grouped_df['Hours'] = st.session_state.grouped_df['Hours'].round(1)

  
Display results

::

  if "grouped_df" in st.session_state:
      st.write("### Duration by Task")
      st.dataframe(
          st.session_state.grouped_df.style.applymap(highlight_task, subset=["Task"]),
          key="data",
          on_select="rerun",
          selection_mode=["multi-row"],
      )

      # Calculate total hours
      total_hours = st.session_state.grouped_df['Hours'].sum()
      st.write(f"**Total Hours: {total_hours}**")

Click button

::
    
  if st.button("Process", type='primary', use_container_width=True):
      process()
