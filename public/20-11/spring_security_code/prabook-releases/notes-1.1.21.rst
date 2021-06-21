---------------------------------
PraBook ver. 1.1.21 (16.03.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:


Исправления
-----------

**[HTPBB-375]** - `Entering generic query on "Search" screen and clicking Enter should return search result for entered query rather than first hint`


  Со стартовой страницы ``prabook.org`` удален виджет с фотографиями. 
  Исправлена проблема, когда при наборе в строке поиска всегда 
  подставлялась первая подсказка.
  
  Сейчас для поиска нужно ввести запрос и нажать **Enter**.
  
  .. image:: images/21/home.png

--------------------------

**[HTPBB-377]** - `Problem with links that are external from the profile (see "Elena Grishanova")`

  Исправлена проблема для линков на другие сайты, возникавшая при просмотре анкеты. 
  
  .. image:: images/21/grishanova.jpg

--------------------------

**[HTPBB-381]** - `Information about relatives cannot be added to profiles`

  Исправлена проблема с добавлением родственников в анкету.
  
--------------------------

**[HTPBB-383]** - `Problem when checking date intervals for validity`

  Исправлена проблема с проверкой интервалов дат для анкеты.
  
--------------------------

**[HTPBB-384]** - `"Recently Created" column on "Search" page is showing wrong profiles`
  
  Исправлена проблема, когда в колонке **Recently Created**
  показывались неверные данные.
  
  .. image:: images/21/recently.jpg

--------------------------

**[HTPBB-385]** - `Layout problems on "Most viewed" and "Recently created" pages`

  Исправлены отображения анкет на страницах **Most viewed** и **Recently created**
  
  .. image:: images/21/mostviewed.jpg

--------------------------

**[HTPBB-386]** - `Wrong URLs in generated "robots.txt" and "sitemap.xml" files`

  Исправлена проблема с неправильным указанием адресов для поисковых систем. 
  
--------------------------

Дополнения
----------

**[HTPBB-374]** - `Allow "Persons" page for administrators only; add "Create Person" button on "Advanced Search" page`

  Страница **Persons** сейчас доступна только администраторам.
  Студентам для работы с базой сейчас нужно пользоваться страницей **Search**.
  
  На страницу **Search** добавлена кнопка для создания анкеты **Create Person**.
  Сейчас эта кнопка доступна студентам только на этом экране
  (поскольку на стартовом экране она удалена вместе с виджетом).

  .. image:: images/21/nopersons.jpg

--------------------------

**[HTPBB-376]** - `Show profile status and locked userid for "View" page. Remove "Edit" buttons if editing is not possible.`

  На странице просмотра анкеты показан текущий статус анкеты и фамилия редактора.
  Кнопки **Edit** спрятаны на этой странице для редакторов, если анкета уже находится в работе у другого 
  редактора.
  
  .. image:: images/21/userid.jpg

--------------------------

**[HTPBB-378]** - `Add "Check for possible duplicates" panel on "Edit" screen`

  При редактировании анкеты внизу показывается панель возможных дубликатов.
  Студентам следует обращать внимание на эту панель и не создавать дубликатов,
  а редактировать ранее созданные анкеты.
  
  .. image:: images/21/Irina_Vidova.png 

--------------------------

**[HTPBB-380]** - `Prabook should be accessed only by Facebook-authenticated users`

  На текущем этапе ``prabook.org`` закрыт для индексирования поисковыми системами.
  Доступ к сайту возможен только для пользователей, авторизованных в **Facebook**.
