---------------------------------
PraBook ver. 1.1.15 (03.02.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

На этой неделе мы переместились на новый хостинг: http://prabook.activeby.net

Очередной релиз содержит следующие дополнения:

**[HTPBB-309]** `Change default profile icon size to 130x130`

  Заглавная страница приведена к утвержденному дизайну:
  
  .. image:: images/15/home.jpg
  
-----------------------

**[HTPBB-310]** `Implement rollback of versions in profile with "Unlock" button`

  Анкета в статусе ``TAKEN`` при нажатии кнопки **Unlock** 
  возвращается в состояние, которое было до нажатия кнопки **Take**
  
  .. image:: images/15/unlock.jpg
  
-----------------------

**[HTPBB-311]** `Add approval process for profiles`

  Закончена имплементация процесса утверждения анкеты, описанного
  в моем письме `PraBook: Экран редактирования анкеты` 
  от `24 января`. Диаграмма возможных переходов между состояниями для 
  анкеты согласно спецификации в письме выглядит так:
  
  .. image:: images/15/states.gv.gif

