---------------------------------
PraBook ver. 1.1.28 (04.05.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', Татьяна Боровкова [borovkova.t.v@gmail.com], Андрей Головнев (ahalauniou@exadel.com)

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.1.28

Исправления
-----------

[HTPBB-452] - Solr full-import is not able to process BC dates
==============================================================

Исправлены проблемы, возникавшие на экране поиска с результатами,
содержащими даты до нашей эры.

[HTPBB-455] - Image crop functionality on person-edit page is not working in Chrome
===================================================================================

Исправлена проблема с выделением видимой области на главной фотографии
для браузера Chrome.

.. image:: images/28/chrome.jpg
   :align: center


Дополнения
----------

[HTPBB-450] - Add support for BC dates on "Advanced Search" screen
==================================================================

Добавлена возможность указывать дату для поиска до нашей эры с 
помощью соответствующего чекбокса.

.. image:: images/28/bc.jpg
   :align: center

[HTPBB-451] - Possibility to upload several photos per one operation
====================================================================

Добавлена возможность загружать несколько фотографий в альбом за одну операцию.

.. image:: images/28/photos.jpg
   :align: center

[HTPBB-453] - Remove "This person also known as" from person-view page
======================================================================

Поле "This person also known as" удалено с экрана просмотра анкеты
и переименовано на экране редактирования.

.. image:: images/28/pseudo.jpg
   :align: center

[HTPBB-454] - Move "This person on the internet" from the top of person-view page
=================================================================================

Поле "This person on the internet" перенесено в конец анкеты при просмотре.
В этом поле могут быть указаны персональный сайт, блог, страница 
персоны, описываемой анкетой. Если в этом поле не указано никаких адресов, оно будет скрыто.
Заголовок представляет собой линк для поиска в Google по имени.

.. image:: images/28/inet.jpg
   :align: center

