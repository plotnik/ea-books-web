---------------------------------
PraBook ver. 1.2.7 (19.02.2013)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'; Mariya Alferovich <alferovich@PARK.BY>; 
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', 'Андрушкевич Михаил <mandrushkevich@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.2.7

**Внимание:**
    `Для того, чтобы гарантированно подхватить обновленные базовые стили,
    при первом открытии измененных страниц рекомендуется обновить кэш браузера` (**Ctrl+F5** в Firefox).

Исправления
-----------


[HTPBB-544] - Relative description displays international symbols incorrectly
=============================================================================

Исправлена проблема с отображением символов в поле "Relative description"

.. image:: images2/07/rel_desc.jpg
   :align: center


[HTPBB-551] - Problem updating "Career/Description" field
=========================================================

Исправлена проблема, возникавшая для поля "Career/Description"


Дополнения
----------

[HTPBB-537] - Add geo locations from GEODATASOURCE-CITIES-FREE.TXT.ZIP into administrative_unit table
=====================================================================================================

В таблицу ``administrative_unit`` загружено более 2х млн названий 
населенных пунктов из файла ``GEODATASOURCE-CITIES-FREE.TXT.ZIP``.

[HTPBB-540] - Editing of administrative_unit dictionary via web interface
=========================================================================

Добавлена возможность редактирования справочника населенных пунктов с возможностью их
иерархической организации.

.. image:: images2/07/adm_unit.jpg
   :align: center


[HTPBB-542] - "Spelling variants" field should NOT be required
==============================================================

Поле "Spelling variants" сделано необязательным.

[HTPBB-545] - Contributors list should mention each editor only once
====================================================================

Список **Contributors** на странице просмотра анкеты
показывает каждого редактора только один раз.
Администраторы исключены из этого списка.
Список отсортирован по датам первой редакции,
но показывает даты последней редакции.

.. image:: images2/07/contribs.jpg
   :align: center


[HTPBB-546] - Add check for duplicates with Spelling Variants according to 27.11.2012 email
===========================================================================================

Добавлено правило проверки на дубликаты для поля **Spelling Variants**. 
Допустим, анкета №1 уже существует. Мы добавляем анкету №2.
Мы считаем анкету дубликатом, если:

    - Name1 = name2
    - Surname1 = surname2
    - Birth date1 = birthdate2

Мы также считаем анкету дубликатом, если:
    
    - Name1 != name2
    - Surname1 != surname2
    - Spelling variants1 = name2 and surname2
    - Birth date1 = birthdate2


[HTPBB-547] - Validation rules for list elements in profiles
============================================================

Сняты проверки на допустимость для следующих списочных элементов:

    - PoliticalVews -> Membership
    - Education-> School
    - Education-> College/University
    - Career name
    - Award name
    - Publications
    
Для **Career** поле **period** является обязательным.
Для **Publications** поле **name** является обязательным.

[HTPBB-548] - If matching line in search result duplicates the beginning of General Info, then show 4 first lines of General Info instead of 2
==============================================================================================================================================

Если в результатах поиска строка с результатом совпадает с начальной строкой **General Info**,
то мы показываем 4 строки **General Info** вместо 2х.

.. image:: images2/07/pablo.jpg
   :align: center

[HTPBB-549] - Extend descriptions for "Connections/Other connections" to 64 kb and increase appropriate text field size on editing screen
=========================================================================================================================================

Размер поля **Description** для **Connections/Other connections** расширен до 64 kb

[HTPBB-550] - Popup profile in search results should move along with highlighted profile
========================================================================================

Расширенное окошко для найденной анкеты теперь показывается рядом со своим результатом поиска.

.. image:: images2/07/popup_profile.jpg
   :align: center

[HTPBB-552] - Customize JS components for Date on editing page to follow birth date value
=========================================================================================

- Флажок BC исчезает в компонентах даты, если он не выбран для даты рождения.
- Даты в компонентах дат должны предлагаться в диапазоне 100 лет от даты рождения.


[HTPBB-553] - New design for Name, Surname, Spelling variants
=============================================================

- **Name** и **Surname** имеют свои собственные поля **Spelling Variants**
- Добавлено поле **Middle name**
- Существующие значения **Spelling Variants** заменены одним полем **Pseudonym**, 
  в котором существующие значения разделены запятой.

.. image:: images2/07/sp_vars.jpg
   :align: center

[HTPBB-555] - Remove "Major" field for "College/University" and "Favorite music artists" for "Personal Interests"
=================================================================================================================

Удалено поле **Major** из секции **College/University** и поле **Favorite music artists** из секции **Personal Interests**

[HTPBB-557] - Update "General" editing page to new design
=========================================================

Страница редактирования анкеты **General** переведена на новый дизайн.

[HTPBB-563] - Update hints for profile editing screens - part 1
===============================================================

Для некоторых полей на страницах редактирования анкеты
установлены новые тексты подсказок.

.. image:: images2/07/general.jpg
   :align: center


[HTPBB-558] - Update "Education" editing page to new design
===========================================================

Страница редактирования анкеты **Education** переведена на новый дизайн.

.. image:: images2/07/education.jpg
   :align: center

[HTPBB-560] - Update "Career" editing page to new design
========================================================

Страница редактирования анкеты **Career** переведена на новый дизайн.

.. image:: images2/07/career.jpg
   :align: center

[HTPBB-562] - Update "Connections" editing page to new design
=============================================================

Страница редактирования анкеты **Connections** переведена на новый дизайн.

.. image:: images2/07/connections.jpg
   :align: center

[HTPBB-564] - Update "Life Stance" editing page to new design
=============================================================

Страница редактирования анкеты **Life Stance** переведена на новый дизайн.

.. image:: images2/07/stance.jpg
   :align: center

[HTPBB-565] - Update "Album" editing page to new design
=======================================================

Страница редактирования анкеты **Album** переведена на новый дизайн.

.. image:: images2/07/album.jpg
   :align: center

[HTPBB-567] - Update design on Search page
==========================================

Согласно новым требованиям подправлен дизайн страницы поиска.

.. image:: images2/07/search.jpg
   :align: center

[HTPBB-559] - Modify Nationality on search page (e.g. Belarusian for Belarus, American for US)
==============================================================================================

В таблицу ``nationality`` добавлено поле ``name_form``, которое 
содержит грамматическую форму названия национальности, которая
учитывается при отображении результатов поиска. Если это поле не заполнено в базе,
при отображении результатов поиска используется основное название национальности.
Это поле для грамматической формы не редактируется с веб-интерфейса.
На текущий момент заполнено всего 2 значения:

- Belarusian for Belarus, 
- American for United States

.. image:: images2/07/grammar.jpg
   :align: center


[HTPBB-588] - "Award Description" field should support line breaks
==================================================================

Поле **Award Description** теперь поддерживает отображение текста в несколько строк.

