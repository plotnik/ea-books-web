---------------------------------
PraBook ver. 1.2.5 (26.10.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'; Mariya Alferovich <alferovich@PARK.BY>; 
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', 'Андрушкевич Михаил <mandrushkevich@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.2.5

**Внимание:**
    `Для того, чтобы гарантированно подхватить обновленные базовые стили,
    при первом открытии измененных страниц рекомендуется обновить кэш браузера` (**Ctrl+F5** в Firefox).

Исправления
-----------

[HTPBB-511] - Only first results page is loaded on the Search page in IE8/9
===========================================================================

Исправлена проблема, возникавшая при просмотре страницы поиска в Internet Explorer.

[HTPBB-514] - Pagination works incorrectly
==========================================

Исправлена проблема, возникавшая на странице поиска при переходе между страницами 
результатов.

[HTPBB-516] - HTML tags are worked for Career Description field and Dropdowns
=============================================================================

Исправлена проблема для поля **Career Description**, возникавшая
при вводе HTML-тэгов (символы `<>&`)


Дополнения
----------


[HTPBB-510] - Replace Rich Text Editor for General Info with plain text area and strip HTML tags from life_in_brief field in database
=====================================================================================================================================

Rich Text Editor для поля **General Info** заменен на обычный текстовый редактор без поддержки форматирования.
Форматирующие HTML-тэги удалены из этого поля в базе данных.

.. image:: images2/05/bio.jpg
   :align: center

[HTPBB-512] - If dictionary element to be created already exists, link should be provided to the existing one.
==============================================================================================================

При попытке создания элемента справочника с уже существующим именем выдается ссылка на уже существующий элемент.

.. image:: images2/05/president.jpg
   :align: center


[HTPBB-513] - Changes from Administrator shouldn't lock profile for Editor
==========================================================================

Если анкета находится в статусе **Finished**, администратор может внести в нее свои правки
без того, чтобы анкета стала недоступной оригинальному редактору.



