YouTube Clean
=============
         
This is a
`Playwright <https://playwright.dev/python/docs/running-tests>`__ script
for deleting likes from videos one by one.

Before running the script, you need to start Chrome in remote debugging mode
and login into your Google account.

Here is invoke commad for MacOS:

.. code:: python

   @task
   def chrome_mac(ctx):
       chrome_path = r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
       ctx.run(f'"{chrome_path}" '
                '--remote-debugging-port=9222 '
                '--user-data-dir=.chrome', pty=True)


Here is invoke commad for Windows:  

.. code:: python
                                                         
   @task                                                                               
   def chrome_win(ctx):            
       chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
       ctx.run(f'"{chrome_path}" '
                '--remote-debugging-port=9222 '
                '--user-data-dir=.chrome', pty=False)
                                      
Imports

::

  from playwright.sync_api import sync_playwright
  import time
  import sys

Allow to print Unicode on Windows

::

  sys.stdout.reconfigure(encoding="utf-8")
  sys.stderr.reconfigure(encoding="utf-8")

Read the number of likes to delete from command line

::
    
  NUM_TO_DELETE = 100

  if len(sys.argv) > 1:
      NUM_TO_DELETE = int(sys.argv[1])
    
  print(f"Number of likes to delete: {NUM_TO_DELETE}")

Attach to Chrome.

::
    
  with sync_playwright() as p:
      browser = p.chromium.connect_over_cdp("http://localhost:9222")
      context = browser.contexts[0]
      page = context.new_page()

      for i in range(NUM_TO_DELETE):
          page.goto("https://www.youtube.com/playlist?list=LL")
          page.wait_for_selector("ytd-playlist-video-renderer", timeout=15000)
          time.sleep(2)
        
Always target the first video since the list shifts up after each removal

::

          video = page.locator("ytd-playlist-video-renderer").first
          title_el = video.locator("#video-title")
          title = title_el.get_attribute("title") or title_el.inner_text()
          print(f"[{i+1}/{NUM_TO_DELETE}] Removing: {title}")

Open the three-dot menu for this video

::

          menu_button = video.locator("button#button.yt-icon-button", has=page.locator("yt-icon"))
          menu_button.click()
          time.sleep(1)

Click "Remove from Liked videos" in the popup menu

::

          remove_option = page.locator(
              "ytd-menu-service-item-renderer yt-formatted-string"
          ).filter(has_text="Remove from Liked videos")
          remove_option.wait_for(state="visible", timeout=5000)
          remove_option.click()
          time.sleep(1)
      
Print the result

::

      print(f"Done — removed {NUM_TO_DELETE} videos from Liked playlist.")