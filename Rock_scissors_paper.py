import random
import time

#Массивы с выбором, по ним проверяется, что выбрал игрок
main_arr = ['1', 'играть', '2', 'правила', '3', 'настройки', '4', 'выйти']
game_arr = ['1', 'камень', '2', 'ножницы', '3', 'бумага', '4', 'обвинить', '5', 'логи', '6', 'сдаться']
rules_arr =['1', 'базовые', '2', 'обман', '3', 'назад']
sett_arr = ['1', 'баланс', '2', 'частота', '3', 'количество', '4', 'назад']
#Инициализация всех переменных на дефолтные значения
tact_arr = [1] * 7; step_arr = [-2] * 30; tact_arr[0] = 50; games_count = 0; best_balance = 0; best_step = 0; logs_amount = 5; st_balance = 40; bot_blame = 0; bot_lose = 0; bot_win = 0; rocks = 0; papers = 0; scissors = 0; tactic = 0; last_b_mv = 1; last = 1; last_p_mv = 1; last_res = 0; b_b_mp = 2

#Функция для проверки, можно ли перевести строку в инт
def is_int(n):
    try:
        n = int(n)
        return True
    except ValueError:
        return False

#Функция для очищения всех значений после окончания игры
def clear():
    tact_arr = [1] * 7
    step_arr = [-2] * 30
    tact_arr[0] = 50
    bot_blame = 0; bot_lose = 0; bot_win = 0; rocks = 0; papers = 0; scissors = 0; tactic = 0; last_b_mv = 1; last = 1; last_p_mv = 1; last_res = 0

#Функция вывода, дабы вывод был более удобен и все версии в одной функции
def out(text = "", n = 0, t = 44):    
    #Вывод с t новыми строками, текстом и запросом
    if n == 0:
        print("\n" * t + text, "\n\n>", end = '')
        return input().lower()
    #Вывод с новыми строками, текстом
    elif n == 1:
        print("\n" * t + text, end = '')
    #Вывод текста
    elif n == 2:
        print(text, end = '')
    #Вывод без новых строк с запросом
    elif n == 3:
        print(text + "\n\n>", end = '')
        return input().lower()


#Функция определения текущей тактики бота
def tactics():
    #Глобализация необходимых переменных
    global tactic, tact_arr
    #Если бот жульничает, не меняем тактику
    if bot_blame == 1:
        return
    else:
        #Если что-то < 0, исправляем
        for i in range(7):
            if (tact_arr[i] <= 0):
                tact_arr[i] = 1
        #+1 к тактике рандома, чтобы при прочих равных он чаще выбирал ее
        tact_arr[0] += 1
        #Если бот не победил в последний раз, он больше захочет жульничать
        if(last_res != 1):
                tact_arr[1] += b_b_mp * 2
        #Если бот больше проигрывал, чем выигрывал
        if (bot_lose > bot_win):
            #обновляем желание бота сжульничать
            #и также тактику игры до победного
            tact_arr[5] += bot_lose - bot_win
            tact_arr[1] += b_b_mp * ((bot_lose - bot_win - 1) + 1)
        #Если какого-то элемента больше чем двух остальных, добавляем + к
        #Тактике, когда выбирается только противоположный
        #И + к тактике мимикрии
        if 0 < 2 * rocks - papers - scissors:
            tact_arr[2] += rocks - papers; tact_arr[2] += rocks - scissors;
            tact_arr[6] += 2
            #Если последний ход игрока - этот элемент, добавляем еще больше
            if (last_p_mv == 1):
                tact_arr[2] += 10
            else:
                tact_arr[2] -= 10
        #Тоже самое что и в прошлом if-е
        if 0 < 2 * papers - rocks - scissors:
            tact_arr[3] += papers - rocks; tact_arr[2] += papers - scissors;
            tact_arr[6] += 2
            if (last_p_mv == 3):
                tact_arr[3] += 10
            else:
                tact_arr[3] -= 10
                
        #Тоже самое, что и в прощлом if-е
        if 0 < 2 * scissors - rocks - scissors:
            tact_arr[4] += scissors - rocks; tact_arr[2] += scissors - papers;
            tact_arr[6] += 2
            if (last_p_mv == 2):
                tact_arr[4] += 10
            else:
                tact_arr[4] -= 10
        #Бот выбирает, какой тактики ему придерживаться
        #Суммируются веса всех тактик
        #И ищется отрезок на который выпала тактика
        
        res = random.randint(1, sum(tact_arr))
        for i in range(0, 7):
            res -= tact_arr[i]
            if res <= 0:
                tactic = i
                break

#Функция хода бота
def bot_move(p_move, step):
    global bot_blame, balance, tact_arr, last_res, bot_lose, bot_win, rocks, scissors, papers, last_p_mv, step_arr
    #Выбираем из списка тактик нашу текущую и играем соответственно ей
    #Тактика - рандом, выбирается рандомный элемент
    if tactic == 0:
        b_mv = random.randint(1, 3)
    #Тактика - жульничество, бот всегда выигрывает
    elif tactic == 1:
        bot_blame = 1
        b_mv = p_move - 1
        if (b_mv == 0):
            b_mv = 3
    #Тактика - всегда бумага
    elif tactic == 2:
        b_mv = 3
    #Тактика - всегда ножницы
    elif tactic == 3:
        b_mv = 2
    #Тактика - всегда камень
    elif tactic == 4:
        b_mv = 1
    #Тактика - мимик, последний ход игрока
    elif tactic == 5:
        b_mv = last_p_mv
    #Тактика - до проигрыша, бот выбирает один и тот же элемент до первого проигрыша
    elif tactic == 6:
        if last_res == 0:
            b_mv = random.randint(1,3)
        else:
            b_mv = last_b_mv

    #Проверки на победу/ничью/проигрыш
    #В зависимости от исхода изменяем баланс игрока, запоминаем последний результат, изменяем поощрение тактики, изменяем сопутствующие переменные победы/проигрыша бота
    #Заполняем логи (step_arr)
    if (b_mv == 1 and p_move == 2) or (b_mv == 2 and p_move == 3) or (b_mv == 3 and p_move == 1):
        tact_arr[tactic] += 15
        balance -= step * 2
        out("Ваш ход: ", 1);out(game_arr[p_move * 2 - 1], 2);out("\nХод бота: ", 2);out(game_arr[b_mv * 2 - 1], 2);out("\n\nБОТ ВЫЙГРАЛ", 2);out(str('\nИзменение баланса: ' + str(step * -2)), 2)
        time.sleep(1)
        last_res = 1
        step_arr.insert(0, 1)
        bot_win += 2
        
    elif (b_mv == 2 and p_move == 1) or (b_mv == 3 and p_move == 2) or (b_mv == 1 and p_move == 3):
        tact_arr[tactic] -= 40
        balance += step * 2
        out("Ваш ход: ", 1);out(game_arr[p_move * 2 - 1], 2); out("\nХод бота: ", 2);out(game_arr[b_mv * 2 - 1], 2);out("\n\nВЫ ВЫЙГРАЛИ", 2);out(str('\nИзменение баланса: +' + str(step * 2)), 2)
        time.sleep(1)
        last_res = 0
        step_arr.insert(0, -1)
        bot_lose += 2
        
    else:
        out("Ваш ход: ", 1);out(game_arr[p_move * 2 - 1], 2);out("\nХод бота: ", 2);out(game_arr[b_mv * 2 - 1], 2);out("\n\nНИЧЬЯ", 2);out("\n0", 2)
        tact_arr[tactic] -= 15
        last_res = 1
        step_arr.insert(0, 0)
        bot_lose += 1

    #Дозаполняем соответствующие логи и переменные    
    time.sleep(1.2)
    #print("\nТактика бота: ", tactic)
    #print(tact_arr)
    #time.sleep(1) 
    step_arr.insert(0, p_move)
    step_arr.insert(0, b_mv)
    last_p_mv = p_move
    if (p_move == 1):
        rocks += 1
    elif (p_move == 2):
        scissors += 1
    else:
        papers += 1

#Функция вывода лога ходов в игре
def logs():
    #Опираясь на logs_amount сверху вниз выводим исходы последних ходов
    out("Последние " + str(logs_amount) + ":\n", 1)
    for i in range(logs_amount - 1, -1, -1):

        #каждый i*3 + 1 - ход игрока
        out("\nВаш ход: ", 2)
        if step_arr[i * 3 + 1] == 1:
            out("камень ", 2)
        elif step_arr[i * 3 + 1] == 2:
            out("ножницы", 2)
        elif step_arr[i * 3 + 1] == 3:
            out("бумага ", 2)
        else:
            out("-", 2)

        #каждый i*3 - ход бота
        out("     Ход бота: ", 2)
        if step_arr[i * 3] == 1:
            out("камень ", 2)
        elif step_arr[i * 3] == 2:
            out("ножницы", 2)
        elif step_arr[i * 3] == 3:
            out("бумага ", 2)
        else:
            out("-", 2)

        #каждый i * 3 + 2 - результат хода
        out("     Результат хода: ", 2)
        if step_arr[i * 3 + 2] == 0:
            out("Ничья", 2)
        elif step_arr[i * 3 + 2] == 1:
            out("бот победил", 2)
        elif step_arr[i * 3 + 2] == -1:
            out("вы победили", 2)
            
    #ожидание любого ввода, дабы игрок смог все прочитать        
    out("", 3)

#функци обвинения бота в жульничистве        
def blame(balance):
    global bot_blame, tact_arr
    #Запрос на значение ставки
    amount = out("Вы обивняете бота в жульничестве\nВведите сумму, которую вы готовы поставить\n\nВаш баланс: " + str(balance));
    #Проверяем на правильность ввода
    if not(is_int(amount)):
        out("Неправильный ввод\nВозвращаемся...", 1)
        time.sleep(1)
        return balance
    if int(amount) > int(balance) or int(amount) < 1:
        out("Неккоректное значение\nВозвращаемся...", 1)
        time.sleep(1)
        return balance
    else:
        #Если ввод правильный
        out("Вы поставили: ", 1);out(amount, 2);out("\nCверяем показания...", 2);
        time.sleep(2)
        if bot_blame == 1:
            #Если бот жульничал, обновляем баланс и обнуляем значение жульничества бота
            tact_arr[1] = 3 * bb_m_p
            out("Бот жульничал!", 1)
            bot_blame = 0
            time.sleep(1)
            return balance + int(amount) * 3
        elif bot_blame == 0:
            #Если бот не жульничал, возвращаем баланс - ставка
            out("Бот не жульничал...", 1)
            time.sleep(1)
            return balance - int(amount)
        
#Функция проверки выбора игрока
def checker(inp, arr):
    
    try:
        for i in arr:
    #Сверяем последовательно первые символы, при совпадении возвращаем результат
            if i[0] == inp[0]:
                #Так как есть 2 варианта, возвращаем индекс деленный на 2
                #Прибавляем 1 для удобной индексации
                return((arr.index(i)) // 2 + 1)
    #Если нет совпадений или слово слишком короткое или есть проблема с индексами
    except:
        return(999)
    return(999)

#Функция изменения настроек
def settings():
    global b_b_mp, st_balance, logs_amount
    #Пока человек не захочет вернуться, возвращаемся снова в это меню
    while (True):
        #Запрос выбора
        ans = checker(out("Выберите настройку, что хотите изменить:\n1)Баланс в начале\n2)Частота жульничества бота\n3)Количество ходов в логах\n4)Назад"), sett_arr)
        #Изменение изначального баланса и обработка правильности ввода
        if ans == 1:
            ans = out("Введите целое число от 1 до 100 - ваш новый баланс\nПо умолчанию: 40\nТекущее значение: " + str(st_balance))
            if is_int(ans):
                ans = int(ans)
                if ans >= 1 and ans <= 100:
                    st_balance = ans
                    out("Значениe нового изначального баланса установлено на: " + str(st_balance), 1)
                    time.sleep(1)
                else:
                    out("Неправильное значение...", 1)
                    time.sleep(1)
            else:
                out("Неправильный ввод...", 1)
                time.sleep(1)
        #Изменение значение частоты жульничества и обработка правильности ввода
        elif ans == 2:
            ans = out("Введите целое число от 1 до 5 - новая частота жульничества бота\nПо умолчанию: 2\nТекущее значение: " + str(b_b_mp))
            if is_int(ans):
                ans = int(ans)
                if ans >= 1 and ans <= 5:
                    b_b_mp = ans
                    out("Значениe жульничества бота установлено на: " + str(b_b_mp), 1)
                    time.sleep(1)
                else:
                    out("Неправильное значение...", 1)
                    time.sleep(1)
            else:
                out("Неправильный ввод...", 1)
                time.sleep(1)
        #Изменение кол-ва отображаемых логов
        elif ans == 3:
            ans = out("Введите целое число от 1 до 10 - количество отображаемых ходов в логах\nПо умолчанию: 5\nТекущее значение: " + str(logs_amount))
            if is_int(ans):
                ans = int(ans)
                if ans >= 1 and ans <= 10:
                    logs_amount = ans
                    out("Значениe нового изначального баланса установлено на: " + str(logs_amount), 1)
                    time.sleep(1)
                else:
                    out("Неправильное значение...", 1)
                    time.sleep(1)
            else:
                out("Неправильный ввод...", 1)
                time.sleep(1)
        #Возврат в меню
        elif ans == 4:
            out("Возвращаемся...", 1)
            time.sleep(1)
            break;
        #Неправильный ввод
        else:
            out("Неправильный ввод...", 1)
            time.sleep(1)

#Функция вывода правил игры
def rules():
    #Объяснение правил по запросу
    while (True):
        ans = checker(out("Выберите пункт правил, что вам интересен, или вернитесь в меню:\n\n1)Базовые правила камень-ножницы-бумаги\n2)Обман, ставки, жульничество\n3)Назад"), rules_arr)
        if (ans == 1):
            out("Основная часть игры состоит из правил игры в обычные КНП\nИграют два игрока. Они выбирают один из трех возможных вариантов: камень, ножницы, бумага\nКамень побеждает ножницы, бумага побеждает камень, ножницы побеждают бумагу. Два одинаковых варианта - ничья.")
        elif (ans == 2):
            out("Основное дополнение этой версии игры состоит в добавлении понятия баланса, ставки и жульничества\n\nБаланс: в начале игры вам выдается определенное кол-во монет.\nЗа каждую выйгранную или проигранную игру вам выдается или забирается, соответственно: n * 2 монет, где n - текущий номер хода\n\nЖульничество и ставка: периодически бот может начать жульничать. Он всегда будет выигрывать, и, пока вы его не разоблачите, он будет продолжать.\nПоэтому вы можете его в этом обвинить и поставить ставку - кол-во монет, что вы готовы поставить. При правильном предположении, ваша ставка возвращается к вам в утроенном размере. В ином случае вы теряете кол-во поставленных монет")
        elif (ans == 3):
            out("Возвращаемся...", 1)
            time.sleep(1)
            break;
        
#Функция проведения игры
def game():
    #Глобалим переменные, что необходимо будет возвращать, обновляем кол-во игр
    global bot_blame, balance, best_balance, best_step, balance, games_count
    games_count += 1
    step = 0
    balance = st_balance
    while (balance > 0):
        step += 1

        #Запрос на действие игрока
        out("Ход: ", 1);out(step, 2);out("\nВаш баланс: ", 2);out(balance, 2)
        ans = checker(out("\n\n1)Камень\n2)Ножницы\n3)Бумага\n4)Обвинить бота в жульничистве\n5)Лог последних ходов\n6)Сдаться", 3), game_arr)
        #Если игрок ходит, вычисляем тактику и бот ходит
        if ans > 0 and ans < 4:
            tactics()
            bot_move(ans, step)
        #Обвинение бота в жульничестве
        elif ans == 4:
            balance = blame(balance)
            step -= 1
        #Просмотр логов
        elif ans == 5:
            logs()
            step -= 1
        #Выход
        elif ans == 6:
            bot_blame = 0
            break
        #Обработка неправильного ввода
        elif ans == 999:
            out("Неправильный ввод...", 1)
            time.sleep(1)
            step -= 1
    #Выход из цикла и окончание игры
    out("Вы проиграли...", 1);
    time.sleep(2)

#Функция вывода главного меню
def main():
    #Выводим меню
    ans = checker(out(" Камень, Ножницы, Бумага, Ложь\n1)Играть\n2)Правила\n3)Настройки\n4)Выход"), main_arr)
    #Сверяем ответ
    if ans == 1:
        game()
    elif ans == 2:
        rules()
    elif ans == 3:
        settings()
    elif ans == 4:
        quit()
    elif ans == 999:
        out("Неправильный ввод...", 1)
        time.sleep(1)

if (__name__ == "__main__"):
    #Маленькая инструкция при запуске
    out("Для выбора варианта вводите цифры или первое слово запроса в консоль", 1)
    time.sleep(3)
    #Цикл, дабы при выходе из всех функций, игрок возвращался в меню
    while(True):
        #Главное меню
        main()
        #Очищение всех переменных после игры
        clear()
