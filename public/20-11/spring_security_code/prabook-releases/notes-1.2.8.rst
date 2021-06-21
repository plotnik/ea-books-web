---------------------------------
PraBook ver. 1.2.8 (18.06.2013)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'; Mariya Alferovich <alferovich@PARK.BY>; 
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', 'Андрушкевич Михаил <mandrushkevich@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.2.8

**Внимание:**
    `Для того, чтобы гарантированно подхватить обновленные базовые стили,
    при первом открытии измененных страниц рекомендуется обновить кэш браузера` (**Ctrl+F5** в Firefox).

Исправления
-----------

.. Исправлены некоторые проблемы с компонентом ввода дат

[HTPBB-604] - Dates in date components is not "birth date + 100 years"
======================================================================

Исправлена проблема с предлагаемым диапазоном (100 лет от даты рождения).

[HTPBB-610] - "Death" Dropdown list is not correct for b.c.
===========================================================

Исправлена проблема возникавшая при вводе дат до нашей эры.
  
[HTPBB-606] - Search field is cleared after clicking on the "Clear" button in the "Narrow your search" menu
===========================================================================================================

Исправлена проблема, когда по кнопке "Clear" вместе с полями уточняющего поиска "Narrow your search"
очищалось основное поле поиска вверху страницы.

[HTPBB-632] - Activity Catalog page give "Error 404. Page not found"
====================================================================

Исправлена проблема со справочником "Activity Catalog"

[HTPBB-657] - Problems with slow input in Advanced Search panel
===============================================================

Исправлена проблема ввода для полей уточняющего поиска "Narrow your search"

[HTPBB-675] - NullPointerException for old PhotoIcons
=====================================================

Исправлена проблема, когда не отображались фотографии в старых анкетах.

[HTPBB-631] - Names of relations containing quotes do not allow editing page to open
====================================================================================

Исправлена проблема, возникавшая, когда в именах родственников был введен символ "кавычки"

[HTPBB-637] - "Deceased" mark hides only Death date, but Resting Place still remains
====================================================================================

Флажок "Deceased" при редактировании не прятал поле ввода "Resting Place"


Дополнения
----------

[HTPBB-651] - Maintain DB consistency for adm.units
===================================================

Из таблицы ``administrative_units`` с названиями населенных пунктов:

    - удалены пункты с пустыми именами

    - из названий пунктов удалены запятые (это недопустимый символ, он используется для отделения названий родительских областей) 

    - слиты в один пункты, имеющие одинаковое "полное имя" (то есть название пункта плюс названия родительских областей, отделенные запятыми), 

Например, пункт с полным именем ``Kensington, London, England, UK`` называется ``Kensington`` и расположен внутри пункта ``London``. 

[HTPBB-655] - In adm.unit dictionary show full name of adm.unit in list
=======================================================================

Страница справочника **Administrative Units** теперь показывает полные имена для населенных пунктов.

.. image:: images2/08/adm_unit_list.jpg
   :align: center

[HTPBB-656] - Merge/Edit screens for adm.units should operate with full names
=============================================================================
   
Экраны **Merge** и **Edit** теперь оперируют полными именами населенных пунктов.

.. image:: images2/08/adm_unit_merge.jpg
   :align: center
   
[HTPBB-664] - Automerge problems for adm units
==============================================

Экран **Automerge** также работает с полными именами населенных пунктов.

[HTPBB-653] - "Reset Status" and "Delete" buttons on profile editing screen should not perform validation
=========================================================================================================

Кнопки **Reset Status** и **Delete** на странице редактирования теперь не требуют приведения всех полей анкеты 
в соответствие с текущими правилами валидации перед выполнением требуемой операции.

[HTPBB-654] - Extend text field sizes from 3000 to 10000
========================================================

Размеры многострочных текстовых полей в анкетах увеличены до 10000 символов.

[HTPBB-661] - Update person-view page to new design
===================================================

Страница просмотра анкеты переведена на новый дизайн.

.. image:: images2/08/person_view.jpg
   :align: center

[HTPBB-663] - Allow Prabook Search to be accessed without Facebook login
========================================================================

Поиск и просмотр аппрувленных анкет в Prabook теперь не требуют логина Facebook.

[HTPBB-665] - Minor updates to edit page design
===============================================

Некоторые изменения на странице редактирования:

    - Заменена пустая фотография 
    - Курсор изменяется на указатель при наведении на изображения

[HTPBB-668] - Selection of main photos for school / university / career
=======================================================================

Добавлена возможность выбора "главных" фотографий для разделов *School / University / Career* 

.. image:: images2/08/main_school.jpg
   :align: center

[HTPBB-666] - Add "Works description" field to profile
======================================================

Добавлено поле **Works description** в раздел **Works**

.. image:: images2/08/works_description.jpg
   :align: center

[HTPBB-669] - Add list of official titles to profile
====================================================

В раздел **Career** добавлен список **Official titles** 
для показа на странице просмотра анкеты согласно новому дизайну.

.. image:: images2/08/official_title.jpg
   :align: center

