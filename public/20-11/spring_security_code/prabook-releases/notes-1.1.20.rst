---------------------------------
PraBook ver. 1.1.20 (07.03.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

Сегодня приблизительно с 09:45 до 11.00 имели место проблемы с DNS на серверах Facebook: 

  http://www.gazeta.ru/business/2012/03/07/4030025.shtml

В связи с этим пользователи Prabook в указанное время не могли войти в систему под своими логинами.
После восстановления работоспособности Facebook работоспособность Prabook также восстановилась.

Текущий релиз содержит следующие дополнения и исправления:


Исправления
-----------

**[HTPBB-368]** - `Error "HTTP Status 405 - Request method 'GET' not supported" when trying to Reset dictionary element after Rename`

  Исправлена проблема c кнопкой **Reset** на экране **Rename** после ошибки валидации.
  Экран **Rename** переименован в **Merge**.
  
  .. image:: images/20/merge.jpg
  
-------------

**[HTPBB-370]** - `NullPointerException when calling "Show Versions" for some profiles`

  Исправлена проблема для команды **Show Versions** на экране **Persons**.
  
-------------

**[HTPBB-371]** - `Clicking item in cloud of tags does not open "Advanced Search" combobox`

  Исправлена проблема, когда псле нажатия элемента в облаке тэгов поля критериев поиска оставались спрятанными. 

-------------

**[HTPBB-372]** - `Filter values in "Persons" table should be trimmed`

  Исправлена проблема, когда пробелы по краям значений в фильтрах таблицы **Persons**
  влияли на результат фильтрации.
  
--------------------------

**[HTPBB-362]** - `Exception for "activity" table: Data truncation: Data too long for column 'name' at row 1`

  Исправлена проблема, возникавшая, когда значение поля **activity** превышало 256 символов
  (сейчас система не позволяет вводить более 256 символов в этом поле):

  .. image:: images/20/activity.jpg
  
--------------------------

Дополнения
----------

**[HTPBB-361]** - `Implement "Similar Persons" functionality using Solr`

   Значительно повышена скорость выполнения и уменьшена нагрузка на сервер
   для функциональности **Similar Persons**:
   
  .. image:: images/20/similar.jpg
   
--------------------------

**[HTPBB-363]** - `Optimize creation of ExtJS comboboxes on profile editing page`

  Некоторая оптимизация страницы редактирования анкеты.
  
--------------------------

**[HTPBB-364]** - `Make "Remove" and "Edit" links to appear on images on profile editing page when mouse is over image`

  Линки **Remove** и **Edit** появляются непосредственно при наведении
  курсора мыши на сохраненное изображение.
  
  .. image:: images/20/remove.jpg

--------------------------

**[HTPBB-365]** - `Default number of results on page for all tables should be 50`

  Количество результатов, загружаемых по умолчанию в таблицы сделано равным 50.

  .. image:: images/20/50.jpg

--------------------------

**[HTPBB-366]** - `Link to audit-log on "Users" page should point to grouped version of audit log. User should be able to request more than one-month interval from audit-log.`

  На странице **Users** фамилия пользователя является ссылкой на экран группированного аудит-лога,
  Ограничение в 1 месяц на интервал выбираемых аудит-записей не накладывается,
  если в фильтре выбран определенный пользователь:
  
  .. image:: images/20/audit.jpg
  
--------------------------

**[HTPBB-367]** - `Add validation rule for profile editing: "Name/Surname/Birth date" combination should be unique for the profile`

   Система не позволяет сохранить анкету, если уже существует анкета
   с такими же значениями полей "Name/Surname/Birth date":
   
   .. image:: images/20/already_exists.jpg
   
--------------------------

**[HTPBB-369]** - `Optimize initial loading time for "Search" page`

  Уменьшено время начальной загрузки для экрана **Advanced Search**.
  
--------------------------

**[HTPBB-373]** - `Show number of profiles taken/finished by user as a column in "Users" table`

  На странице **Users** добавлена колонка, показывающая количество анкет 
  в статусах ``taken/finished`` для данного пользователя.
  
   .. image:: images/20/in_work.jpg
  
