---------------------------------
PraBook ver. 1.1.11  (06.01.2012)
---------------------------------

    :To: 'Tsepkalo Valery'; 'Мартинкевич Александр Михайлович'; 'Sergey Severin'
    :Cc: 'HTP PeopleBook'


Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

Исправления
-----------

**[HTPBB-272]** `Cannot rename nationality "Abbadids kingdom" into "Abbasid caliphate"`

  Исправлена проблема, возникавшая при слиянии элементов справочников.

------------------------

**[HTPBB-277]** `Problem when searching birth/death dates`

  Исправлена проблема, возникавшая при поиске по датам.

------------------------

Дополнения
----------


**[HTPBB-266]** `Create prototype of PraBook home page with search function`

  Добавлен экран простого поиска, который содержит строку для ввода критерия поиска, 
  окруженную информацией о нескольких анкетах, соответствующих этому критерию. 
  При открытии экрана критерий поиска выбирается случайным образом из нескольких значений, установленных администратором.

  Когда пользователь вводит свой критерий поиска, найденные анкеты меняются соответствующим образом по мере набора.

  .. image:: images/11/home.jpg
  
------------------------

**[HTPBB-265]** `Add new dictionary for predefined search keywords`

  Добавлен справочник для критериев поиска предлагаемых по умолчанию на экране простого поиска.

  .. image:: images/11/default_search_query.jpg

------------------------

**[HTPBB-255]** `Publication Type field in profile should be able to add new dictionary elements for approval`

  Значения для справочника **Publication Type** могут добавляться через экран редактирования анкеты.
  
  .. image:: images/11/publication_type.jpg

------------------------

**[HTPBB-261]** `Following fields in profile should be able to add new dictionary elements for approval: "Person on the Internet", "Relative", "Other connections"`

  Значения для справочников **Person on the Internet**, **Relative**, **Other connections** 
  могут добавляться через экран редактирования анкеты.

  .. image:: images/11/relatives.jpg
  
------------------------

**[HTPBB-257]** `Provide number of profiles using this dictionary item on Catalog page`

  Для разделов и подразделов каталога указано количество анкет, 
  использующих этот элемент справочника.
  
  .. image:: images/11/catalog.jpg
  
------------------------

**[HTPBB-260]** `Cache profile icons for "Search" screen`

   Оптимизация работы с иконками изображений
   
---------------------


**[HTPBB-262]** `Update Solr for negative dates`

  Поддержка поисковым сервисом дат до н.э.
  
------------------------

**[HTPBB-263]** `Remove HTML comments when saving "Life in brief" and "History Events"`

  Исправлена проблема, возникавшая при копировании в поля, содержащие форматированный текст
  ("Life in brief" и "History Events") из MS Word.
  
------------------------

**[HTPBB-264]** `Remove tabs from "Profile View" to have all information as a single page`

  При просмотре анкеты вся информация, содержащаяся в анкете, представлена на одной странице
  и опущены пустые секции.
  
  .. image:: images/11/orda.jpg

------------------------


**[HTPBB-267]** `Replace date controls on "Search" page with date editing component used in profiles`

  На странице поиска поля ввода дат заменены на компонент, уже использующийся при редактировании анкеты и
  позволяющий вводить даты до нашей эры:
  
  .. image:: images/11/search_dates.jpg

------------------------

**[HTPBB-269]** `Create "Add link to profile" button for "Life in brief" and "Event" editing fields`

  В редакторы форматированного текста (поля "Life in brief" и "Event")
  добавлена кнопка "Link to profile", позволяющая добавлять в текст 
  ссылки на существующие анкеты PraBook:
  
  .. image:: images/11/link_to_profile.jpg

------------------------

**[HTPBB-271]** `Add PhotoFile cleaning task to PraBook scheduler`

  Загруженные фотографии, которые не используются ни в одной из анкет
  (если анкета не была сохранена после загрузки фотографии)
  теперь удаляются.
  
------------------------

**[HTPBB-273]** `Investigate how to reduce size of Ext.Js library for certain pages`

  Рассмотрены возможности уменьшения времени загрузки страниц PraBook 
  за счет конфигурирования библиотеки Ext.Js
  
------------------------

**[HTPBB-274]** `Refactor service for grouped audit-log to count records with Projections.countDistinct`

  Оптимизация и уменьшение времени загрузки страницы группированного аудит-лога. 
  
------------------------

**[HTPBB-275]** `Always limit range in audit log tables (grouped and detailed)`

  Принудительное ограничение отображаемого интервала на срок в 1 месяц на страницах аудит-лога.
   
  Поскольку аудит-лог через определенное время может стать достаточно большим, 
  система ограничивает интервал дат, для которых выводятся данные. 

  .. image:: images/11/audit_log_dates.jpg
  
------------------------

**[HTPBB-276]** `Optimize database interactions we perform to open "Persons" page`

   Оптимизация и уменьшение времени загрузки страницы со списком анкет. 
  


