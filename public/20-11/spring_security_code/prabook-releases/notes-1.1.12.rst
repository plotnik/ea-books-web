---------------------------------
PraBook ver. 1.1.12  (13.01.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>'


Здравствуйте,

Мы обновили регистрацию приложения в Facebook, поэтому пользователям 
нужно один раз дополнительно нажать "Log In" в окне подтверждения

.. image:: images/12/facebook_confirm.jpg

Текущий релиз содержит следующие дополнения и исправления:

Исправления
-----------

**[HTPBB-289]** `ConstraintViolationException in prabook.org logs` 

    Исправлена проблема, проявлявшаяся сообщением об ошибке:
    
    ::
        
        11:25:36,085 ERROR PersonController - handled unexpected exception
        org.springframework.dao.DataIntegrityViolationException: Could not execute JDBC batch update; 
        SQL [insert into person_activity (person_id, activity_id) values (?, ?)]; constraint [null]; 
        nested exception is org.hibernate.exception.ConstraintViolationException: 
        Could not execute JDBC batch update

    Мы предполагаем, что эта ошибка возникала, когда пользователь 
    пытался добавить в анкету две одинакове activity:
    
    .. image:: images/12/same_activities.jpg
    
    Сейчас в программу добавлена проверка, которая убирает подобные дубликаты
    при сохранении анкеты.
    
------------------------

Дополнения
----------

**[HTPBB-268]** `Replace date controls on "Persons" page with date editing component used in profiles`

   Фильтр списка анкет теперь позволяет выбирать неполные даты и даты до нашей эры:
   
   .. image:: images/12/date_filter.jpg
   
------------------------

| **[HTPBB-278]** `Add cloud of tags and links to services to Home page`
| **[HTPBB-284]** `Create links to external social networks on PraBook home page: Twitter, FaceBook, LinkedIn, LiveJournal`

  На стартовой странице ``prabook.org`` добавлены облако тэгов,
  и ссылки, позволяющие пользователям автоматически добавлять информацию
  о PraBook в свои социальные сети:
  
   .. image:: images/12/home.jpg
   
------------------------
  

**[HTPBB-279]** `Update photo URLs to bypass system_user checks; keep system_user info in session to minimize number of db requests`

  Оптимизация системы: уменьшение количества запросов к базе для показа иконок анкет.
  
------------------------

**[HTPBB-280]** `Ensure that user role is rechecked for editing URLs`

  Если администратор сменил роль пользователю (например, 
  сделал его `Viewer` вместо `Administrator`), то недоступные линки пропадут при переходе на
  новую страницу. Раньше это осуществлялось только после того, как пользователь 
  выполнит **Logout**.
  
------------------------

**[HTPBB-281]** `Collect search requests from users and provide most popular ones as hints`

  Система сейчас запоминает запросы пользователей, и выдает наиболее популярные 
  как подсказки при поиске. Изначально в базу подсказок для поиска залиты имена из анкет.
  
   .. image:: images/12/hints.jpg
   
------------------------
  
  
**[HTPBB-283]** `"Suspended" field for system users`

   Администратор может установить для пользователя флаг **Suspend**. 
   При этом роль пользователя снижается до `Viewer`,
   а все изменения, которые он произвел в анкетах, откатываются.

   .. image:: images/12/suspend.jpg
   
------------------------

**[HTPBB-285]** `Highlight found patterns on Home and Search pages`

  На страницах **Home** и **Search** найденные строки подсвечены фоном.
  

  
