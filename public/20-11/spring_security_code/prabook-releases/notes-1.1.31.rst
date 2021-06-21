---------------------------------
PraBook ver. 1.1.31 (25.05.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', Татьяна Боровкова [borovkova.t.v@gmail.com], Бильдюкевич Ольга (vbildziukevich@exadel.com), Андрушкевич Михаил (mandrushkevich@exadel.com)

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.1.31

Исправления
-----------

[HTPBB-460] - Dictionary: can save Activity catalog with empty name
===================================================================

Добавлена проверка, запрещающая сохранение элемента каталога с пустым именем.

[HTPBB-461] - Dictionary: HTTP/1.1 405 Method Not Allowed when try to merge schools
===================================================================================

Исправлена проблема, возникавшая в некоторых случаях при слиянии элементов справочников.

[HTPBB-464] - Users: old design on the users edit page
======================================================

Страница для редактирования прав пользователя приведена к "новому" дизайну.

.. image:: images/31/user.jpg
   :align: center

[HTPBB-466] - Can not edit person profile if '\' char exists in the name of added activity
==========================================================================================

Исправлена проблема для элементов справочника **Activity**, содержащих символ ``\\``.

[HTPBB-467] - Profiles with names including international characters can not be found
=====================================================================================

Исправлена проблема, возникавшая при поиске фамилий, содержащих символы со штрихами.

Дополнения
----------

[HTPBB-468] - Dictionary values on profile-view page should be links showing profiles from appropriate categories
=================================================================================================================

Элементы справочников при просмотре анкеты представлены линками.

.. image:: images/31/laura.jpg
   :align: center

[HTPBB-469] - Search queries should have higher priorities for activities rather than person names
==================================================================================================

Реализовано для справочника **Activity**, согласно требованию,
чтобы в поиске при наборе `music` в первую очередь выдавались люди, 
которые занимаются музыкой, а только потом фамилии.

