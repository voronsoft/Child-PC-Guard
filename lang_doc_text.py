# ------------------------------------ RU_HTML- контент ------------------------------------
ru_html_content = r"""
<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Документация - Child PC Guard</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }
            h1 {
                color: #2c3e50;
            }
            h2 {
                color: #2980b9;
            }
            p, li {
                margin-bottom: 10px;
            }
            .lang-section {
                margin-bottom: 30px;
            }
            ul {
                list-style-type: decimal;
                padding-left: 20px;
            }

            .important, .admin-warning {
                color: red;
            }
            .toc {
                margin-bottom: 20px;
            }
            .toc a {
                text-decoration: none;
                color: #2980b9;
            }
        </style>
    </head>

    <body>
        <div class="lang-section">
            <h1>Добро пожаловать в Child PC Guard</h1>

            <div class="toc">
                <h2>Содержание:</h2>
                <ul>
                    <li><a href="#program-features_ru">Что может эта программа?</a></li>
                    <li><a href="#usage-rules_ru">Правила использования программы</a></li>
                    <li><a href="#telegram-setup_ru">Настройка оповещения через бот Телеграм</a></li>
                    <li><a href="#contacts_ru">Контакты</a></li>
                </ul>
            </div>

            <p class="important">ВАЖНО!</p>

            <p class="admin-warning">
                Программа всегда должна запускаться от имени администратора.<br> 
                Если этого не сделать, то некоторые функции попросту не будут работать.<br> 
                Поэтому всегда помните об этом как о первом правиле.<br>
            </p>

            <h2 id="program-features_ru">Итак, что может эта программа?</h2>
            <p>
                Она создана для контроля времени, сколько ваш ребенок проведет сегодня или завтра за компьютером.<br>
                Все просто на самом деле. Вы выбираете время в часах из списка и нажимаете "Запуск".<br>
                Включается таймер, когда таймер закончит свою работу, ПК будет заблокирован.<br>
                То есть доступ для вашего ребенка будет ограничен.<br>
                Только вы, имея пароль к программе, сможете снова дать доступ на определенное время.<br>
            </p>

            <h2 id="usage-rules_ru">Правила использования программы</h2>
            <ul>
                <h3>1 Правило.</h3>
                    <p>
                        На ПК должно быть две учетные записи. Если будет одна, программа не запустится.<br> 
                        Это сделано в целях безопасности, чтобы не заблокировать самого себя.<br> 
                        Вам нужно создать вторую учетную запись для того, чтобы программа могла её блокировать.<br> 
                        Первая учетная запись должна иметь права доступа администратора.<br> 
                        Вторая учетная запись также должна быть с правами администратора.<br>
                    </p>

                <br>
                <h3>2 Правило.</h3>
                    <p>
                        Запускать программу нужно в той учетной записи, которую нужно блокировать.<br> 
                        Назначьте время, запустите программу и оставьте её в свернутом виде.<br> 
                        Если программу закрыть, она перестанет отсчитывать время таймером.<br> 
                        То есть её нужно просто свернуть, чтобы она не мешала ребенку.<br> 
                        Конечно, не забудьте заблокировать интерфейс, чтобы у ребенка не было возможности закрыть или изменить что-то в настройках.<br>
                    </p>

                <br>
                <h3>3 Правило.</h3>
                    <p>
                        Если блокировка сработала, ребенок не сможет зайти в свою учетную запись, так как к ней не будет доступа.<br> 
                        Вам нужно сначала зайти в свою учетную запись (администратора), запустить программу и выбрать ярлык - "Разблокировать".<br> 
                        В окне будет показано, кто заблокирован. Вам нужно нажать кнопку "Разблокировать".<br>
                    </p>

                <br>
                <h3>4 Правило.</h3>
                    <p>После разблокировки нужно перейти снова в учетную запись ребенка и назначить время для блокировки ПК.</p>

                <br>
                <h3>5 Правило.</h3>
                    <p>
                        С наступлением нового дня учетной записи будет всегда добавляться 2 часа для работы на ПК.<br> 
                        Но если, допустим, вы решили задать время для блокировки, то добавленные часы (2 часа) будут обнулены.<br> 
                        Будет назначено только то время, которое вы назначите.<br>
                    </p>
            </ul>
            <hr><br>
            <p>
                Программа помнит, сколько времени прошло, если вдруг ПК будет выключен, когда таймер считает время.<br> 
                То есть если его включить и зайти в учетную запись ребенка, программа автоматически сама запустится и продолжит отсчет оставшегося времени.<br>
            </p>

            <p>В целом это всё, что важно знать. Остальные кнопочки в программе вы можете сами понять, как работают.</p>            

            <p>
                И самое интересное: программу не получится просто закрыть и всё.<br> 
                Если программа будет закрыта, то через некоторое время она запустится снова.<br> 
                Вы же понимаете, что детки в наше время очень умненькие.<br> 
                Я постарался это предусмотреть. Но если сильно захотеть, понятное дело, её можно просто удалить.<br>
            </p>

            <p>
                Я постарался многое предусмотреть, но реальных испытаний я не делал.<br> 
                Поэтому, если у вас будут пожелания или дельные предложения, я буду рад их рассмотреть.<br> 
                Только в боевых условиях будет понятно, что не хватает или где можно улучшить.<br>
            </p>

            <hr>

            <h2 id="telegram-setup_ru">Настройка оповещения через бот Телеграм</h2>
            <p>Вы можете подключить оповещение через Телеграм. Как это сделать?</p>
            <ul>
                <li>Запустите программу Child PC Guard</li>
                <li>На телефоне запустите приложение Телеграм</li>
                <li>В строке поиска Телеграм введите имя бота для вашей программы: <b>@ChildPCGuard_bot</b></li>
                <li>Найдите бота и начните с ним диалог</li>
                <li>На странице диалога с ботом вы увидите инструкцию для начала работы. 
                Нажмите кнопку <strong>START</strong> или введите команду <strong>/start</strong>. 
                Бот отправит вам сообщение с вашим <b>chat_id</b>. 
                Запомните его, этот номер нужно ввести в программе Child PC Guard.</li>
                <li>На главном экране программы Child PC Guard найдите кнопку <b>Оповещение</b> и войдите в этот раздел для настройки</li>
                <li>В окне настройки бота следуйте дальнейшим инструкциям</li>
                <li>В поле введите ваш <b>chat_id</b>, который вам прислал бот в Телеграме, без пробелов</li>
                <li>Подтвердите настройки, нажав ОК</li>
            </ul>
            <p>
                Бот получит ваш номер, чтобы понимать, кому отсылать сообщения о работе Child PC Guard.
                А также принимать команды от вас.
                Команды привязаны к кнопкам меню Бота.
            </p>
            <p>Далее все очень просто.</p>
            <p>
                Вы запустили контроль времени в самой программе, бот, зная ваш номер chat_id, будет посылать сообщения о состоянии работы приложения.<br>   
                Допустим:<br>
                - Программа запущена.<br>
                - Программа была кем-то закрыта.<br>
                - Кто-то ввел неправильный пароль.<br>
            </p>
            <p>
                Также вы можете удаленно управлять через Бот некоторыми функциями Child PC Guard:
                <li>Узнать статус состояния программы.<br></li>
                <li>Вывести на экран ПК какое-либо сообщение, написав текст сообщения боту.<br></li>
                <li>Выключить компьютер, но без блокировки пользователя.<br></li>
                <li>Заблокировать доступ к ПК в независимости от того работает таймер отсчета времени или нет.<br></li>
            </p>
            <p id="contacts_ru" class="admin-warning">
                Писать по адресу - <b>gbo4.net@gmail.com</b><br>
                Мой ник в Telegram:" <b>@norovprog</b>
            </p>
            <p>
                Возможно какую то функци.я не добавил но это можно реализовать в других версиях программы.<br>

                Да ВАЖНО понимать, что Бот Телеграмм будет работать только тогда когда:<br>
                1 Программа Child PC Guard, включена на ПК.<br>
                2 Ваш ПК подкоючен к интернету ))<br>
                
                И так это все что касается настройки оповещения работы программы с помощью Бота телеграмм.<br>
            </p>
        </div>
    </body>
</html>
"""

# ------------------------------------ UA_HTML- контент ------------------------------------
uk_html_content = r"""
<!DOCTYPE html>
<html lang="uk">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Документація - Child PC Guard</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }
            h1 {
                color: #2c3e50;
            }
            h2 {
                color: #2980b9;
            }
            p, li {
                margin-bottom: 10px;
            }
            .lang-section {
                margin-bottom: 30px;
            }
            ul {
                list-style-type: decimal;
                padding-left: 20px;
            }

            .important, .admin-warning {
                color: red;
            }
            .toc {
                margin-bottom: 20px;
            }
            .toc a {
                text-decoration: none;
                color: #2980b9;
            }
        </style>
    </head>

    <body>
        <div class="lang-section">
            <h1>Ласкаво просимо до Child PC Guard</h1>

            <div class="toc">
                <h2>Зміст:</h2>
                <ul>
                    <li><a href="#program-features_uk">Що може ця програма?</a></li>
                    <li><a href="#usage-rules_uk">Правила використання програми</a></li>
                    <li><a href="#telegram-setup_uk">Налаштування сповіщення через бот Телеграм</a></li>
                    <li><a href="#contacts_uk">Контакти</a></li>
                </ul>
            </div>

            <p class="important">ВАЖЛИВО!</p>

            <p class="admin-warning">
                Програма завжди повинна запускатися від імені адміністратора.<br> 
                Якщо цього не зробити, то деякі функції просто не будуть працювати.<br> 
                Тому завжди пам'ятайте про це як про перше правило.<br>
            </p>

            <h2 id="program-features_uk">Отже, що може ця програма?</h2>
            <p>
                Вона створена для контролю часу, скільки ваша дитина проведе сьогодні або завтра за комп'ютером.<br>
                Все просто насправді. Ви вибираєте час в годинах зі списку і натискаєте "Запуск".<br>
                Включається таймер, коли таймер закінчить свою роботу, ПК буде заблоковано.<br>
                Тобто доступ для вашої дитини буде обмежено.<br>
                Тільки ви, маючи пароль до програми, зможете знову дати доступ на певний час.<br>
            </p>

            <h2 id="usage-rules_uk">Правила використання програми</h2>
            <ul>
                <h3>1 Правило.</h3>
                    <p>
                        На ПК повинно бути дві облікові записи. Якщо буде одна, програма не запуститься.<br> 
                        Це зроблено в цілях безпеки, щоб не заблокувати самого себе.<br> 
                        Вам потрібно створити другу облікову запис, щоб програма могла її блокувати.<br> 
                        Перша облікова запис повинна мати права доступу адміністратора.<br> 
                        Друга облікова запис також повинна бути з правами адміністратора.<br>
                    </p>

                <br>
                <h3>2 Правило.</h3>
                    <p>
                        Запускати програму потрібно в тій обліковій записі, яку потрібно блокувати.<br> 
                        Призначте час, запустіть програму і залиште її в згорнутому вигляді.<br> 
                        Якщо програму закрити, вона перестане відстежувати час таймером.<br> 
                        Тобто її потрібно просто згорнути, щоб вона не заважала дитині.<br> 
                        Звичайно, не забудьте заблокувати інтерфейс, щоб у дитини не було можливості закрити або змінити щось у налаштуваннях.<br>
                    </p>

                <br>
                <h3>3 Правило.</h3>
                    <p>
                        Якщо блокування спрацювало, дитина не зможе зайти у свою облікову запис, так як до неї не буде доступу.<br> 
                        Вам потрібно спочатку зайти у свою облікову запис (адміністратора), запустити програму і вибрати ярлик - "Розблокувати".<br> 
                        У вікні буде показано, хто заблокований. Вам потрібно натиснути кнопку "Розблокувати".<br>
                    </p>

                <br>
                <h3>4 Правило.</h3>
                    <p>Після розблокування потрібно перейти знову в облікову запис дитини і призначити час для блокування ПК.</p>

                <br>
                <h3>5 Правило.</h3>
                    <p>
                        З настанням нового дня обліковій запису завжди буде додаватися 2 години для роботи на ПК.<br> 
                        Але якщо, припустимо, ви вирішили задати час для блокування, то додані години (2 години) будуть обнулені.<br> 
                        Буде призначено тільки те час, яке ви призначите.<br>
                    </p>
            </ul>
            <hr><br>
            <p>
                Програма пам'ятає, скільки часу пройшло, якщо раптом ПК буде вимкнено, коли таймер відраховує час.<br> 
                Тобто якщо його включити і зайти в облікову запис дитини, програма автоматично сама запуститься і продовжить відлік залишеного часу.<br>
            </p>

            <p>В цілому це все, що важливо знати. Інші кнопочки в програмі ви можете самі зрозуміти, як працюють.</p>            

            <p>
                І найцікавіше: програму не вдасться просто закрити і все.<br> 
                Якщо програма буде закрита, то через деякий час вона запуститься знову.<br> 
                Ви ж розумієте, що діти в наш час дуже розумні.<br> 
                Я постарався це передбачити. Але якщо сильно захотіти, зрозуміло, її можна просто видалити.<br>
            </p>

            <p>
                Я постарався багато що передбачити, але реальних випробувань я не проводив.<br> 
                Тому, якщо у вас будуть побажання або слушні пропозиції, я буду радий їх розглянути.<br> 
                Тільки в бойових умовах буде зрозуміло, що не вистачає або де можна покращити.<br>
            </p>

            <hr>

            <h2 id="telegram-setup_uk">Налаштування сповіщення через бот Телеграм</h2>
            <p>Ви можете підключити сповіщення через Телеграм. Як це зробити?</p>
            <ul>
                <li>Запустіть програму Child PC Guard</li>
                <li>На телефоні запустіть додаток Телеграм</li>
                <li>У рядку пошуку Телеграм введіть ім'я бота для вашої програми: <b>@ChildPCGuard_bot</b></li>
                <li>Знайдіть бота і почніть з ним діалог</li>
                <li>На сторінці діалогу з ботом ви побачите інструкцію для початку роботи. 
                Натисніть кнопку <strong>START</strong> або введіть команду <strong>/start</strong>. 
                Бот надішле вам повідомлення з вашим <b>chat_id</b>. 
                Запам'ятайте його, цей номер потрібно ввести в програмі Child PC Guard.</li>
                <li>На головному екрані програми Child PC Guard знайдіть кнопку <b>Сповіщення</b> і увійдіть у цей розділ для налаштування</li>
                <li>У вікні налаштування бота дотримуйтесь подальших інструкцій</li>
                <li>В полі введіть ваш <b>chat_id</b>, який вам прислав бот у Телеграмі, без пробілів</li>
                <li>Підтверджте налаштування, натиснувши ОК</li>
            </ul>
            <p>
                Бот отримає ваш номер, щоб розуміти, кому надсилати повідомлення про роботу Child PC Guard.
                А також приймати команди від вас.
                Команди прив'язані до кнопок меню Бота.
            </p>
            <p>Далі все дуже просто.</p>
            <p>
                Ви запустили контроль часу в самій програмі, бот, знаючи ваш номер chat_id, буде надсилати повідомлення про стан роботи програми.<br>
                Припустимо:<br>
                - Програма запущена.<br>
                - Програма була кимось закрита.<br>
                - Хтось ввів неправильний пароль.<br>
            </p>
            <p>
                Також ви можете віддалено керувати через Бота деякими функціями Child PC Guard:
                <li>Дізнатися статус стану програми.<br></li>
                <li>Вивести на екран ПК якесь повідомлення, написавши текст повідомлення боту.<br></li>
                <li>Вимкнути комп'ютер, але без блокування користувача.<br></li>
                <li>Заблокувати доступ до ПК незалежно від того, працює таймер відліку часу чи ні.<br></li>
            </p>
            <p>
                Можливо, якусь функцію я не додав, але це можна реалізувати в інших версіях програми.<br>
                
                Так ВАЖЛИВО розуміти, що Бот Телеграм буде працювати тільки тоді, коли:<br>
                1. Програма Child PC Guard увімкнена на ПК.<br>
                2. Ваш ПК підключений до Інтернету ))<br>
                
                І так, це все, що стосується налаштування сповіщення про роботу програми за допомогою Бота Телеграм.<br>
            </p>
            <p id="contacts_uk" class="admin-warning">
                Писати за адресою - <b>gbo4.net@gmail.com</b><br>
                Мій нік у Telegram: "<b>@norovprog</b>"
            </p>

        </div>
    </body>
</html>
"""

# ------------------------------------ EN_HTML- контент ------------------------------------
en_html_content = r"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Documentation - Child PC Guard</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }
            h1 {
                color: #2c3e50;
            }
            h2 {
                color: #2980b9;
            }
            p, li {
                margin-bottom: 10px;
            }
            .lang-section {
                margin-bottom: 30px;
            }
            ul {
                list-style-type: decimal;
                padding-left: 20px;
            }

            .important, .admin-warning {
                color: red;
            }
            .toc {
                margin-bottom: 20px;
            }
            .toc a {
                text-decoration: none;
                color: #2980b9;
            }
        </style>
    </head>

    <body>
        <div class="lang-section">
            <h1>Welcome to Child PC Guard</h1>

            <div class="toc">
                <h2>Contents:</h2>
                <ul>
                    <li><a href="#program-features_en">What can this program do?</a></li>
                    <li><a href="#usage-rules_en">Rules for using the program</a></li>
                    <li><a href="#telegram-setup_en">Setting up notifications via Telegram bot</a></li>
                    <li><a href="#contacts_en">Contacts</a></li>
                </ul>
            </div>

            <p class="important">IMPORTANT!</p>

            <p class="admin-warning">
                The program must always be run as an administrator.<br>
                If this is not done, some functions simply will not work.<br>
                Therefore, always remember this as the first rule.<br>
            </p>

            <h2 id="program-features_en">So, what can this program do?</h2>
            <p>
                It is designed to control how much time your child spends on the computer today or tomorrow.<br>
                It's actually quite simple. You choose the time in hours from the list and click "Start".<br>
                A timer starts, and when the timer finishes, the PC will be locked.<br>
                That is, access for your child will be restricted.<br>
                Only you, having the password to the program, can grant access again for a certain time.<br>
            </p>

            <h2 id="usage-rules_en">Rules for using the program</h2>
            <ul>
                <h3>1st Rule.</h3>
                    <p>
                        There must be two user accounts on the PC. If there is only one, the program will not start.<br>
                        This is done for safety reasons, so you don't lock yourself out.<br>
                        You need to create a second user account for the program to be able to block it.<br>
                        The first user account should have administrator access.<br>
                        The second account should also have administrator rights.<br>
                    </p>

                <br>
                <h3>2nd Rule.</h3>
                    <p>
                        The program should be launched under the account that needs to be blocked.<br>
                        Set the time, start the program, and minimize it.<br>
                        If you close the program, it will stop counting down the timer.<br>
                        In other words, you just need to minimize it so that it doesn’t disturb the child.<br>
                        Of course, don’t forget to block the interface so that the child doesn’t have the opportunity to close or change anything in the settings.<br>
                    </p>

                <br>
                <h3>3rd Rule.</h3>
                    <p>
                        If the block is activated, the child will not be able to log into their account as it will be inaccessible.<br>
                        You need to first log into your own account (administrator), start the program, and select the shortcut - "Unlock".<br>
                        The window will show who is blocked. You need to press the "Unlock" button.<br>
                    </p>

                <br>
                <h3>4th Rule.</h3>
                    <p>After unlocking, you need to go back to the child's account and set the time for blocking the PC.</p>

                <br>
                <h3>5th Rule.</h3>
                    <p>
                        With the arrival of a new day, the account will always receive 2 hours of working time on the PC.<br>
                        But if, for example, you decided to set a time for blocking, the added hours (2 hours) will be reset.<br>
                        Only the time you designate will be assigned.<br>
                    </p>
            </ul>
            <hr><br>
            <p>
                The program remembers how much time has passed if the PC is turned off while the timer is counting.<br>
                So if it is turned back on and you log into the child's account, the program will automatically start and continue counting down the remaining time.<br>
            </p>

            <p>This is basically all you need to know. You can understand how the other buttons in the program work yourself.</p>

            <p>
                And the most interesting part: the program cannot simply be closed and that's it.<br>
                If the program is closed, it will start again after a while.<br>
                You understand that kids these days are very smart.<br>
                I tried to anticipate this. But if one really wants, of course, it can be simply uninstalled.<br>
            </p>

            <p>
                I tried to take many things into account, but I haven’t done real testing.<br>
                Therefore, if you have suggestions or constructive proposals, I would be happy to consider them.<br>
                Only in real-world conditions will it be clear what is missing or where improvements can be made.<br>
            </p>

            <hr>

            <h2 id="telegram-setup_en">Setting up notifications via Telegram bot</h2>
            <p>You can connect notifications through Telegram. How to do this?</p>
            <ul>
                <li>Run the Child PC Guard program</li>
                <li>On your phone, open the Telegram app</li>
                <li>In the Telegram search bar, type the bot name for your program: <b>@ChildPCGuard_bot</b></li>
                <li>Find the bot and start a chat with it</li>
                <li>On the chat page with the bot, you will see instructions to get started. 
                Click the <strong>START</strong> button or enter the command <strong>/start</strong>. 
                The bot will send you a message with your <b>chat_id</b>. 
                Remember it; this number needs to be entered in the Child PC Guard program.</li>
                <li>On the main screen of the Child PC Guard program, find the <b>Notification</b> button and enter this section for setup</li>
                <li>In the bot setup window, follow the further instructions</li>
                <li>In the field, enter your <b>chat_id</b> that the bot sent you in Telegram, without spaces</li>
                <li>Confirm the settings by clicking OK</li>
            </ul>
            <p>
                The bot will receive your number to know whom to send messages about the operation of Child PC Guard.
                And also to receive commands from you.
                The commands are tied to the buttons in the Bot's menu.
            </p>
            <p>After that, everything is very simple.</p>
            <p>
                You started time control in the program itself, and the bot, knowing your chat_id, will send messages about the application's status.<br>   
                For example:<br>
                - The program is running.<br>
                - The program has been closed by someone.<br>
                - Someone entered the wrong password.<br>
            </p>
            <p>
                You can also remotely control some functions of Child PC Guard through the Bot:
                <li>Know the status of the program.<br></li>
                <li>Display any message on the PC screen by writing the message text to the bot.<br></li>
                <li>Shut down the computer without locking the user.<br></li>
                <li>Block access to the PC regardless of whether the timer is running or not.<br></li>
            </p>
            <p>
                Perhaps I did not add some function, but this can be implemented in other versions of the program.<br>

                Yes, it is IMPORTANT to understand that the Telegram Bot will work only when:<br>
                1. The Child PC Guard program is running on the PC.<br>
                2. Your PC is connected to the internet ))<br>

                And so this is all regarding the setup of notifications about the program's operation using the Telegram Bot.<br>
            </p>
            <p id="contacts_en" class="admin-warning">
                Write to the address - <b>gbo4.net@gmail.com</b><br>
                My nickname on Telegram: "<b>@norovprog</b>
            </p>
        </div>
    </body>
</html>
"""


