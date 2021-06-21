---------------------------------
PraBook ver. 1.1.17 (17.02.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

На этой неделе новый хостинг на active.by перенастроен на имя http://prabook.org

Текущий релиз содердит следующие дополнения и исправления:

Исправления
-----------

**[HTPBB-327]** - `InvalidTokenOffsetsExceptions in Solr log`

  Для устранения проблемы, возникавшей на поисковом сервере при выделении найденных результатов, 
  отключены некоторые синонимы для поиска.
  
-----------------  
  
**[HTPBB-328]** - `Unnecessary redirect to Facebook during login`

  Устранение ненужной перезагрузки страницы, возникавшей в некоторых случаях
  при логине пользователя через Facebook.
  
-----------------  
  
**[HTPBB-334]** - `DataIntegrityViolationException: not-null property references a null or transient value: com.htp.peoplebook.domain.object.Publication.type`

  Добавлены необходимые валидационные правила: тип публикации не может быть пустым.
  
  .. image:: images/17/public_type.jpg 
  
----------------

**[HTPBB-335]** - `Wrong sorting for "Registration date" column of "Users" screen`

  Исправлена сортировка по полю "Registration date" на экране "Users":
  
----------------
  
**[HTPBB-339]** - `Negative validation when editing profile brings buttons for "Initial" status (should be for "Taken" status)`

  Исправлена проблема, при которой при попытке сохранения
  анкеты с неправильными данными показывались кнопки для статуса "Initial",
  хотя анкета при редактировании находится в статусе "Taken".
    
----------------

Дополнения
----------

**[HTPBB-325]** - `Provide method to delete profiles`

  Были внесены изменения в базу данных, необходимые для 
  того, чтобы сделать возможным удаление анкет.
  Имплементация удаления анкет администратором через веб-интерфейс ожидается в следующем релизе.

----------------
  
**[HTPBB-329]** - `Empty search comboboxes are initially closed on Advanced Search page`

  На странице "Advanced search" пустые поля для расширенного поиска изначально спрятаны:
  
  .. image:: images/17/closed_controls.jpg
  
----------------

**[HTPBB-330]** - Minor issues when rendering search results

  Исправлены некоторые проблемы, возникавшие при прокрутке результатов поиска. 
  
----------------

**[HTPBB-331]** - `Automatic login on home page reloads page and changes default search request`

  На домашней странице ``prabook.org`` при логине осуществляется
  запрос к Facebook, при этом страница раньше перегружалась,
  случайный критерий поиска мог измениться и анкеты заменялись на другие.
  Теперь запрос к Facebook осуществляется через AJA{ и анкеты не перегружаются.
  
---------------  

**[HTPBB-332]** - `Investigate possibilities to apply Google Analytics to PraBook`

  На страницы ``prabook.org`` добавлен сервис Google Analytics, позволяющий
  собрать статистику посещаемости для сайта:
  
  .. image:: images/17/google_analytics.jpg 
  
---------------  
 
**[HTPBB-333]** - `Create error pages for HTTP results 401, 403, 404, 500/501`

  Ошибки HTTP 401, 403, 404, 500/501 возвращаются серером через специальную страницу:

  .. image:: images/17/403_forbidden.jpg 
  
---------------  
 
**[HTPBB-337]** - `Add sorting and filtering for "Comment" field on "Users" screen`

  Для колонки комментария на странице "Users" добавлена возможность сортировки и фильтрации:
  
  .. image:: images/17/comment.jpg 
  
---------------  

**[HTPBB-340]** - `Hide "Born" and "Died" dates on "Persons" page`

  Колонки для дат рождения и смерти спрятаны на странице "Persons", чтобы таблица легче
  помещалась на экран:
  
  .. image:: images/17/persons.jpg 

