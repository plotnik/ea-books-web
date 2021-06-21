---------------------------------
PraBook ver. 1.2.0 (27.08.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'; Mariya Alferovich <alferovich@PARK.BY>; 'Ksenia Titova <devlon4ik@gmail.com>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', 'Андрушкевич Михаил <mandrushkevich@exadel.com>', (Дарина Матвиенко?, Андрей Головнев?)

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями:

.. contents:: Изменения в релизе 1.2.0


Дополнения
----------

[HTPBB-473] - Update design for Prabook main page
=================================================

Обновлена в соответствии с новым дизайном первая страница приложения.
При первом открытии
рекомендуется обновить кэш браузера (`Ctrl+F5` в Firefox)
чтобы гарантированно подхватить новые базовые стили.

Линки **About**, **Terms of Use**, **Contacts** (в нижней части экрана)
сейчас никуда не ведут, потому что таких страниц в приложении пока нет.
(Если их нужно добавить, то нам нужны указания насчет их содержимого и дизайна).

.. image:: images2/00/home.jpg
   :align: center

[HTPBB-476] - Create database migration script to strip out <font> and <a> tags from "Life In Brief" field
==========================================================================================================

Из биографий в анкетах (поле **Life in Brief**) полностью удалена информация о шрифтах и цвете текста. 
Также из текста биографий удалены ссылки. Встроенный редактор для **Life in Brief** пока еще позволяет
сохранять эту информацию, но в будущем информация о шрифтах, цвете текста и ссылках
для биографий в анкетах сохраняться не будет.

.. image:: images2/00/bio.jpg
   :align: center

[HTPBB-474] - "Work Results" field should support line breaks
=============================================================

Поле **Work results** теперь поддерживает отображение текста в несколько строк.

.. image:: images2/00/work.jpg
   :align: center

[HTPBB-472] - Replace label "Details" with "Ethnicity Details" on profile editing screen
========================================================================================

Метка поля уточнена до **Ethnicity Details**, чтобы подчеркнуть, что эта информация относится 
именно к этничности персоны.

.. image:: images2/00/ethnicity.jpg
   :align: center


