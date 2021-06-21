---------------------------------
PraBook ver. 1.1.16 (10.02.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

Исправления
-----------

| **[HTPBB-318]** - `Do not redirect errors in AJAX requests to error page, but return HTTP 500 error code`
| **[HTPBB-321]** - `Minor issues with home page layout`
| **[HTPBB-323]** - `org.hibernate.QueryException: duplicate alias: _actualPersonVersion`
| **[HTPBB-324]** - `Parameter "width" is ignored for image icon URLs`
| **[HTPBB-326]** - `"HTTP Status 404" when opening PraBook page simultaneously in several browser tabs`
| **[HTPBB-320]** - `"Related Profiles" section on "person-view.html" page should fit into a single line`
| **[HTPBB-317]** - `Minor changes to improve usability on search screens`

  Исправлен ряд ошибок и неточностей, возникавших при работе программы.

Дополнения
----------

**[HTPBB-306]** - `Status should be displayed for profiles on "Search" screen`

  Статус анкеты показывается при на экране расширенного поиска:
  
  .. image:: images/16/status.jpg
  
---------------

**[HTPBB-312]** - `Profiles in "Initial" and "Taken" states should not be visible in search results for Viewers`

  Для пользователей со статусом `Viewer` показываются 
  только анкеты со статусами ``FINISHED`` и ``APPROVED``.
  
---------------

**[HTPBB-316]** - `Add "Search by profile status" criteria for Editors on "Advanced search" page`

  Для пользователей со статусом `Editor` доступен комбобокс 
  для поиска анкет с указанным статусом.

  .. image:: images/16/status-combo.jpg
  
---------------

**[HTPBB-319]** - `Add "Loading" indicator for AJAX requests for all pages using AJAX`

  На многих страницах добавлен индикатор динамической загрузки:
  
  .. image:: images/16/indicator.jpg
  
---------------

**[HTPBB-313]** - `Create Selenium test to find average times for profile editing scenario`

  На нашем сервере minsk-ftp.exadel.com запущен процесс, который срабатывает каждый час. 
  Каждый раз при запуске этот процесс выполняет следующие действия: 
  
   - он автоматически запускает браузер,
   - вызывает домашнюю страницу PraBook, 
   - логинится в приложение через Facebook, 
   - открывает одну анкету для редактирования (но ничего не меняет)
   - разлогинивается через Facebook.
   
  Для всех этих действий измеряется затраченное время, эта статистика сохраняется в файл.
  С помощью этого файла можно оценить доступность сайта и скорость загрузки страниц 
  на разных интервалах времени. 
   
---------------

**[HTPBB-314]** - `Investigate possibilities to profile PraBook editing scenarios with JMeter and YSlow`

  Проведено нагрузочное тестирование сервера ``prabook.activeby.net`` с помощью программы
  `JMeter <http://jmeter.apache.org/>`_. Результаты приведены в следующей таблице:
      
   ====================  =========================  ==================================================  ============== ======================================== =======================
   Страница              Запущено "пользователей"   Каждый "пользователь" выполнил запросов к странице  Всего запросов Среднее время обработки запроса сервером Производительность
   ====================  =========================  ==================================================  ============== ======================================== =======================
   ``home.html``         ``10``                     ``100``                                             ``1000``       ``2.30 сек``                             ``3.71 запроса/сек``
   ``home.html``         ``100``                    ``10``                                              ``1000``       ``21.30 сек``                            ``3.64 запроса/сек``
   ``search.html``       ``10``                     ``100``                                             ``1000``       ``1.12 сек``                             ``6.33 запроса/сек``
   ``search.html``       ``100``                    ``10``                                              ``1000``       ``12.99 сек``                            ``6.22 запроса/сек``
   ``categories.html``   ``10``                     ``100``                                             ``1000``       ``0.89 сек``                             ``7.08 запроса/сек``
   ``categories.html``   ``100``                    ``10``                                              ``1000``       ``4.58 сек``                             ``6.90 запроса/сек``
   ``persons.html``      ``10``                     ``100``                                             ``1000``       ``7.64 сек``                             ``1.29 запроса/сек``
   ``persons.html``      ``100``                    ``10``                                              ``1000``       ``66.74 сек``                            ``1.15 запроса/сек``
   ``person-view.html``  ``10``                     ``100``                                             ``1000``       ``3.33 сек``                             ``2.94 запроса/сек``
   ``person-view.html``  ``100``                    ``10``                                              ``1000``       ``32.06 сек``                            ``2.80 запроса/сек``
   ====================  =========================  ==================================================  ============== ======================================== =======================
   
---------------

**[HTPBB-315]** - `Optimize Solr delta-import settings`

  Оптимизирован процесс индексирования поисковой системы.


