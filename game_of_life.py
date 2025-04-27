#Подключаем необходимые библиотеки
#Pygame - отрисовка поля
#numpy - упрощение вычислений/операции
import pygame
import numpy as np

#Определение размеров окна
width, height = 800, 600
#Определение размеров клетки
c_size = 10
#Определение количества клеток по горизонтали и вертикали
c_width = width // c_size
c_height = height // c_size

#Создание пустого поля
def empty():
    return np.zeros((c_width, c_height), dtype=int)

#Функция для отрисовки текущего состояния поля
def draw_grid(screen, grid):
    #Заполнение окна белым цветом
    screen.fill((255, 255, 255))
    #Отрисовка горизонтальных линий
    for y in range(0, height, c_size):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (width, y))
    #Отрисовка вертикальных линий
    for x in range(0, width, c_size):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, height))
    #Отрисовка живых клеток
    for x in range(c_width):
        for y in range(c_height):
            if grid[x][y] == 1:
                pygame.draw.rect(screen, (0, 0, 0), (x * c_size, y * c_size, c_size, c_size))

#Функция для преобразования координат мыши в координаты ячейки поля
def on_click(pos):
    x, y = pos
    #Координаты по x, y для новой клетки
    cell_x = x // c_size
    cell_y = y // c_size
    return cell_x, cell_y

#Функция для обновления состояния поля на следующий шаг
def update_grid(grid):
    #Копируем текущее поле
    new_grid = np.copy(grid)
    #Проходимся циклом по каждой клетке
    for x in range(c_width):
        for y in range(c_height):
            #Считаем кол-во соседей для каждой клетки
            neighbors = count_neighbors(grid, x, y)
            #Если клетка живая
            if grid[x][y] == 1:
                #Если соседей меньше 2 или больше 3, клетка умирает
                if neighbors < 2 or neighbors > 3:
                    new_grid[x][y] = 0
            #Если клетка не живая
            else:
                #Если соседей 3
                if neighbors == 3:
                    #Клетка становится живой
                    new_grid[x][y] = 1
    #Возвращаем обновленное поле
    return new_grid

#Функция для определения кол-ва живых соседей для клетки
def count_neighbors(grid, x, y):
    #Счетчик соседей
    count = 0
    #Цикл, проходящийся по кавдрату 3x3
    for i in range(-1, 2):
        for j in range(-1, 2):
            #Пропуск подсчета самой себя
            if i == 0 and j == 0:
                continue
            #Если не уходим за границы поля, то прибавляем значение соседней клетки
            #1 - живая клетка, 0 - мертвая
            if 0 <= x + i < c_width and 0 <= y + j < c_height:
                count += grid[x + i][y + j]
    #Возвращаем кол-во живых соседей
    return count

def main():
    #Выводим в терминал инструкцию по работе с игрой
    print('''\nИнструкция:\n"ЛКМ" - поставить живую клетку\n"ПКМ" - удалить живую клетку\n"space" - остановить/запустить генерацию\n"c" - очистить поле\n"q" - выйти из игры''')
    #Запускаем pygame окно
    pygame.init()
    #Редактируем окно под нужные размеры
    screen = pygame.display.set_mode((width, height))
    #Заголовок окна
    pygame.display.set_caption("Game of Life")

    #Размер надписи о кол-ве генераций
    font = pygame.font.Font(None, 36)
    #Счетчик генераций
    generation = 0

    #Инициализируем пустое поле
    grid = empty()

    #Происходит ли редактирование поля
    editing = True
    #Запущена ли игра
    running = False
    #Приостановлена ли генерация
    paused = False

    #Пока мы редактируем
    while editing:
        #Считываем клавиши/нажатия мыши
        for event in pygame.event.get():
            #Если выходим из игры, то останавливаем циклы
            if event.type == pygame.QUIT:
                editing = False
                running = False
            #Если кликаем мышью
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #ЛКМ
                if pygame.mouse.get_pressed()[0]:
                    #Позиция клика
                    pos = pygame.mouse.get_pos()
                    cell_x, cell_y = on_click(pos)
                    #Меняем значение в поле на единицу
                    grid[cell_x][cell_y] = 1
                #ПКМ
                elif pygame.mouse.get_pressed()[2]:
                    #Позиция клика
                    pos = pygame.mouse.get_pos()
                    cell_x, cell_y = on_click(pos)
                    #Меняем значение в поле на ноль
                    grid[cell_x][cell_y] = 0
            #Если нажали какую-то клавишу
            elif event.type == pygame.KEYDOWN:
                #Если эта клавиша - пробел
                if event.key == pygame.K_SPACE:
                    #Если игра не запущена - запускаем
                    if not running:
                        running = True
                    #Менеям значение генерации на противопожожное
                    paused = not paused
                    #Если запустили - обнуляем генерации
                    if not paused:
                        generation = 0
                #Если нажали "c", то обнуляем поле и значение генераций
                elif event.key == pygame.K_c:
                    grid = empty()
                    generation = 0
                #Если нажали "q", то выходим из всех циклов
                elif event.key == pygame.K_q:
                    editing = False
                    running = False
                    
        #Если игра запущена и не на паузе
        if running and not paused:
            grid = update_grid(grid)
            generation += 1
        
        #Отрисовываем новое поле
        draw_grid(screen, grid)

        #Отображение счетчика генераций
        text = font.render(f"Generation: {generation}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        #Обновляем дисплей
        pygame.display.flip()

    #Если выходим из всех цилов - выходим из игры
    pygame.quit()
