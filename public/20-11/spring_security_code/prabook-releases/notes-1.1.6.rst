Северин Сергей Александрович [S.Severin@PARK.BY]
To: 
Cc: Tsepkalo Valery; Мартинкевич Александр Михайлович; 'HTP PeopleBook'


------------------------------------------------

PraBook ver. 1.1.6  (25.11.2011)


Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

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


  
`С уважением,`
    `Егор Абрамович`

