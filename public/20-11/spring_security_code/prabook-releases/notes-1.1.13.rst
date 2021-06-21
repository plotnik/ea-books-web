---------------------------------
PraBook ver. 1.1.13  (20.01.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>'


Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:


Исправления
-----------

**[HTPBB-287]** `Request for prabook.org/web/sitemap-0.txt returns "IllegalArgumentException: Not correct sitemap id"`

   Оптимизация сайта для поисковых систем Google, Yandex и др.
   
------------------------

**[HTPBB-291]** `"Categories" page is not working in IE8`

   Устранены проблемы на странице "Categories", возникавшие при работе в Internet Explorer 8.

------------------------

**[HTPBB-292]** `For new user with status 5 role cannot be changed with "Save" button on user.html`

  Исправлена проблема со сменой роли для новых пользователей.

------------------------

**[HTPBB-294]** `Black box on person-view-version.html page appears.`
    
  Исправлены проблемы на странице просмотра версий анкет. 
  
------------------------

Дополнения
----------

**[HTPBB-282]** `Handling anonymous users`

  Анонимным пользователям, не имеющим аккаунта в Facebook
  предоставлен доступ для просмотра анкет. Для анонимных пользователей в правом верхнем углу 
  появляется кнопка "Login with Facebook".
  Пользователи, имеющие аккаунт в Facebook, должны воспользоваться этой кнопкой,
  чтобы авторизоваться в системе.

  .. image:: images/13/no_facebook.png
  

------------------------

**[HTPBB-298]** `Add "registration date" and "comment" fields to system_user table`

  В таблицу администрирования пользователей, добавлена колонка с датой регистрации
  (по которой можно отсортировать таблицу) и комментарием. Поскольку до сих пор
  информации о дате регистрации в таблице не было, значение для уже существующих 
  пользователей было установлено в текущую дату.
  
  .. image:: images/13/reg_date.png
  
------------------------

**[HTPBB-290]** `Links to external sites should be opened in a new window and not followed by search engines`

  Ссылки на внешние сайты в биографии персоны будут открываться в новом окне. 

  .. image:: images/13/ext_links.png
  
------------------------

**[HTPBB-295]** `Add links to external social networks and "Print" button to person-view.html`

  При просмотре анкеты можно разместить информацию о ней в своих
  социальных сетях или распечатать ее:
  
  .. image:: images/13/ext_links.png

------------------------

**[HTPBB-297]** `Provide "No profiles found" message on Search screen if nothing was found.`

  Если по критерию поиска не найдено ни одного результата, 
  выдается соответствующее сообщение.
  
  .. image:: images/13/no_profiles.png

------------------------

**[HTPBB-296]** `Optimize JavaScript in person-edit.html`

  Оптимизация JavaScript на странице редактирования анкеты
  для уменьшения времени загрузки.
  
------------------------


**[HTPBB-288]** `Add "alt" attribute to all pictires displayed on PraBook site`

  Для всех изображений на страницах добавлен уникальный атрибут "alt" 
  для их описания.
  
------------------------

**[HTPBB-300]** `<meta description> and <meta keywords> tags should be different for every page`

  Для всех анкет добавлены уникальные тэги ``<meta description>`` and ``<meta keywords>``,
  используемые поисковыми системами и соцсетями.

