# Пояснительная записка к проекту Retro Racer
_____
## Структура проекта:

**Проект разделен на 6 разделов**:

1. **data**
   
    В папке **data** хранятся все данные, используемые в проекте (картинки для заднего фона, звуки)

   Папка **data** разделена на 2 раздела:
   - **images**. В этой папке хранятся изображения машин, задних фонов, препятствий
      * *car.png* - изображение машины
      * *forest.png* - изображение леса - заднего фона
      * *hole.png* - изображение ямы - препятствия
      * *road.png* - изоюражение дороги
   - **sounds**. В этой папке хранятся звуки двигателя, покупки и тд
___
2. **src**
   
    В папке **src** находится весь исходный код, используемый в проекте.

   Папка **src** содержит такие файлы, как:
   * ***car.py*** - файл, реализующий класс машины пользователя. 
     
     Методы класса:
     - **init** - инициализация
     - **update** - обновление координат машины после определенных событий (нажатий на стрелки клавиатуры)
     - **draw** - отрисовка машины на дороге
   
   * ***colors.py*** - файл, в котором находятся цвета в формате RGB для импорта в другие, чтобы не прописывать их в каждом файле
  
   * ***forest.py*** - файл, реализующий скроллинг заднего фона - леса
     
     Методы класса:
     - **init** - инициализация
     - **update** - обновление координат изображения леса (y-игрик не превышал допустимый y-игрик окна)
     - **draw** - отрисовка фона
  
   * ***game.py*** - файл, реализующий класс самой игры.
     Методы класса:
     - **init** - инициализация
     - **game_loop** - сам игровой цикл -> создаются экземпляры машины, дороги, ямы и заднего фона -> затем идет отслеживание событий -> затем прорисовка экземпляров в опреленном порядке
  
   * ***hole.py*** - файл, реализующий скроллинг ям
     Методы класса:
     - **init** - инициализация
     - **update** - обновление координат изображения ям (y-игрик не превышал допустимый y-игрик окна)
     - **draw** - отрисовка ям
  
   * ***main_menu.py*** - файл, реализующий главное меню. 
     
     Главное меню состоит из 4 разделов:
     * *Играть* - здесь пользователь может играть против машин-препятствий, собирать бонусы, избегать ям и зарабатывать очки, чтобы подниматься в топ таблицы лидеров
     * *Гараж* - здесь пользователь может выбирать, покупать и менять машину
     * *Настройки* - здесь пользователь может менять громкость звуков игры
     * *Таблица лидеров* - здесь пользователь может просматривать лидеров по очкам
     
     Функции:
     - **draw_button** - вспомогательная функция отрисовки кнопки
     - **draw_text** - вспомогательная функция отрисовки текста
     - **main_menu** - функция, реализующая само главное меню, отрисовывающая все кнопки и отслеживающая действия пользователя через перебор событий
  
   * ***road.py*** - файл, реализующий скроллинг дороги - самой важной части игры
     Методы класса:
     - **init** - инициализация
     - **update** - обновление координат изображения дороги (y-игрик не превышал допустимый y-игрик окна)
     - **draw** - отрисовка дороги

   * ***garage.py*** - файл, реализующий окно гаража - места покупки и прокачки своих машин.
     В файле содержатся такие классы как:
       - class Product - *класс, реализующий саму машину, которую возможно купить/улучшить*
         Методы класса:
         - init - инициализация
       - class Shop - *класс, реализующий сам магазин со всеми машинами в нем*
         Методы класса:
         - init - инициализация
         - draw_shop - отрисовка всего гаража
         - buy_car - покупка машины
         - draw_money - отрисовка баланса
         - main - главный цикл, совмещающий методы в единое целое
   * ***register.py*** - файл, реализующий класс регистрации
     Методы класса:
     - init - инициализация
     - handle_events - обработка событий (ввода текста, нажатия кнопок и корректности ввода)
     - draw - отрисовка всего + добавление нового пользователя в базу данных
     - main_loop - метод-цикл, объединяющий все методы в единое целое
   * ***login.py*** - файл, реалищующий окно выбора (войти/регистрация)
     Методы класса:
     - init - инициализация
     - draw_button/draw_text - вспомогательные функции отрисовки кнопки/текста
     - main_loop - главный цикл
_______
3. **.gitignore** - самый обычный гитигнор файл
_______
4. **DESCRIPTION.md** - описание идеи и процессов проекта в разрешении *.md*
_______
5. **requirements.txt** - здесь хранятся библиотеки, которые так или иначе затрагиваются в проекте
_______
6. **TZ.md** - техническое задание проекта в .md формате
