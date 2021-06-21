---------------------------------
PraBook ver. 1.1.29 (11.05.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', Татьяна Боровкова [borovkova.t.v@gmail.com], Бильдюкевич Ольга (vbildziukevich@exadel.com)

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.1.29

Исправления
-----------

[HTPBB-457] - Disable "Edit" buttons for profiles in Finished status 
====================================================================

Для пользователей с ролью `Editor` закрыта возможность редактирования анкет,
созданных другими пользователями,
в статусах ``FINISHED`` и ``APPROVED``. Таким образом, редактирование
пользователей с ролью `Editor` будет возможно в следующих случаях:

:INITIAL: возможно всегда
:TAKEN: возможно только для своих анкет
:FINISHED: возможно только для своих анкет
:APPROVED: невозможно
    
.. image:: images/29/edit.jpg
   :align: center


Дополнения
----------

[HTPBB-456] - "This person on internet" link should be always visible
=====================================================================

Линк **This person on internet** будет виден при просмотре анкеты,
даже если в этом поле нет ни одного интернетовского адреса. 

.. image:: images/29/inet.jpg
   :align: center

[HTPBB-458] - Show "This person also known as" on person-view page without a label
==================================================================================

Поле, заполняемое в анкете как **Full name, name spelling variants, pseudonym**,
будет показано при просмотре без поясняющей метки.

.. image:: images/29/nick.jpg
   :align: center

