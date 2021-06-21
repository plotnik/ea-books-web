---------------------------------
PraBook ver. 1.1.10  (23.12.2011)
---------------------------------

    :To: Tsepkalo Valery; Мартинкевич Александр Михайлович; Северин Сергей Александрович [S.Severin@PARK.BY]  
    :Cc: 'HTP PeopleBook'


Здравствуйте,

К сегодняшней дате мы подготовили релиз 1.1.10.
Ниже идет описание изменений для этого релиза,
плюс изменения для "внутренних" релизов 1.1.8 и 1.1.9,
которые не публиковались в связи с недоступностью 
сервера ``prabook.org``

Исправления
-----------

| **[HTPBB-226]** `Editing names of dictionary categories throws an exception`
| **[HTPBB-259]** `For RelationType dictionary switching "Approve" flag with "Save" button gives error message "This value already exists in database"`
| **[HTPBB-215]** `"Value for all binded persons" combobox on Dictionary Element Editing Screen is not working`
| **[HTPBB-216]** `Changing Activity name to the value already existing in dictionary`
| **[HTPBB-239]** `Not existing value provided in Dictionary Element Rename throws an exception`
| **[HTPBB-250]** `An exception can occur when merging dictionaries if related tables have similar links`

   Исправлен ряд проблем, возникавших при редактировании и слиянии 
   элементов справочников.

-------------------------

| **[HTPBB-244]** `Editing "Life in Brief" field can throw an exception when there is too much content in field`

  Исправлена проблема, возникавшая при редактировании длинных строк в поле "Life in Brief".
  
-------------------------

**[HTPBB-254]** `Cell content is centered in tables for IE`

  Исправлена проблема с отображением таблиц справочников в Internet Explorer.
  
-----------------------

**[HTPBB-240]** `Search criteria passed from Tag Cloud is shown in combobox as gray`

  Исправлена проблема с отображением критерия поиска, переданного из "облака тэгов". 
  
-----------------------

Дополнения
----------

| **[HTPBB-221]** `Create prototype page for Frontend Catalog`
| **[HTPBB-228]** `Provide number of profiles using this category on Catalog page`
| **[HTPBB-231]** `Add link to "Catalog" page into main PraBook menu`

   Добавлен каталог анкет с разбиением по справочникам. Число рядом с названием
   категории (например, "ARTS & ENTERTAINMENT") указывает количество находящихся в ней анкет (3). 
   Сейчас идет работа
   по добавлению информации о количестве анкет также к отдельным подразделам 
   (т.е. элементам справочников).
   
   .. image:: images/10/catalog.jpg
   
--------------------   

| **[HTPBB-229]** `Add "Visible in Frontend" checkbox to dictionary pages`
| **[HTPBB-233]** `Add "Visible in Frontend" field to dictionary tables`
| **[HTPBB-241]** `Add "Frontend Visible" sortable column to 3 kinds of dictionary tables`
| **[HTPBB-246]** `Click on "Approved/Visible" columns in dictionary and category tables should change value of flag`

   В каталоге анкет будут показаны только те категории и элементы справочников,
   для которых включен флажок "Visible in Frontend".
   
   .. image:: images/10/dict_list.jpg

--------------------   

| **[HTPBB-234]** `Add "Day in History" section at the right side of frontend pages with birth dates from profiles`
| **[HTPBB-251]** `Show events for "Day in History" on Search page`

  В правой части страницы "Search" добавлена колонка "Day in History",
  в которой отображаются наиболее популярные персоны, у которых сегодня день рождения, 
  и последние события, годовщины которых отмечаются сегодня.

  .. image:: images/10/day_in_history.jpg

  Нажатие на линк "See All" в верхнем правом углу выдает расширенный 
  список персон и событий для сегодняшнего дня:
  
  .. image:: images/10/day_in_history_all.jpg
  
--------------------   
  
**[HTPBB-245]** `Screen to administer events for Day in History`

  Нажатие на линк "Edit" в верхнем правом углу предыдущего экрана позволяет 
  добавлять события для выбранного дня недели. Календарь внизу экрана позволяет 
  быстро переходить к выбранному дню:
  
  .. image:: images/10/day_in_history_add.jpg
  
--------------------   

**[HTPBB-235]** `Create "Remove links" button for "Life in brief" editing field`

  Редактор форматированного текста для поля "Life in brief" в анкете
  имеет кнопку "Remove links" (крайняя справа). Она предназначена для удаления
  ссылок из выделенного текста, и может быть полезна, чтобы удалить
  ссылки на внешние сайты, если информация скопирована, например,
  из Википедии:
  
  .. image:: images/10/remove_links.jpg
  
--------------------   

**[HTPBB-256]** `Add "See also" section on Profile View page using existing rule engine (rules-definition.xml)`

  При просмотре анкеты подбирается и показывается внизу экрана список анкет,
  подобных данной ("Similar Persons"):
  
  .. image:: images/10/similar_persons.jpg
  
--------------------   

**[HTPBB-224]** `Add "Most Popular Profiles" section at the right side of frontend pages`

  В правой части страницы "Search" добавлена колонка "Most Viewed", 
  в которой отображаются наиболее часто просматриваемые анкеты:
  
  .. image:: images/10/most_viewed.jpg

--------------------   
  
**[HTPBB-227]** `Add "Recently Created Profiles" section at the right side of frontend pages`

  В правой части страницы "Search" добавлена колонка "Recently Created", 
  в которой отображаются только что добавленные анкеты:
  
  .. image:: images/10/recently_created.jpg

--------------------   

**[HTPBB-237]** `Add "Tag Cloud" section at the right side of frontend pages`

  В правой части страницы "Search" добавлено
  "облако тэгов", в котором показаны наиболее популярные личности и категории каталога:
  
  .. image:: images/10/tag_cloud.jpg

--------------------   

**[HTPBB-238]** `Create page to configure tag parameters for the cloud`

  Параметры облака тэгов можно конфигурировать. Экран для этого доступен ченез меню
  DICTIONARIES, пункт "Tag Cloud Configuration". Здесь можно указать, какие из справочников 
  будут участвовать в облаке тэгов, количество элементов, которые будут добавлены в облако
  из данного справочника, а также "весовой коэффициент", который позволяет повысить "вес" 
  данного справочника в облаке.
  
  .. image:: images/10/tag_cloud_config.jpg
  
--------------------   

| **[HTPBB-242]** `Add "Rate" field in Persons UI table for ROLE_DICTIONARY_MANAGER`
| **[HTPBB-243]** `Add server support for "rate" field in profile_statistics table`

  В списке анкет добавлена колонка "Rate", позволяющая вводить вручную
  "весовой коэффициент" популярности анкеты, на который будет домножаться 
  автоматически рассчитанный коэффициент популярности, учитываемый в "облаке тэгов".
  
  .. image:: images/10/person_rates.jpg
  
--------------------   

**[HTPBB-230]** `Add gray hints in input boxes on Search page`

  На странице "Search" в полях расширенного поиска добавлены 
  подсказки о возможных значениях:
  
  .. image:: images/10/search_hints.jpg
  
--------------------   

**[HTPBB-232]** `Create validation rule to verify all dates in profile to be in "birth-death" interval`

  Для редактирования анкеты добавлена проверка, чтобы введенные даты лежали в интервале
  между датами рождения и смерти.

--------------------   

**[HTPBB-249]** `B.C. dates should be possible in profiles`

  В анкетах добавлена возможность вводить даты до нашей эры: 

  .. image:: images/10/bc_dates.jpg
  
--------------------   

**[HTPBB-247]** `Add "Category" column with filter to appropriate dictionary tables in "Dictionary" menu`

  В таблицы справочников добавлена колонка, позволяющая
  отсортировать элементы определенной категории:
  
  .. image:: images/10/filter_dict_category.jpg
  
--------------------   

**[HTPBB-253]** `Hide tabs with no data for profile in "View" mode`

  Пустые странички анкеты прячутся в режиме просмотра: 
  
  .. image:: images/10/filter_dict_category.jpg
  
--------------------   

**[HTPBB-252]** `Additional filters on "Persons" page to find profiles with empty fields`

  Справа на списке анкет добавлен фильтр, позволяющий выделить анкеты,
  в которых не заполнены те или иные поля. Если фильтр выключен, он будет находиться 
  в сложенном состоянии, если включен - в раскрытом. Для того, чтобы применить 
  фильтр, нужно поставить галочки напротив интересующих полей 
  и нажать "Apply":
  
  .. image:: images/10/empty_fields_filter.jpg
  
--------------------   

**[HTPBB-258]** `Improve quality of thumbnail images`

  Улучшено качество уменьшенных изображений для анкет.


