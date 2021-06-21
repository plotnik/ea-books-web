---------------------------------
PraBook ver. 1.2.6 (23.11.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'; Mariya Alferovich <alferovich@PARK.BY>; 
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', 'Андрушкевич Михаил <mandrushkevich@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.2.6

**Внимание:**
    `Для того, чтобы гарантированно подхватить обновленные базовые стили,
    при первом открытии измененных страниц рекомендуется обновить кэш браузера` (**Ctrl+F5** в Firefox).

Исправления
-----------


[HTPBB-526] - "Career description" field shows "<br/>" instead of supporting line breaks
========================================================================================

Исправлена проблема с тэгами ``<br/>``, возникавшая для поля **Career description**.

.. image:: images2/06/career_descr.jpg
   :align: center

[HTPBB-528] - List of parties shouldn't be displayed if empty
=============================================================

Исправлена проблема с отображением списка партий.

.. image:: images2/06/parties.jpg
   :align: center


Дополнения
----------

[HTPBB-515] - Move "Narrow your search" menu to the left side
=============================================================

Кнопка **Narrow your search** смещена в левую панель на экране поиска.

[HTPBB-517] - Minor changes in exterior of search page according to requirements from 18.10.2012
================================================================================================

В соответствии с требованиями в письме от 18.10.2012 внесены изменения на экране поиска:

1. Стиль текста "Found xxx profiles"
2. Ключевое слово в результатах поиска выделяется жирным шрифтом
3. Изменен шрифт в результатах поиска
4. В результат поиска добавлена дата рождения
5. **Activity** удалено из результатов поиска
6. Фотография удалена из результатов поиска

.. image:: images2/06/scrshot2.jpg
   :align: center

[HTPBB-518] - Changes in "Search Result Extended Information" popup window according to requirements from 18.10.2012
====================================================================================================================

В соответствии с требованиями в письме от 18.10.2012 изменена правая панель на экране поиска:

.. image:: images2/06/rpanel.jpg
   :align: center

[HTPBB-519] - In search results provide first line from General Info field as well as line containing the match
===============================================================================================================

В результатах поиска выводится теперь как начало анкеты, так и фрагмент, содержащий шаблон поиска.

.. image:: images2/06/double.jpg
   :align: center

[HTPBB-520] - "Reset status" button for Administrator
=====================================================

Для администратора добавлена кнопка **Reset status**, переводящая статус анкеты в ``INITIAL``.

.. image:: images2/06/reset.jpg
   :align: center

[HTPBB-521] - Add links to 20 first profiles using this dictionary element to dictionary element editing screen
===============================================================================================================

На экран редактирования элемента словаря добавлены линки на 
20 первых анкет, использующих этот элемент.

.. image:: images2/06/dict_links.jpg
   :align: center

[HTPBB-522] - Fields cannot be empty: 1.Political Vews -> Membership 2.Education -> School 3.Education -> College/University
============================================================================================================================

Добавлен запрет на сохранение пустых значений для полей:

  1. Political Vews -> Membership 
  2. Education -> School 
  3. Education -> College/University

[HTPBB-523] - Automatic Merge for dictionaries
==============================================

Выполненные операции **Merge** можно просмотреть и повторно запустить через экран **Auto Merge**
(линк доступен для администратора в главном меню).

.. image:: images2/06/automerge.jpg
   :align: center

[HTPBB-529] - "Spelling variants" field should be required
==========================================================

Теперь Prabook не дает сохранить анкету с незаполненным полем **Spelling variants**.

.. image:: images2/06/spelling_variants.jpg
   :align: center

[HTPBB-530] - Add death date and place to person-view page
==========================================================

На странице просмотра анкеты теперь отображается дата смерти, если она заполнена.

.. image:: images2/06/death.jpg
   :align: center

[HTPBB-531] - Do not show question sign in incomplete periods
=============================================================

В периодах теперь указываются слова *from* и *to*.

.. image:: images2/06/fromto.jpg
   :align: center

[HTPBB-532] - In validation message for the required field always specify field name
====================================================================================

В сообщении об ошибке при сохранении анкеты теперь указывается 
название табуляции для проблемного поля, сама табуляция подсвечивается и на нее осуществляется переход.

.. image:: images2/06/errortab.jpg
   :align: center

[HTPBB-534] - Create "Complain" button with redirect to Facebook
================================================================

Добавлена кнопка **Complain**, позволяющая редактору пожаловаться 
на содержание анкеты через группу приложения в Facebook.

.. image:: images2/06/complain.jpg
   :align: center

[HTPBB-535] - Add "Privacy Policy" page
=======================================

По требованию Facebook добавлена страница **Privacy Policy**

.. image:: images2/06/privacy.jpg
   :align: center

[HTPBB-536] - "Connections > Descriptions" field missing on person-view page
============================================================================

Поле **Connections > Descriptions** теперь отображается при просмотре анкеты.

.. image:: images2/06/connections.jpg
   :align: center

