# ------------------------------------ RU_HTML- контент ------------------------------------
# Пример HTML-контента с локализацией
ru_html_content = r"""
<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Документация - Child PC Guard</title>
        
        <style>
            .important, .admin-warning {
                color: red;
            }
        </style>
    </head>

    <body>
            <h1>Добро пожаловать в программу Child PC Guard</h1>
            
            <p class="important">ВАЖНО!</p>

            <p>
                Программа всегда должна запускаться от имени администратора.<br> 
                Если этого не сделать, то некоторые функции попросту не будут работать.<br> 
                Поэтому всегда помните об этом как о первом правиле.<br>
            </p>
            
            <h2>Итак, что может эта программа?</h2>
            <p class="admin-warning">
                Она создана для контроля времени, сколько ваш ребенок проведет сегодня или завтра за компьютером.<br>
                Все просто на самом деле. Вы выбираете время в часах из списка и нажимаете "Запуск".<br>
                Включается таймер, когда таймер закончит свою работу, ПК будет заблокирован.<br>
                То есть доступ для вашего ребенка будет ограничен.<br>
                Только вы, имея пароль к программе, сможете снова дать доступ на определенное время.<br>
            </p>
            
            <h2>Правила использования программы</h2>
            <ul>
                <li><h3>1 Правило.</h3></li>
                    <p>
                        На ПК должно быть две учетные записи. Если будет одна, программа не запустится.<br> 
                        Это сделано в целях безопасности, чтобы не заблокировать самого себя.<br> 
                        Вам нужно создать вторую учетную запись для того, чтобы программа могла её блокировать.<br> 
                        Первая учетная запись должна иметь права доступа администратора.<br> 
                        Вторая учетная запись также должна быть с правами администратора.<br>
                    </p>
                
                <br>
                <li><h3>2 Правило.</h3></li>
                    <p>
                        Запускать программу нужно в той учетной записи, которую нужно блокировать.<br> 
                        Назначьте время, запустите программу и оставьте её в свернутом виде.<br> 
                        Если программу закрыть, она перестанет отсчитывать время таймером.<br> 
                        То есть её нужно просто свернуть, чтобы она не мешала ребенку.<br> 
                        Конечно, не забудьте заблокировать интерфейс, чтобы у ребенка не было возможности закрыть или изменить что-то в настройках.<br>
                    </p>
                
                <br>
                <li><h3>3 Правило.</h3></li>
                    <p>
                        Если блокировка сработала, ребенок не сможет зайти в свою учетную запись, так как к ней не будет доступа.<br> 
                        Вам нужно сначала зайти в свою учетную запись (администратора), запустить программу и выбрать ярлык - "Разблокировать".<br> 
                        В окне будет показано, кто заблокирован. Вам нужно нажать кнопку "Разблокировать".<br>
                    </p>
                
                <br>
                <li><h3>4 Правило.</h3></li>
                    <p>После разблокировки нужно перейти снова в учетную запись ребенка и назначить время для блокировки ПК.</p>
                
                <br>
                <li><h3>5 Правило.</h3></li>
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
            
            <p>
                Писать по адресу - <b>gbo4.net@gmail.com</b><br>
                Мой ник в Telegram:" <b>@norovprog</b>
            </p>
    
    </body>
</html>"""
# ------------------------------------ UA_HTML- контент ------------------------------------
uk_html_content = r"""
<!DOCTYPE html>
<html lang="uk">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Документація - Child PC Guard</title>
        
        <style>
            .important, .admin-warning {
                color: red;
            }
        </style>
    </head>

    <body>
            <h1>Ласкаво просимо до програми Child PC Guard</h1>
            
            <p class="important">ВАЖЛИВО!</p>

            <p class="admin-warning">
                Програму завжди потрібно запускати від імені адміністратора. 
                Якщо цього не зробити, деякі функції просто не будуть працювати. 
                Тому завжди пам'ятайте про це як про перше правило.
            </p>
            
            <h2>Отже, що може ця програма?</h2>
            <p>
                Вона створена для контролю часу, скільки ваша дитина проведе сьогодні або завтра за комп'ютером.
                Все дуже просто. Ви обираєте час у годинах зі списку та натискаєте "Запуск". 
                Увімкнеться таймер, коли таймер завершить роботу, ПК буде заблоковано. 
                Тобто доступ для вашої дитини буде обмежено. 
                Тільки ви, маючи пароль до програми, зможете знову надати доступ на визначений час.
            </p>
            
            <h2>Правила використання програми</h2>
            <ul>
                <li><h3>1 Правило.</h3></li>
                    <p>
                        На ПК повинні бути два облікові записи. Якщо буде лише один, програма не запуститься. 
                        Це зроблено з міркувань безпеки, щоб не заблокувати себе самого. 
                        Вам потрібно створити другий обліковий запис для того, щоб програма могла його блокувати. 
                        Перший обліковий запис повинен мати права адміністратора. 
                        Другий обліковий запис також повинен мати права адміністратора.
                    </p>
                
                <br>
                <li><h3>2 Правило.</h3></li>
                    <p>
                        Запускати програму потрібно в тому обліковому записі, який потрібно блокувати. 
                        Встановіть час, запустіть програму і залиште її згорнутою. 
                        Якщо програму закрити, вона перестане відлічувати час таймером. 
                        Тобто її потрібно просто згорнути, щоб вона не заважала дитині. 
                        Звісно, не забудьте заблокувати інтерфейс, щоб у дитини не було можливості закрити або змінити щось у налаштуваннях.
                    </p>
                
                <br>
                <li><h3>3 Правило.</h3></li>
                    <p>
                        Якщо блокування спрацювало, дитина не зможе зайти до свого облікового запису, оскільки до нього не буде доступу. 
                        Вам потрібно спочатку зайти у свій обліковий запис (адміністратора), запустити програму і вибрати ярлик - "Розблокувати". 
                        У вікні буде показано, хто заблокований. Вам потрібно натиснути кнопку "Розблокувати".
                    </p>
                
                <br>
                <li><h3>4 Правило.</h3></li>
                    <p>Після розблокування потрібно знову перейти до облікового запису дитини і призначити час для блокування ПК.</p>
                
                <br>
                <li><h3>5 Правило.</h3></li>
                    <p>
                        З настанням нового дня обліковому запису завжди буде додаватися 2 години для роботи на ПК. 
                        Але якщо, наприклад, ви вирішите задати час для блокування, то додані години (2 години) будуть обнулені. 
                        Буде призначено лише той час, який ви вкажете.
                    </p>
                
            </ul>
            
            <p>
                Програма пам'ятає, скільки часу минуло, якщо раптом ПК буде вимкнено, коли таймер відлічує час. 
                Тобто якщо його ввімкнути і зайти до облікового запису дитини, програма автоматично сама запуститься і продовжить відлік залишеного часу.
            </p>
            
            <p>В цілому це все, що важливо знати. Решта кнопок у програмі ви зможете самі зрозуміти, як працюють.</p>            
            
            <p>
                І найцікавіше: програму не вийде просто закрити і все. 
                Якщо програму буде закрито, через деякий час вона запуститься знову. 
                Ви ж розумієте, що діти у наш час дуже кмітливі. 
                Я постарався це передбачити. Але якщо сильно захотіти, зрозуміло, її можна просто видалити.
            </p>
            
            <p>
                Я постарався передбачити багато чого, але реальних випробувань я не проводив. 
                Тому, якщо у вас будуть побажання або корисні пропозиції, я буду радий їх розглянути. 
                Тільки в бойових умовах буде зрозуміло, чого не вистачає або де можна покращити.
            </p>
            
            <p>
                Писати на адресу - <b>gbo4.net@gmail.com</b><br>
                Мій нік у Telegram: <b>@norovprog</b>
            </p>
    
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
            .important, .admin-warning {
                color: red;
            }
        </style>
    </head>

    <body>
            <h1>Welcome to the Child PC Guard program</h1>
            
            <p class="important">IMPORTANT!</p>

            <p class="admin-warning">
                The program must always be run as an administrator. 
                If this is not done, some features will simply not work. 
                So always keep this in mind as the first rule.
            </p>
            
            <h2>So, what can this program do?</h2>
            <p>
                It is designed to control the amount of time your child spends today or tomorrow on the computer.
                It's really simple. You select the time in hours from the list and click "Start". 
                The timer starts, and when the timer finishes, the PC will be locked. 
                This means that access for your child will be restricted. 
                Only you, having the program's password, will be able to grant access again for a certain period of time.
            </p>
            
            <h2>Program usage rules</h2>
            <ul>
                <li><h3>Rule 1.</h3></li>
                    <p>
                        The PC must have two user accounts. If there is only one, the program will not start. 
                        This is done for security purposes so that you do not lock yourself out. 
                        You need to create a second account for the program to be able to block it. 
                        The first account must have administrator rights. 
                        The second account must also have administrator rights.
                    </p>
                
                <br>
                <li><h3>Rule 2.</h3></li>
                    <p>
                        You need to run the program in the account that you want to block. 
                        Set the time, start the program, and leave it minimized. 
                        If the program is closed, it will stop counting the time with the timer. 
                        That is, it just needs to be minimized so that it doesn't interfere with the child. 
                        Of course, don't forget to lock the interface so that the child cannot close or change anything in the settings.
                    </p>
                
                <br>
                <li><h3>Rule 3.</h3></li>
                    <p>
                        If the lock is triggered, the child will not be able to log into their account as there will be no access. 
                        You will need to log into your account (administrator), run the program, and select the shortcut - "Unlock". 
                        The window will show who is locked. You need to click the "Unlock" button.
                    </p>
                
                <br>
                <li><h3>Rule 4.</h3></li>
                    <p>After unlocking, you need to switch back to the child's account and set the time for PC blocking.</p>
                
                <br>
                <li><h3>Rule 5.</h3></li>
                    <p>
                        At the start of a new day, 2 hours will always be added for the account to use the PC. 
                        However, if you decide to set a blocking time, the added hours (2 hours) will be reset. 
                        Only the time you set will be applied.
                    </p>
                
            </ul>
            
            <p>
                The program remembers how much time has passed if the PC is suddenly turned off while the timer is counting. 
                That is, if you turn it back on and log into the child's account, the program will automatically restart and continue counting the remaining time.
            </p>
            
            <p>In general, this is all you need to know. You can figure out the other buttons in the program on your own.</p>            
            
            <p>
                And the most interesting part: you can't just close the program and that's it. 
                If the program is closed, after some time it will start again. 
                You understand that kids these days are very clever. 
                I tried to foresee this. But if you really want to, of course, you can simply delete it.
            </p>
            
            <p>
                I tried to anticipate a lot, but I have not conducted real tests. 
                So, if you have any wishes or useful suggestions, I would be happy to consider them. 
                Only in real-life conditions will it become clear what is missing or where improvements can be made.
            </p>
            
            <p>
                Write to this address - <b>gbo4.net@gmail.com</b><br>
                My Telegram nickname: <b>@norovprog</b>
            </p>
    
    </body>
</html>
"""
