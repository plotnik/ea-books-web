---------------------------------
PraBook ver. 1.1.24 (06.04.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', Татьяна Боровкова [borovkova.t.v@gmail.com], Андрей Головнев (ahalauniou@exadel.com)

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы запустили параллельный сервер http://people.belarus.by 
с усеченной версией базы. На текущий момент скрипт удаления анкет небелорусов
еще не закончил свою работу, в понедельник я обновлю на нем
индексы поискового сервера и ``people.belarus.by`` будет готов к использованию.

Также мы подготовили очередной релиз со следующими дополнениями и исправлениями:


Исправления
-----------

**[HTPBB-412]** - `"Profiles in Work" on "Users" page should be equal to number of profiles for this user in audit log`

  На странице **Users** в колонке **Profiles in Work** для пользователя 
  теперь показывается полное количество анкет, которые он редактировал,
  равное количеству его анкет на странице **Dashboard** и в аудит-логе.
  
  .. image:: images/24/inwork.jpg

--------------------

**[HTPBB-407]** - `Buttons for social networks are mentioned twice on "Profile View" page`
  
  Исправлена проблема, когда кнопки социальных сервисов дублировались 
  на странице просмотра анкеты.

----------------

**[HTPBB-403]** - `SolrException: Bad Request`

  Исправлена мелкая проблема для слишком длинных запросов поискового сервера. 
    
--------------------

Дополнения
----------

**[HTPBB-391]** - `Migrate PraBook code to Tomcat 7`

  Сделан апгрейд Java-cерверов для приложения и поиска до версии Tomcat 7.0. 
  
----------------

**[HTPBB-408]** - `Add possibility to manually crop image for the icon`

  Добавлена возможность выбора области изображения для иконки.
  
  .. image:: images/24/crop.jpg
  
----------------

**[HTPBB-409]** - `Extend content column on Search, Catalog, Profile pages on 200px. Add a little padding under the footer.`

  Немного расширена центральная область для страниц поиска, 
  каталога и просмотра анкеты.
  
  .. image:: images/24/search.jpg

----------------

**[HTPBB-410]** - `Add "Delete" button in Dashboard for profile if there were no other editors`

  Добавлена кнопка **Delete** для удаления анкеты на странице **Dashboard**.
  Здесь доступны к удалению не все анкеты, а только те, 
  `единственным` редактором которых был текущий пользователь.
  Если администратор все же хочет удалить анкету, которую редактировал
  кто-то еще, он может сделать это
  на странице **Persons**.

  .. image:: images/24/dashboard.jpg

----------------

**[HTPBB-411]** - `Add configuration parameter in server.xml for people.belarus.by version`

  Добавлен конфигурационный параметр для разделения приложения между 
  серверами ``prabook.org`` и ``people.belarus.by``
  
----------------


**[HTPBB-413]** - `Show profile status on "Audit Log" page`

  На странице **Audit Log** теперь показывается статус анкеты.
  
  .. image:: images/24/audit.jpg

