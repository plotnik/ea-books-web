---------------------------------
PraBook ver. 1.2.1 (28.09.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'; Mariya Alferovich <alferovich@PARK.BY>; 'Ksenia Titova <devlon4ik@gmail.com>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', 'Андрушкевич Михаил <mandrushkevich@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.2.1


Исправления
-----------

[HTPBB-478] - Merge not working for "Political Party" dictionary
================================================================

Исправлена проблема с функцией "Merge" для справочника "Political Party".


Дополнения
----------

[HTPBB-480] - Update design for Prabook Search page
===================================================

Обновлена в соответствии с новым дизайном страница поиска.
При первом открытии
рекомендуется обновить кэш браузера (`Ctrl+F5` в Firefox)
чтобы гарантированно подхватить новые базовые стили.

.. image:: images2/01/search.jpg
   :align: center

[HTPBB-482] - Update design for View Profile page
=================================================

Обновлена в соответствии с новым дизайном страница просмотра анкеты.
При первом открытии
рекомендуется обновить кэш браузера (`Ctrl+F5` в Firefox)
чтобы гарантированно подхватить новые базовые стили.

.. image:: images2/01/view.jpg
   :align: center

[HTPBB-475] - Strip out <font> and <a> tags when saving "Life In Brief" field in profile
========================================================================================
[HTPBB-484] - Strip out "style" attribute when saving "Life In Brief" field in profile
======================================================================================

Встроенный редактор для **Life in Brief** 
при сохранении анкеты удаляет из этого поля информацию о шрифтах и цвете текста.
Также из текста биографии удаляются ссылки. 

[HTPBB-483] - Create database migration script to strip out "style" attribute from "Life In Brief" field
========================================================================================================

Из всех анкет автоматически удален тэг ``<style>``,  
который добавляется в некоторых случаях при копировании информации из MS Word.
и содержит информацию о шрифтах и цвете текста.


