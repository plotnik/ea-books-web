---------------------------------
PraBook ver. 1.1.26 (19.04.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', Татьяна Боровкова [borovkova.t.v@gmail.com], Андрей Головнев (ahalauniou@exadel.com)

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.1.26

Исправления
-----------

[HTPBB-425] - Invocation of method 'updateSolrProfileCore' failed: id to load is required for loading
=====================================================================================================

Исправлена проблема импорта данных поисковым сервером, возникавшая для некоторых анкет. 

[HTPBB-427] - Calendar component on Search page shouldn't extend beyong the column
==================================================================================

Исправлено отображение компонента дат на странице поиска.

.. image:: images/26/calendar.jpg
   :align: center

[HTPBB-429] - Correctly adjust table resize with JavaScript
===========================================================

Исправлено поведение размеров таблицы при изменении размеров окна.

.. image:: images/26/scale.jpg
   :align: center

[HTPBB-431] - Profile with name '<>"<> is not able to display main photo on editing screen
==========================================================================================
    
На странице редактирования анкеты некорректно отображались данные, содержащие
HTML-специфичные символы ``< > &``

.. image:: images/26/spec.jpg
   :align: center

Дополнения
----------

[HTPBB-420] - Apply new design to "Persons" page
================================================

На новый дизайн переведены табличные страницы: **Persons**, **Users**, **Audit Log**, **Dashboard**

.. image:: images/26/persons.jpg
   :align: center

[HTPBB-423] - Apply new design to profile editing page - sections "Connections", "Personal Interests", "Life In Brief" and "Album"
==================================================================================================================================

Закончен перевод на новый дизайн страниц для редактиррования анкеты.

.. image:: images/26/edit.jpg
   :align: center

[HTPBB-424] - Apply new design to pages referenced from "Dictionaries"
======================================================================

Закончен перевод на новый дизайн страниц для редактиррования справочников и каталогов.

.. image:: images/26/activity.jpg
   :align: center

[HTPBB-426] - Apply new design to error pages for HTTP results 401, 403, 404, 500/501
=====================================================================================

На новый дизайн переведена страница, отображаемая в случае ошибки 
(например "Искомая страница не найдена").

.. image:: images/26/404.jpg
   :align: center

[HTPBB-428] - Do not create new version on "Save/Take/Approve/Finish" when there were no changes in profile
===========================================================================================================

Нажатие кнопок **Save/Take/Approve/Finish** при редактировании анкеты не создает новую версию в базе данных.

[HTPBB-430] - Add "History of changes" section to person-view page
==================================================================

На страницу просмотра анкеты добавлен список истории изменений 
(последние 5 версий):

.. image:: images/26/changes.jpg
   :align: center

