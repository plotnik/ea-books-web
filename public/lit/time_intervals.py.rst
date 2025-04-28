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

  st.set_page_config(
      page_title="T-Int",
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
    
  pattern = re.compile(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})\n; ([\w\-]+) (.*?)\n(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})', re.DOTALL)

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
              'task_code': task_code,
              'comment': comment,
              'duration_hours': duration
          })

      # Create DataFrame
      df = pd.DataFrame(records)

Group by task_code, sum durations, and join comments

::
    
      grouped_df = df.groupby('task_code', as_index=False).agg({
          'duration_hours': 'sum',
          'comment': lambda x: ' // '.join(x)
      })

Display results

::
    
      # st.write("### Detailed DataFrame:")
      # st.table(df)

      st.write("### Grouped DataFrame (Total Duration by Task):")
      st.table(grouped_df)
    
Click button

::
    
  if st.button("Process", type='primary', use_container_width=True):
      process()
