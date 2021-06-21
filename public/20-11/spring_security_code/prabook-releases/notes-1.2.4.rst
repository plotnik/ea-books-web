---------------------------------
PraBook ver. 1.2.4 (19.10.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'; Mariya Alferovich <alferovich@PARK.BY>; 
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', 'Андрушкевич Михаил <mandrushkevich@exadel.com>'

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:

.. contents:: Изменения в релизе 1.2.4

**Внимание:**
    `Для того, чтобы гарантированно подхватить обновленные базовые стили,
    при первом открытии измененных страниц рекомендуется обновить кэш браузера` (**Ctrl+F5** в Firefox).

Исправления
-----------

[HTPBB-504] - Some profiles are missing main photos
===================================================

Исправлена проблема, когда на некоторых анкетах не показывалась главная фотография.

[HTPBB-507] - Card on home page is not centered
===============================================

Карточка с полем поиска на заглавной странице отцентрирована по высоте. 


[HTPBB-509] - Crop functional works incorrect
=============================================

Исправлена проблема с выделением области просмотра для главной фотографии.

.. image:: images2/04/crop.png
   :align: center

[HTPBB-502] - Previous version of profile is not using new design
=================================================================

Исправлена проблема для страницы просмотра версии анкеты
(доступна через **Persons > Show Versions**)


Дополнения
----------
   
[HTPBB-500] - "Add profile" button in "Connections" section
===========================================================

В секции **Connections** добавлена кнопка **Add profile**,
позволяющая выбирать уже существующую анкету.
Раньше эта функциональность была доступна, только если в поле **Name**
было введено имя из существующей анкеты. В этом случае поле **Name**
становилось серым.

.. image:: images2/04/profile.jpg
   :align: center

[HTPBB-501] - Same search result page should be displayed when user returns back from viewing some profile
==========================================================================================================

Если на странице поиска номер N перейти на одну из анкет, а затем нажать кнопку **Back**,
то браузер вернется к странице поиска номер N.

.. image:: images2/04/poisk.jpg
   :align: center


[HTPBB-503] - Investigate possibility to support Back button on Home page
=========================================================================

Теперь возможно вернуться со страницы поиска на заглавную страницу 
с помощью кнопки **Back** браузера.

[HTPBB-505] - "Description" field should be added to "Connections" section
==========================================================================

В секции **Connections** добавлено поле **Description** (макс.длина 255 символов)

.. image:: images2/04/rel.jpg
   :align: center

[HTPBB-506] - Enhance "Description" fields on editing page
==========================================================

Для того, чтобы визуально усилить поля описаний мы 
сделали области для этих полей больше
и выделили жирным заголовки:
    
    - Political Views Description
    - School Description
    - University Description
    - "Career Description
    - Awards Description
    - Сonnections Description
    - Other Сonnections Description
    
.. image:: images2/04/polit.jpg
   :align: center

[HTPBB-508] - Fields "Career name" and "Award name" cannot be empty
===================================================================

При попытке сохранить пустые значения в полях **Career name** и **Award name**
будет выдано предупреждение.

