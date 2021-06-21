---------------------------------
PraBook ver. 1.1.19 (02.03.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили очередной релиз 
а также провели измерения производительности.
Вот сравнение изменения производительности между прошлым замером 10 февраля и текущим замером 1 марта.
Разница состоит в том, что произведены некоторые существенные 
оптимизации в коде и Tomcat с базой разнесены на разные машины.
Производительность для страницы просмотра анкеты, например, повысилась приблизительно в 30 раз.


Исправления
-----------

**[HTPBB-322]** - `Sometimes "Categories" page opens empty in Firefox and AJAX request is not sent`

  Исправлена проблема, когда страница "Categories" иногда открывалась пустая.   
  
--------------------------

**[HTPBB-353]** - `"Advanced Search" combos should be closed with "Clear" button`
    
  Исправлена проблема с закрытием пустых полей после нажатия кнопки "Clear".
  
  .. image:: images/19/clear.png
  
--------------------------
    
**[HTPBB-354]** - `It is not possible to edit content of date fields in Opera`
  
  Исправлена проблема с редактированием полей дат в Opera
  
--------------------------

**[HTPBB-356]** - `In "Life in brief" field when pasting text from MS Word some spaces between words are unexpectedly lost`

  Исправлена проблема, когда при вставке в поле "Life in brief" из MS Word иногда 
  терялись пробелы между словами.

--------------------------

**[HTPBB-357]** - `Problems with components placement on "profile editing" and "events" pages`

  Исправлены некоторые проблемы, возникавшие при JavaScript-вставке полей ввода на страницу.
  
--------------------------

**[HTPBB-360]** - `MySQLIntegrityConstraintViolationException: Duplicate entry 'Atheism' for key 'name'`

  Исправлена проблема, выбрасывавшая экран ошибки для дубликатов в поле "Religion"
  
--------------------------

Дополнения
----------

**[HTPBB-344]** - `Combine fields "Name" and "Surname" for "Connections" and "Relatives" into a single one. Add possibility to add references to existing profiles`

  Поля **Name** и **Surname** в секциях **Relatives** и **Other connections"** 
  на странице **Connections** объединены в одно.

  Добавлена возможность заполнять секции **Relatives** и **Other connections"**
  ссылками на уже существующие анкеты. Для этого надо выбрать 
  соответствующий элемент из выпадающего списка подсказок.

  В этом случае при просмотре анкеты в данных секциях будут стоять ссылки на 
  указанные анкеты.
  
  .. image:: images/19/connections.png

--------------------------

**[HTPBB-348]** - `Add "My Edited Profiles" page`

  Добавлена страница **Dashboard**, на которой перечислены анкеты,
  находящиеся в редактировании для данного пользователя. 

  .. image:: images/19/dashboard.png
  
--------------------------

**[HTPBB-349]** - `"Rework" and "Finish" buttons should not close profile editing screen`

  Кнопки **Rework** и **Finish** не закрывают текущую анкету.
  
--------------------------

**[HTPBB-355]** - `On "Home" page if there are no search results add some profiles with photo`

  Если на домашней странице программы не найдено анкет по текущему запросу,
  страница заполняется анкетами стандартных запросов. Рекомендуется 
  для каждой категории стандартных запросов иметь более 6 анкет.
  Анкеты, не соответствующие запросу пользователя, а просто дополняющие
  страницу помечены меткой "see also".
  
  .. image:: images/19/home.png

--------------------------

**[HTPBB-358]** - `On "Users" page add a link to editors name pointing to audit-log table with all changes by this user`

  На странице **Users** фамилия пользователя является ссылкой на экран аудит-лога, 
  на котором перечислены все изменения, внесенные данным пользователем.
  
  .. image:: images/19/users.png
  
