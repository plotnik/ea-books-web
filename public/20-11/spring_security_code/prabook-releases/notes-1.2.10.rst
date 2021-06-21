---------------------------------
PraBook ver. 1.2.10 (19.07.2013)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'; Mariya Alferovich <alferovich@PARK.BY>; 
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', 'Андрушкевич Михаил <mandrushkevich@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.2.10

**Внимание:**
    `Для того, чтобы гарантированно подхватить обновленные базовые стили,
    при первом открытии измененных страниц рекомендуется обновить кэш браузера` (**Ctrl+F5** в Firefox).

Исправления
-----------

[HTPBB-645] - Incorrect display of activities or nationalities with quotes
==========================================================================

Исправлена проблема с отображением `activities` и `nationalities`, 
содержащих апострофы, в таблицах
административных экранов.

[HTPBB-687] - URL should be updated when search field has been changed
======================================================================

Исправлена проблема со сменой страниц на экране поиска.

[HTPBB-688] - Incorrect interface for view previous version page
================================================================

Исправлена проблема для показа страниц предыдущих версий анкеты.

.. image:: images2/10/versions.jpg
   :align: center
   
[HTPBB-689] - Incorrect search query after click on bold link
=============================================================

Исправлена проблема для поиска по выделенным элементам анкеты.

.. image:: images2/10/educator.jpg
   :align: center

[HTPBB-691] - Problem with date
===============================

Исправлена проблема, возникавшая, если в поле года для даты вводить более 4х символов.

.. image:: images2/10/dates.jpg
   :align: center

[HTPBB-695] - Administrator is not able to switch actual version
================================================================

Исправлена проблема, когда линки "Make actual" были недоступны для Администратора.

.. image:: images2/10/actual.jpg
   :align: center


[HTPBB-704] - Profile's status couldn't be "APPROVED by Edit Prabook"
=====================================================================

Исправлена проблема с отображением статуса анкеты на странице редактирования.



Дополнения
----------


[HTPBB-671] - In general search try "Name Surname" combination after "Surname Name"
===================================================================================

Проанализирована проблема и проверен факт, что порядок "Имя/Фамилия" в строке поиска
будет работать также хорошо, как и порядок "Фамилия/Имя".

[HTPBB-673] - Investigate possibility to match activity only as a whole word in general search
==============================================================================================

Изменены приоритеты поиска. Теперь поля **Activity** и **Activity Caategory**
все еще имеют наивысший приоритет, но попадают в результаты поиска только
если они целиком совпадают с запросом. 

[HTPBB-674] - Limit visibility of "Directories" and "Persons" page to administrators
====================================================================================

Страницы **Directories** и **Persons** теперь доступны только администраторам.

[HTPBB-681] - Upgrade Solr to latest version 3.6.2
==================================================

Произведен апгрейд поискового сервера Solr до версии 3.6.2, что устраняет ряд проблем с 
поиском и увеличивает его скорость.

[HTPBB-686] - Provide checkboxes on Save to lock profile and hide from Contributors
===================================================================================

Добавлены чекбоксы  **Available for editing** и **Don't display me as a contributor**

.. image:: images2/10/checkboxes.jpg
   :align: center

[HTPBB-693] - Rename "Finish" button to "Publish"
=================================================

Кнопка **Finish** на странице редактирования анкеты переименована в **Publish**

[HTPBB-694] - Make font in search hint comboboxes larger
========================================================

Увеличен размер шрифта для выпадающих подсказок при поиске.

.. image:: images2/10/search_font.jpg
   :align: center

[HTPBB-696] - Rename FINISHED status to PUBLISHED on administrative screens
===========================================================================

В таблицах на административных экранах статус ``FINISHED`` переименован в ``PUBLISHED``.

[HTPBB-697] - "Take" and "Create" buttons are renamed to "Save"
===============================================================

Кнопки **Take** и **Create** на странице редактирования анкеты переименованы в "Save".
После создания новой анкеты она сразу попадает в статус ``TAKEN``.

[HTPBB-698] - Add hints to status buttons
=========================================

Добавлены подсказки к кнопкам на странице редактирования.

.. image:: images2/10/hints.jpg
   :align: center

[HTPBB-699] - Align "Contributor" and "Go up" to the bottom of the page
=======================================================================

Поле **Contributor** привязано к низу окна для малозаполненных анкет:

.. image:: images2/10/contributors.jpg
   :align: center

