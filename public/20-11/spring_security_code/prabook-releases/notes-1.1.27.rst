---------------------------------
PraBook ver. 1.1.27 (28.04.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', Татьяна Боровкова [borovkova.t.v@gmail.com], Андрей Головнев (ahalauniou@exadel.com)

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.1.27

Исправления
-----------

[HTPBB-433] - Protect application from JavaScript injections 
============================================================

Закрыты обнаруженные уязвимости безопасности приложения
(возможность внедрения скрипта в приложение через поля ввода).


[HTPBB-434] - "Add Event" button on "Day in History" editing screen is not working 
==================================================================================

Исправлены проблемы с добавлением событий на странице **Day in History**

.. image:: images/27/addevent.jpg
   :align: center

[HTPBB-435] - Problem selecting interval of dates with Calendar component on Search page 
========================================================================================

[HTPBB-442] - Typing in "Education" box on "Advanced Search" page opens component in a wrong place 
Исправлены проблемы при поиске в интервале дат.

.. image:: images/27/date_intv.jpg
   :align: center


[HTPBB-437] - In case of timeout for AJAX request on Advanced Search page the "Loading Progress" indicator should be removed 
============================================================================================================================

Исправлена проблема с индикатором поиска.

.. image:: images/27/indicator.jpg
   :align: center


[HTPBB-439] - "500 Internal server error" is displayed for expired Facebook login until AJAX request performs relogin
=====================================================================================================================

Устранено неуместное сообщение об ошибке, возникавшее, пока система ожидала ответа от Facebook
на авторизационный запрос.

[HTPBB-442] - Typing in "Education" box on "Advanced Search" page opens component in a wrong place 
==================================================================================================

Исправлена проблема с полем поиска **Education** 

.. image:: images/27/educ.jpg
   :align: center

[HTPBB-445] - Problems with "Day in History" editing screen 
===========================================================

Исправлены проблемы на экране **Day in History** 

.. image:: images/27/hist.jpg
   :align: center

[HTPBB-449] - Entering "Alvaro Uribe Velez" on Home page will not pass this name to Advanced Search name    
========================================================================================================

Исправлена проблема, когда имена, содержащие интернациональные символы,
не передавались на страницу для поиска.


Дополнения
----------

[HTPBB-432] - Adjust tree component on "Persons" page to table size 
===================================================================

Компонент для поиска пустых полей на экране **Persons** теперь выравнивается по размеру таблицы.

.. image:: images/27/persons.jpg
   :align: center

[HTPBB-436] - Hide main photo from Album on profile-view page 
=============================================================

В альбоме анкеты теперь показываются все фотографии, кроме главной фотографии анкеты.

.. image:: images/27/mainphoto.jpg
   :align: center

[HTPBB-440] - Search hints shouldn't include dictionary catalogs 
================================================================

Подсказки поиска на главной странице не включают теперь каталоги справочников.

[HTPBB-441] - Typing in "Advanced Search" comboboxes brings unwanted "Loading" message for each key pressed 
===========================================================================================================

Проанализирована возможность спрятать сообщение `Loading` для динамически подгружаемых списков.
Установлено, что используемая библиотека Ext JS 4.0 такой возможности не поддерживает.

[HTPBB-443] - History section on person-view page should be collapsed by default 
================================================================================

Секция истории изменений при просмотре анкеты по умолчанию спрятана.

.. image:: images/27/history.jpg
   :align: center

[HTPBB-444] - "Sex" label should be replaced with "Gender"
==========================================================

Метки "Sex" на экранах приложения заменены на "Gender"

.. image:: images/27/sex.jpg
   :align: center
   
[HTPBB-446] - Add slogan at home page   
=====================================

На главную страницу приложения добавлен лозунг.

.. image:: images/27/slogan.jpg
   :align: center
   
[HTPBB-447] - On profile-view page empty blocks of "half-field" class should be removed 
=======================================================================================

Пустые подсекции не отображаются при просмотре анкеты.

.. image:: images/27/subsect.jpg
   :align: center
   
[HTPBB-448] - Make left- and right-side sections collapsible on "Advanced Search" screen 
========================================================================================

Клик по заголовку секции в левой и правой полосах скрывает секцию.
Состояние "сложенности" секции для данного пользователя сохраняется,
даже если перезапустить браузер.

.. image:: images/27/collapse.jpg
   :align: center

