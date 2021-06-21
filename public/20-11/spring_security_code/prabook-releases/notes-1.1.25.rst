---------------------------------
PraBook ver. 1.1.25 (13.04.2012)
---------------------------------

    :To: 'Tsepkalo Valery <director@park.by>'; 'Мартинкевич Александр Михайлович <Martinkevich@park.by>'; 'Sergey Severin <S.Severin@park.by>'
    :Cc: 'HTP PeopleBook <htp-peoplebook-management-project@exadel.com>', Татьяна Боровкова [borovkova.t.v@gmail.com], Андрей Головнев (ahalauniou@exadel.com)

.. |to|  image:: file:///D:/album/freemind/forward.png

Здравствуйте,

К сегодняшней дате мы подготовили релиз со следующими дополнениями и исправлениями:



Исправления
-----------

**[HTPBB-417]** - `"Merge" for dictionaries is not performed if we paste value in combobox instead of selecting it from the list` 

Исправлена проблема, не позволявшая переименовывать элементы справочников,
если новое имя скопировано в поле с помощью `Ctrl+V`, а не выбрано из списка.

.. image:: images/25/merge.jpg
    
--------------------

Дополнения
----------

**[HTPBB-414]** - `Apply new "rubber" design to already migrated pages`

Изменено поведение центральной информационной полосы при растягивании
окна браузера. Теперь она растягивается вместе с окном.
Раньше она имела фиксированную ширину.

.. image:: images/25/rubber.jpg

--------------------

**[HTPBB-415]** - `Search hints shouldn't display profiles in "Initial" and "Taken" statuses`

Подсказки при поиске теперь не отображают анкет в статусах ``Initial`` и ``Taken``.

.. image:: images/25/hints.jpg

--------------------

**[HTPBB-416]** - `For the newly created profile allow to jump to duplicate when name/surname entered`

Если при создании новой анкеты введенные имя и фамилия совпадают
с именем и фамилией уже существующей анкеты, при переходе к
следующему полю будет выдано соответствующее предупреждение и 
предложен линк на существующую анкету.

.. image:: images/25/duplic.jpg

--------------------

**[HTPBB-418]** - `Apply v11 design to "recently-created / day-in-history / dictionaries" pages`

На новый дизайн переведены страницы:

:recently-created: расширенный список недавно созданных страниц, доступный по линку **see more** для блока **RECENTLY CREATED** в правой панели. 
:day-in-history: расширенное описание текущего дня, доступное по линку **see more** для блока **THIS DAY IN HISTORY** в правой панели
:dictionaries: список справочников и каталогов

.. image:: images/25/recent.jpg

--------------------

| **[HTPBB-419]** - `Apply new design to profile editing page - "General" section`
| **[HTPBB-421]** - `Apply new design to profile editing page - sections "Religion and Philosophy" and "Political Views"`
| **[HTPBB-422]** - `Apply new design to profile editing page - sections "Education" and "Work"`

На новый дизайн переведена страница редактирования анкеты:

.. image:: images/25/edit.jpg

