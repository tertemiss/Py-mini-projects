#импорт необходимых библиотек
#pygame - визуализация, math - подсчеты, sys - выход 
import pygame
import sys
import math
import random

#Инициализация Pygame
pygame.init()

#Параметры экрана
WIDTH, HEIGHT = 800, 600

#Множитель отталкивания шаров
FRICTION = 0.87
#Высота пола - 50px
FLOOR = 50
#Множитель гравитации
GRAVITY = 0.1
#Минимальная масса объекта, чтобы не происходило деление на 0 
MIN_MASS = 0.000001
#Максимальная масса шара -> максимальный размер
MAX_MASS = 20
#Отступ стен
WALL = 1


#Инициализация цветов для читабельности кода
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

#Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dnd")

#Класс для объектов ball
class Ball:
    def __init__(self, x, y, mass):
        #Основные параметры ball
        #Положение шара в пространстве
        self.x = x
        self.y = y
        #Масса шара
        self.mass = mass
        #Радиус шара, в 2 раза больше массы
        self.radius = mass * 2
        #Цвет шаров - синий
        self.color = BLUE
        #Флаг, означающий, что объект перетаскивают
        self.dragging = False
        #Скорость объекта по x
        self.velocity_x = 0
        #Скорость объекта по y
        self.velocity_y = 0
        #Стандартный коэффициент замедления (коэффициент трения об пол)
        self.friction_x = 0.994

    def draw(self):
        #Отрисовка круга
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        #Если объект перетаскивают
        if self.dragging:
            #То перемещаем его на координаты мышки
            self.x, self.y = pygame.mouse.get_pos()
        #В другом случае счиатем координаты через скорости
        else:
            #Применяем гравитацию, чем больше масса - тем быстрее объект накапливает скорость
            #Этим уравнивается то, что чем больше объект - тем больше скорости нужно для его движения
            self.velocity_y += GRAVITY * (self.mass / 2)
            #Замедляем объект по горизонтали (трение)
            self.velocity_x *= self.friction_x
            #Объект горизонтально и вертикально двигается со скоростью, замедленной от его массы
            self.x += self.velocity_x * (1 / self.mass + MIN_MASS)
            self.y += self.velocity_y * (1 / self.mass + MIN_MASS)
            #Проверяем отскок от стен
            #Если коснулись левой либо правой стены, то отталкиваемся
            #Левая стена
            if self.x < self.radius + WALL:
                #Меняем направление вектора скорости на противоположное с коэффициентом отталкивания
                self.velocity_x *= -FRICTION * min(11 / self.mass + MIN_MASS, 1)
                #Дабы не застревать в потолке - сдвигаем шар вниз
                self.x = self.radius + WALL
            #Правая стена
            if self.x > WIDTH - WALL - self.radius:
                #Меняем направление вектора скорости на противоположное с коэффициентом отталкивания
                self.velocity_x *= -FRICTION * min(11 / self.mass + MIN_MASS, 1)
                #Дабы не застревать в стене - сдвигаем шар
                self.x = WIDTH - WALL - self.radius
            #Если мы коснулись пола, то отталкиваемся
            if self.y > HEIGHT - FLOOR - self.radius:
                #Из-за отскока - отражаем вектор скорости y и замедляем в зависимости от массы и коэф. отталкивания
                self.velocity_y *= -FRICTION * min(11 / self.mass + MIN_MASS, 1)
                #Определяем положение шара, чтобы он не проваливался в пол
                self.y = HEIGHT - FLOOR - self.radius
            #Если мы коснулись потолка
            if self.y < self.radius + WALL:
                #Из-за отскока - отражаем вектор скорости y и замедляем в зависимости от массы и коэф. отталкивания
                self.velocity_y *= -FRICTION * min(11 / self.mass + MIN_MASS, 1)
                #Дабы не застревать в потолке - сдвигаем шар вниз
                self.y = self.radius + WALL

#Функция для обработки столкновений
def handle_collision(ball1, ball2):
    #Отрезок по горизонтали
    dx = ball2.x - ball1.x
    #Отрезок по вертикали
    dy = ball2.y - ball1.y
    #Расстояние между шарами (Т. Пифагора)
    dist = math.sqrt(dx ** 2 + dy ** 2)
    #Пересечение границ объектов
    overlap = ball1.radius + ball2.radius - dist
    #Если объекты все же пересекаются
    if overlap > 0:
        #отношение y:x
        angle = math.atan2(dy, dx)
        #math.cos(angle) - > коэффициент смещения по x, отношение x к гипотенузе
        #т.е. к x первого шара добавляем коээфициент смещения по x по его радиусу
        #Ищем точку соприкосновения по x
        target_x = ball1.x + math.cos(angle) * ball1.radius
        #math.sin(angle) - > коэффициент смещения по y, отношение y к гипотенузе
        #т.е. к y первого шара добавляем коээфициент смещения по y по его радиусу
        #Ищем точку соприкосновения по y
        target_y = ball1.y + math.sin(angle) * ball1.radius
        #Так как dy и dx = ball2 - ball1, а angle зависит от них, то:
        #От первого шара всегда отбавляем, ко второму прибавляем
        #Если масса первого больше массы второго
        if (ball1.mass > ball2.mass):
            #Больше скорость -> больше overlap -> больше выходная скорость
            #Так же как и в target_x, target_y считаем коэффициент через math.cos/sin(angle)
            #Для шара с большей массой - ball2.mass / ball1.mass -> малое отталкивание
            #Для шара с меньшей массой - (1 - ball2.mass / ball1.mass) * 0.9 -> большее отталкивание
            ball1.velocity_x -= overlap * math.cos(angle) * ball2.mass / ball1.mass
            ball1.velocity_y -= overlap * math.sin(angle) * ball2.mass / ball1.mass
            ball2.velocity_x += overlap * math.cos(angle) * (1 - ball2.mass / ball1.mass) * 0.9
            ball2.velocity_y += overlap * math.sin(angle) * (1 - ball2.mass / ball1.mass) * 0.9
        #Если масса второго больше массы первого
        elif (ball1.mass < ball2.mass):
            #Больше скорость -> больше overlap -> больше выходная скорость
            #Так же как и в target_x, target_y считаем коэффициент через math.cos/sin(angle)
            #Для шара с большей массой - ball2.mass / ball1.mass -> малое отталкивание
            #Для шара с меньшей массой - (1 - ball2.mass / ball1.mass) * 0.9 -> большее отталкивание
            ball1.velocity_x -= overlap * math.cos(angle) * (1 - ball1.mass / ball2.mass) * 0.9
            ball1.velocity_y -= overlap * math.sin(angle) * (1 - ball1.mass / ball2.mass) * 0.9
            ball2.velocity_x += overlap * math.cos(angle) * ball1.mass / ball2.mass
            ball2.velocity_y += overlap * math.sin(angle) * ball1.mass / ball2.mass
        #Если массы объектов равны
        else:
            #Больше скорость -> больше overlap -> больше выходная скорость
            #Так же как и в target_x, target_y считаем коэффициент через math.cos/sin(angle)
            ball1.velocity_x -= overlap * math.cos(angle)
            ball1.velocity_y -= overlap * math.sin(angle)
            ball2.velocity_x += overlap * math.cos(angle)
            ball2.velocity_y += overlap * math.sin(angle)


#Функция для отображения массы и скорости шара при наведении
def draw_info_label(ball):
    #Определяем шрифт
    font = pygame.font.Font(None, 24)
    #Надпись для массы
    mass_label = font.render(f"Mass: {round(ball.mass, 2)}", True, BLACK)
    #Надпись для скорости
    velocity_label = font.render(f"Velocity: ({ball.velocity_x:.0f}, {ball.velocity_y:.0f})", True, BLACK)
    #Выводим массу снизу от шара на 10px
    screen.blit(mass_label, (ball.x - ball.radius, ball.y + ball.radius + 10))
    #Выводим скорость снизу от шара на 30px
    screen.blit(velocity_label, (ball.x - ball.radius, ball.y + ball.radius + 30))

#Массив хранения объектов
balls = []

#Переменные для отслеживания времени удержания ПКМ
#Флаг, зажата ли ПКМ
right_click_pressed = False
#Время в которое зажали ПКМ
right_click_start_time = 0

# Главный цикл программы
running = True
FLOOR = 1
while running:
    x = random.randint(-5, 5)
    if (FLOOR > 250):
        x = random.randint(-100, 0)
    if (x == 0):
        x += 6;
    FLOOR += x
    WALL += x
    #Заполняем весь экран белым
    screen.fill(WHITE)
    #Получаем позицию мыши
    mouse_pos = pygame.mouse.get_pos()

    #Просматриваем все event в pygame
    for event in pygame.event.get():
        #Если event - выход из игры, то завершаем цикл
        if event.type == pygame.QUIT:
            running = False
        #Если кликнули по мышке
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Если нажата ЛКМ
            if event.button == 1:
                #Проверяем шары и смотрим какой из них мы хотим захватить
                for ball in balls:
                    #Если координаты совпадают, то говорим, что мы хотим перетащить этот шар
                    if pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, 2 * ball.radius, 2 * ball.radius).collidepoint(event.pos):
                        #Флаг перетаскивания = true
                        ball.dragging = True
                        #Обнуляем скорости
                        ball.velocity_x = 0
                        ball.velocity_y = 0
            #Если нажата ПКМ
            elif event.button == 3:
                #Флаг нажатия правой кнопки
                right_click_pressed = True
                #Запоминаем нажатие правой кнопки
                right_click_start_time = pygame.time.get_ticks()

        #Если кнопку на мыши отжали
        elif event.type == pygame.MOUSEBUTTONUP:
            #Если ПКМ отжали
            if event.button == 3:
                #Если она была нажата
                if right_click_pressed:
                    #Обнуляем флаг
                    right_click_pressed = False
                    #Запоминаем x, y
                    x, y = event.pos
                    #Время, которое был зажат ПКМ
                    elapsed_time = pygame.time.get_ticks() - right_click_start_time
                    #Высчитываем массу шара
                    mass = min(MAX_MASS, elapsed_time // 100 + 0.000001)
                    #Создаем шар на координатах x, y, с массой mass
                    new_ball = Ball(x, y, mass)
                    #Добавляем в массив шаров новый объект
                    balls.append(new_ball)
            #Если ЛКМ отжали
            elif event.button == 1:
                #Проходимся по всем объектам в списке
                for ball in balls:
                    #Если мышка на шаре -> его перетаскивали -> отключаем перетаскивание
                    if pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, 2 * ball.radius, 2 * ball.radius).collidepoint(event.pos):
                        ball.dragging = False
        #Если отжали кнопку "c" -> очищаем экран (обнуляем массив объектов)
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_c:
                 balls = []
    #При зажатой ПКМ отрисовываем шар и его рост
    if right_click_pressed:
        #Запоминаем x, y
        x, y = event.pos
        #Запоминаем время, прошедшее между зажатием пкм и этим моментом
        elapsed_time = pygame.time.get_ticks() - right_click_start_time
        #Вычисляем массу
        mass = min(MAX_MASS, elapsed_time // 100 + 0.000001)
        #Создаем временный шар, что сразу удалится в начале цикла после отрисовки
        new_ball = Ball(x, y, mass)
        #Добавляем объект в массив для единичной отрисовки
        balls.append(new_ball)

    #Проходимся по всем объектам
    for ball in balls:
        #Если курсор на шаре, то выводим под ним массу и скорость
        if pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, 2 * ball.radius, 2 * ball.radius).collidepoint(mouse_pos):
            draw_info_label(ball)
        #ball.radius -= 0.01
        #Обновляем хар-ки объекта
        ball.update()
        #Отрисовываем объект
        ball.draw()
        
    #Если был зажат ПКМ -> последний объект в массиве - временный, удаляем
    if right_click_pressed:
        balls.pop(len(balls) - 1)

    #Отрисовка стен
    #Пол
    pygame.draw.line(screen, BLACK, (0, HEIGHT - FLOOR), (WIDTH, HEIGHT - FLOOR), 3)
    #Левая стена
    pygame.draw.line(screen, BLACK, (WALL, 0), (WALL, HEIGHT), 3)
    #Правая стена
    pygame.draw.line(screen, BLACK, (WIDTH - WALL, 0), (WIDTH - WALL, HEIGHT), 3)
    #Потолок
    pygame.draw.line(screen, BLACK, (0, WALL), (WIDTH, WALL), 3)

    #Проходимся по всем парам объектов
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            #Просчитываем коллизию между объектами
            handle_collision(balls[i], balls[j])

    #Обновляем экран
    pygame.display.flip()

    #Счетчик pygame
    pygame.time.Clock().tick(60)

#Вышли из цикла -> выходим из игры и из программы
pygame.quit()
sys.exit()
