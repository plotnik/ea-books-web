---------------------------------
PraBook ver. 1.1.18 (24.02.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

Исправления
-----------

**[HTPBB-336]** - `Search field values provided as URL parameters are not copied into search field controls on "Advanced Search" page`

  Исправлена проблема со спрятанными полями поиска на экране "Advanced Search".
  
-----------------  

**[HTPBB-342]** - `Unlocking profile throws MySQLIntegrityConstraintViolationException: Column 'actual_person_version_id' cannot be null`

  Исправлена проблема, не позволявшая отменить сделанные изменения в анкете в состоянии ``TAKEN`` 
  (была обнаружена для анкеты ``YAUNEVICH``)

-----------------  

**[HTPBB-343]** - `In IE there are "JspTagException: No message found under code 'person.{$fieldName}.id'" messages when saving the profile`

  Исправлены проблемы, возникавшие в Internet Explorer при редактировании анкеты.
  
-----------------  

**[HTPBB-345]** - `Russian characters are garbled when using filters on "Users" screen`

  Исправлены проблемы с русскими буквами, возникавшие на хостинге **active.by**.

-----------------  

**[HTPBB-350]** - `Several "Work/achievements" additions are merged into a single one`

  Исправлена проблема, возникавшая при добавлении нескольких записей в поле
  "Achievements"
  
  .. image:: images/18/achievements.jpg 

-----------------  

**[HTPBB-351]** - `"Position" label on "work/career" editing screen is missing`

  Исправлена метка поля на экране "Work/Career":

  .. image:: images/18/career.jpg 

----------------

Дополнения
----------

**[HTPBB-338]** - `Deletion of profiles by Administrator should be possible`
  
  У администратора появилась возможность удаления анкет:
  
  .. image:: images/18/delete.jpg 

