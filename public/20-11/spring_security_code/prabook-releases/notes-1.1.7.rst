--------------------------------
PraBook ver. 1.1.7  (02.12.2011)
--------------------------------

    :To: Tsepkalo Valery; Мартинкевич Александр Михайлович; Северин Сергей Александрович [S.Severin@PARK.BY]  
    :Cc: 'HTP PeopleBook'


Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

Исправления
-----------

**[HTPBB-209]** `Special HTML characters in dictionaries`

  Исправлены проблемы, возникавшие при работе
  со специальными символами HTML ``< > & " '`` в справочниках:
  
  .. image:: images/html_activity.jpg

-----------------------

**[HTPBB-218]** `Special HTML characters &<>" in audit log`

  Исправлены проблемы, возникавшие при работе с аудит-логом
  для записей, содержащих
  специальные HTML символы: ``< > & " '``
  
  .. image:: images/html_audit_log.jpg

-----------------------
  
**[HTPBB-220]** `Date filter tor Audit Log Summary page throws an exception`

  Исправлена проблема, не позволявшая применять фильтр по датам 
  на странице аудит-лога с записями, сгруппированными 
  по "редакторам и анкетам":
  
  .. image:: images/audit_log_dates.jpg
  

Дополнения
----------

**[HTPBB-222]** `Add link to "Search" page into main PraBook menu`

  Линк на страницу поиска вынесен в главное меню PraBook, чтобы сделать 
  эту функциональность, существовавшую уже в предыдущих релизах PraBook,
  более доступной для тестирования. 
  
  Дизайн для этой страницы еще находится в процессе разработки. 
  
  .. image:: images/search.jpg
  
  
-----------------------

**[HTPBB-212]** `Add fields to "Search Result" page`
   
  Расширено количество полей, выводимых для найденных анкет. Сейчас это поля:
  
    - Photo
    - Name / Surname
    - Birth date / Death date (if avail)
    - Activity
    - A piece of "Life in brief"

  Текст из поискового запроса подсвечен жирным шрифтом. 
  
-----------------------

**[HTPBB-217]** `Convert remaining Date fields in Profile to Day/Month/Year set of inputs`

  В прошлом релизе была начата миграция полей с датами в анкетах на 3 раздельных поля 
  "день-месяц-год" для того, чтобы обеспечить возможность указывать только год для даты,  
  либо не указывать конкретный день. В этом релизе закончен переход на новую систему ввода дат
  для всех страниц анкеты:

  .. image:: images/work_dates.jpg
  
-----------------------

**[HTPBB-223]** `Remove obsolete Date fields in person_version table (currently replaced with Y/M/D fields)`

  Поля для старой системы ввода дат удалены из таблиц в базе данных.  

-----------------------

**[HTPBB-219]** `All fields that use dictionaries in profile should be able to add new dictionary elements for approval`

  В предыдущей версии при редактировании анкеты нельзя было добавить 
  новое значение в справочники, разбитые по категориям: `Activity, Religion, Nationality, Ethnicity`.
  Сейчас поля ввода в анкетах, использующие справочники, допускают вводить значения, 
  на данный момент отсутствующие в справочниках. После сохранения анкеты новые значения
  будут добавлены в соответствующие справочники как неутвержденное (т.е. без пометки **Approved**).
  Впоследствии администратор может проанализировать неутвержденные значения в справочниках,
  и либо утвердить их, либо заменить во всех анкетах на утвержденные значения, либо удалить.

  .. image:: images/dict_elems.jpg

-----------------------

`С уважением,`
    | `Егор Абрамович`
    | `HTP Belarus PraBook Project,` http://www.prabook.org
    | `Exadel, Inc`


.. prev-release

    Исправления
    -----------
    
    **[HTPBB-202]** `Updating "Resting Place" in Person's Profile throws an exception`
    
      Исправлена проблема, возникавшая при сохранении полей
      "Resting Place", "Birth Place" и "Death Place" в анкете.
    
    **[HTPBB-203]** `Not possible to replace Party Affiliation "democrat" with "Democrat"`
    
      В разделе "Dictionaries" добавлен новый справочник "Party". С его 
      помощью можно отредактировать поле **Name** в требуемое значение 
      и нажать **Save Changes**. При этом значение изменится 
      во всех анкетах, которые используют данный элемент справочника.
      
      .. image:: images/party.jpg
      
    **[HTPBB-211]** `"Show Changes" window is not able to display international characters`
    
      Окно для просмотра изменений между версиями анкет теперь поддерживает
      интернациональные символы.
      
    Дополнения
    ----------
    
    **[HTPBB-201]** `Add "Life in brief" tab to Person Profile`
    
      Добавлено поле для ввода биографии:
      
       .. image:: images/bio.jpg
      
    
    **[HTPBB-130]** `Add ability to add date without month and day` + **[HTPBB-207]** `Server support for partial dates in profile`
    
       Компонент для ввода дат теперь позволяет вводить только год, либо год и месяц, либо год, месяц и день. 
       
       .. image:: images/party.jpg
       
       На текущий момент компонент заменен только на странице **General** анкеты.
       В следующей версии мы планируем заменить его на остальных страницах.
    
    **[HTPBB-173]** `Make Religion category savable without religion`
    
      Удалено поле "Категории" для религий:
      
       .. image:: images/saved_religion.jpg
      
    
    **[HTPBB-204]** `Combine "Work" and "Awards" tabs into a single one in Person's Profile`
    
      Две страницы справочника объединены в одну.
      
      .. image:: images/work_awards.jpg
      
    **[HTPBB-205]** `"Approved" column should be sortable in Dictionaries` + 
    **[HTPBB-206]** `"Approve" link should be added to Dictionary tables` +
    **[HTPBB-191]** `Apply design to dictionary pages`
    
      Можно отсортировать элементы справочника, которые еще не прошли проверку.
      Можно подтверждать элементы справочника прямо из общего списка.
      
      .. image:: images/approve_dict.jpg
      
    
    **[HTPBB-208]** `Link to profile in audit log should point to the latest version`
    
      Ссылка на анкету в аудит-логе теперь указывает на актуальную версию анкеты 
      (раньше она указывала именно на ту версию анкеты, для которой были сделаны данные изменения)
    
    **[HTPBB-200]** `Identify Person's Profile viewing and editing pages with # sign in URL`
    
       Каждой странице редактирования внутри одной анкеты присвоен уникальный URL.


  

