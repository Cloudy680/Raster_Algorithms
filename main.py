"""
Лабораторная работа 4: Базовые растровые алгоритмы
Реализация алгоритмов растеризации отрезков и окружностей
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import math
from typing import List, Tuple


class RasterAlgorithms:
    """Класс с реализацией всех растровых алгоритмов"""
    
    @staticmethod
    def step_by_step(x1: int, y1: int, x2: int, y2: int) -> List[Tuple[int, int]]:
        """
        Пошаговый алгоритм растеризации отрезка
        
        Args:
            x1, y1: координаты начальной точки
            x2, y2: координаты конечной точки
            
        Returns:
            список координат точек (x, y)
        """
        points = []
        dx = x2 - x1
        dy = y2 - y1
        
        # Определяем количество шагов
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            return [(x1, y1)]
        
        # Вычисляем приращения
        x_increment = dx / steps
        y_increment = dy / steps
        
        # Начальные координаты
        x = float(x1)
        y = float(y1)
        
        # Генерируем точки
        for _ in range(steps + 1):
            points.append((round(x), round(y)))
            x += x_increment
            y += y_increment
            
        return points
    
    @staticmethod
    def dda(x1: int, y1: int, x2: int, y2: int) -> List[Tuple[int, int]]:
        """
        Алгоритм ЦДА (DDA - Digital Differential Analyzer)
        
        Args:
            x1, y1: координаты начальной точки
            x2, y2: координаты конечной точки
            
        Returns:
            список координат точек (x, y)
        """
        points = []
        dx = x2 - x1
        dy = y2 - y1
        
        # Определяем количество шагов
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            return [(x1, y1)]
        
        # Вычисляем приращения
        x_increment = dx / steps
        y_increment = dy / steps
        
        # Начальные координаты
        x = float(x1)
        y = float(y1)
        
        # Генерируем точки
        for _ in range(steps + 1):
            points.append((int(x + 0.5), int(y + 0.5)))
            x += x_increment
            y += y_increment
            
        return points
    
    @staticmethod
    def bresenham_line(x1: int, y1: int, x2: int, y2: int) -> List[Tuple[int, int]]:
        """
        Алгоритм Брезенхема для отрезка
        
        Args:
            x1, y1: координаты начальной точки
            x2, y2: координаты конечной точки
            
        Returns:
            список координат точек (x, y)
        """
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        # Определяем направление
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        err = dx - dy
        x, y = x1, y1
        
        while True:
            points.append((x, y))
            
            if x == x2 and y == y2:
                break
                
            e2 = 2 * err
            
            if e2 > -dy:
                err -= dy
                x += sx
                
            if e2 < dx:
                err += dx
                y += sy
                
        return points
    
    @staticmethod
    def bresenham_circle(xc: int, yc: int, r: int) -> List[Tuple[int, int]]:
        """
        Алгоритм Брезенхема для окружности
        
        Args:
            xc, yc: координаты центра окружности
            r: радиус окружности
            
        Returns:
            список координат точек (x, y)
        """
        points = []
        x = 0
        y = r
        d = 3 - 2 * r
        
        def add_circle_points(xc, yc, x, y):
            """Добавляем 8 симметричных точек"""
            pts = [
                (xc + x, yc + y),
                (xc - x, yc + y),
                (xc + x, yc - y),
                (xc - x, yc - y),
                (xc + y, yc + x),
                (xc - y, yc + x),
                (xc + y, yc - x),
                (xc - y, yc - x)
            ]
            return pts
        
        while y >= x:
            points.extend(add_circle_points(xc, yc, x, y))
            x += 1
            
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
                
        # Удаляем дубликаты
        return list(set(points))


class RasterVisualizerApp:
    """Главное приложение для визуализации растровых алгоритмов"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа 4: Базовые растровые алгоритмы")
        self.root.geometry("1400x900")
        
        # Параметры визуализации
        self.cell_size = 20  # Размер одной клетки в пикселях
        self.grid_width = 40  # Ширина сетки в клетках
        self.grid_height = 30  # Высота сетки в клетках
        self.offset_x = 50  # Отступ слева для подписей
        self.offset_y = 50  # Отступ сверху для подписей
        
        self.algorithms = RasterAlgorithms()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        
        # Создаем основной контейнер
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель с настройками
        left_panel = ttk.Frame(main_container, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Правая панель с визуализацией
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # === Левая панель ===
        
        # Заголовок
        title_label = ttk.Label(left_panel, text="Параметры алгоритма", 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=10)
        
        # Выбор алгоритма
        algo_frame = ttk.LabelFrame(left_panel, text="Выбор алгоритма", padding=10)
        algo_frame.pack(fill=tk.X, pady=5)
        
        self.algorithm_var = tk.StringVar(value="step")
        
        algorithms = [
            ("Пошаговый алгоритм", "step"),
            ("Алгоритм ЦДА", "dda"),
            ("Алгоритм Брезенхема (отрезок)", "bresenham_line"),
            ("Алгоритм Брезенхема (окружность)", "bresenham_circle")
        ]
        
        for text, value in algorithms:
            rb = ttk.Radiobutton(algo_frame, text=text, variable=self.algorithm_var, 
                                value=value, command=self.on_algorithm_change)
            rb.pack(anchor=tk.W, pady=2)
        
        # Параметры для линии
        self.line_frame = ttk.LabelFrame(left_panel, text="Параметры отрезка", padding=10)
        self.line_frame.pack(fill=tk.X, pady=5)
        
        # Начальная точка
        ttk.Label(self.line_frame, text="Начальная точка (x1, y1):").pack(anchor=tk.W)
        point1_frame = ttk.Frame(self.line_frame)
        point1_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(point1_frame, text="x1:").pack(side=tk.LEFT)
        self.x1_var = tk.StringVar(value="5")
        ttk.Entry(point1_frame, textvariable=self.x1_var, width=8).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(point1_frame, text="y1:").pack(side=tk.LEFT)
        self.y1_var = tk.StringVar(value="5")
        ttk.Entry(point1_frame, textvariable=self.y1_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Конечная точка
        ttk.Label(self.line_frame, text="Конечная точка (x2, y2):").pack(anchor=tk.W, pady=(10, 0))
        point2_frame = ttk.Frame(self.line_frame)
        point2_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(point2_frame, text="x2:").pack(side=tk.LEFT)
        self.x2_var = tk.StringVar(value="15")
        ttk.Entry(point2_frame, textvariable=self.x2_var, width=8).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(point2_frame, text="y2:").pack(side=tk.LEFT)
        self.y2_var = tk.StringVar(value="12")
        ttk.Entry(point2_frame, textvariable=self.y2_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Параметры для окружности
        self.circle_frame = ttk.LabelFrame(left_panel, text="Параметры окружности", padding=10)
        
        ttk.Label(self.circle_frame, text="Центр окружности (xc, yc):").pack(anchor=tk.W)
        center_frame = ttk.Frame(self.circle_frame)
        center_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(center_frame, text="xc:").pack(side=tk.LEFT)
        self.xc_var = tk.StringVar(value="20")
        ttk.Entry(center_frame, textvariable=self.xc_var, width=8).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(center_frame, text="yc:").pack(side=tk.LEFT)
        self.yc_var = tk.StringVar(value="15")
        ttk.Entry(center_frame, textvariable=self.yc_var, width=8).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.circle_frame, text="Радиус:").pack(anchor=tk.W, pady=(10, 0))
        radius_frame = ttk.Frame(self.circle_frame)
        radius_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(radius_frame, text="r:").pack(side=tk.LEFT)
        self.r_var = tk.StringVar(value="8")
        ttk.Entry(radius_frame, textvariable=self.r_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Кнопка построения
        build_btn = ttk.Button(left_panel, text="Построить", command=self.build_raster)
        build_btn.pack(pady=10, fill=tk.X)
        
        # Информация о времени выполнения
        info_frame = ttk.LabelFrame(left_panel, text="Информация", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=10, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # === Правая панель ===
        
        # Canvas для визуализации
        canvas_frame = ttk.LabelFrame(right_panel, text="Визуализация", padding=5)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создаем canvas с возможностью прокрутки
        self.canvas = tk.Canvas(canvas_frame, bg="white", 
                               width=self.grid_width * self.cell_size + self.offset_x * 2,
                               height=self.grid_height * self.cell_size + self.offset_y * 2)
        
        # Скроллбары
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Размещение
        self.canvas.grid(row=0, column=0, sticky="nsew")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Настройка области прокрутки
        self.canvas.configure(scrollregion=(0, 0, 
                                           self.grid_width * self.cell_size + self.offset_x * 2,
                                           self.grid_height * self.cell_size + self.offset_y * 2))
        
        # Инициализация
        self.on_algorithm_change()
        self.draw_grid()
        
    def on_algorithm_change(self):
        """Обработчик изменения алгоритма"""
        if self.algorithm_var.get() == "bresenham_circle":
            self.line_frame.pack_forget()
            self.circle_frame.pack(fill=tk.X, pady=5)
        else:
            self.circle_frame.pack_forget()
            self.line_frame.pack(fill=tk.X, pady=5)
    
    def draw_grid(self):
        """Отрисовка координатной сетки"""
        self.canvas.delete("all")
        
        # Рисуем сетку
        for i in range(self.grid_width + 1):
            x = self.offset_x + i * self.cell_size
            self.canvas.create_line(x, self.offset_y, 
                                   x, self.offset_y + self.grid_height * self.cell_size,
                                   fill="#dddddd", width=1)
            
            # Подписи по X (каждые 5 клеток)
            if i % 5 == 0:
                self.canvas.create_text(x, self.offset_y - 10, text=str(i), 
                                       font=("Arial", 8))
        
        for i in range(self.grid_height + 1):
            y = self.offset_y + i * self.cell_size
            self.canvas.create_line(self.offset_x, y, 
                                   self.offset_x + self.grid_width * self.cell_size, y,
                                   fill="#dddddd", width=1)
            
            # Подписи по Y (каждые 5 клеток)
            if i % 5 == 0:
                self.canvas.create_text(self.offset_x - 15, y, text=str(i), 
                                       font=("Arial", 8))
        
        # Оси координат (жирные линии через начало координат)
        self.canvas.create_line(self.offset_x, self.offset_y, 
                               self.offset_x, self.offset_y + self.grid_height * self.cell_size,
                               fill="#000000", width=2)
        self.canvas.create_line(self.offset_x, self.offset_y, 
                               self.offset_x + self.grid_width * self.cell_size, self.offset_y,
                               fill="#000000", width=2)
        
        # Подписи осей
        self.canvas.create_text(self.offset_x + self.grid_width * self.cell_size + 20, 
                               self.offset_y, text="X", font=("Arial", 12, "bold"))
        self.canvas.create_text(self.offset_x, 
                               self.offset_y + self.grid_height * self.cell_size + 20, 
                               text="Y", font=("Arial", 12, "bold"))
    
    def draw_point(self, x: int, y: int, color: str = "blue"):
        """Отрисовка точки на сетке"""
        canvas_x = self.offset_x + x * self.cell_size
        canvas_y = self.offset_y + y * self.cell_size
        
        # Рисуем закрашенную клетку
        self.canvas.create_rectangle(canvas_x + 1, canvas_y + 1,
                                     canvas_x + self.cell_size - 1,
                                     canvas_y + self.cell_size - 1,
                                     fill=color, outline="")
    
    def build_raster(self):
        """Построение растра по выбранному алгоритму"""
        try:
            algorithm = self.algorithm_var.get()
            
            # Очищаем информацию
            self.info_text.delete(1.0, tk.END)
            
            # Перерисовываем сетку
            self.draw_grid()
            
            # Выполняем алгоритм
            start_time = time.perf_counter()
            
            if algorithm == "bresenham_circle":
                xc = int(self.xc_var.get())
                yc = int(self.yc_var.get())
                r = int(self.r_var.get())
                
                points = self.algorithms.bresenham_circle(xc, yc, r)
                
                self.info_text.insert(tk.END, f"Алгоритм: Брезенхем (окружность)\n")
                self.info_text.insert(tk.END, f"Параметры: центр ({xc}, {yc}), радиус {r}\n")
                
            else:
                x1 = int(self.x1_var.get())
                y1 = int(self.y1_var.get())
                x2 = int(self.x2_var.get())
                y2 = int(self.y2_var.get())
                
                if algorithm == "step":
                    points = self.algorithms.step_by_step(x1, y1, x2, y2)
                    algo_name = "Пошаговый алгоритм"
                elif algorithm == "dda":
                    points = self.algorithms.dda(x1, y1, x2, y2)
                    algo_name = "Алгоритм ЦДА"
                else:  # bresenham_line
                    points = self.algorithms.bresenham_line(x1, y1, x2, y2)
                    algo_name = "Алгоритм Брезенхема (отрезок)"
                
                self.info_text.insert(tk.END, f"Алгоритм: {algo_name}\n")
                self.info_text.insert(tk.END, f"Параметры: от ({x1}, {y1}) до ({x2}, {y2})\n")
            
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000000  # в микросекундах
            
            # Отрисовываем точки
            for point in points:
                if 0 <= point[0] < self.grid_width and 0 <= point[1] < self.grid_height:
                    self.draw_point(point[0], point[1], "blue")
            
            # Отображаем начальную и конечную точки другим цветом
            if algorithm != "bresenham_circle":
                x1 = int(self.x1_var.get())
                y1 = int(self.y1_var.get())
                x2 = int(self.x2_var.get())
                y2 = int(self.y2_var.get())
                
                if 0 <= x1 < self.grid_width and 0 <= y1 < self.grid_height:
                    self.draw_point(x1, y1, "green")
                if 0 <= x2 < self.grid_width and 0 <= y2 < self.grid_height:
                    self.draw_point(x2, y2, "red")
            
            # Выводим информацию
            self.info_text.insert(tk.END, f"\nКоличество точек: {len(points)}\n")
            self.info_text.insert(tk.END, f"Время выполнения: {execution_time:.2f} мкс ({execution_time/1000:.4f} мс)\n")
            
            # Показываем пример вычислений для первых нескольких точек
            self.info_text.insert(tk.END, f"\n--- Пример вычислений ---\n")
            
            if algorithm == "step" or algorithm == "dda":
                x1 = int(self.x1_var.get())
                y1 = int(self.y1_var.get())
                x2 = int(self.x2_var.get())
                y2 = int(self.y2_var.get())
                
                dx = x2 - x1
                dy = y2 - y1
                steps = max(abs(dx), abs(dy))
                
                self.info_text.insert(tk.END, f"dx = {x2} - {x1} = {dx}\n")
                self.info_text.insert(tk.END, f"dy = {y2} - {y1} = {dy}\n")
                self.info_text.insert(tk.END, f"steps = max(|{dx}|, |{dy}|) = {steps}\n")
                
                if steps > 0:
                    x_inc = dx / steps
                    y_inc = dy / steps
                    self.info_text.insert(tk.END, f"x_increment = {dx}/{steps} = {x_inc:.4f}\n")
                    self.info_text.insert(tk.END, f"y_increment = {dy}/{steps} = {y_inc:.4f}\n\n")
                    
                    # Первые 5 итераций
                    self.info_text.insert(tk.END, "Первые точки:\n")
                    for i in range(min(5, len(points))):
                        x = x1 + i * x_inc
                        y = y1 + i * y_inc
                        if algorithm == "step":
                            self.info_text.insert(tk.END, 
                                f"Шаг {i}: x={x:.2f}, y={y:.2f} → ({round(x)}, {round(y)})\n")
                        else:  # dda
                            self.info_text.insert(tk.END, 
                                f"Шаг {i}: x={x:.2f}, y={y:.2f} → ({int(x+0.5)}, {int(y+0.5)})\n")
            
            elif algorithm == "bresenham_line":
                x1 = int(self.x1_var.get())
                y1 = int(self.y1_var.get())
                x2 = int(self.x2_var.get())
                y2 = int(self.y2_var.get())
                
                dx = abs(x2 - x1)
                dy = abs(y2 - y1)
                
                self.info_text.insert(tk.END, f"dx = |{x2} - {x1}| = {dx}\n")
                self.info_text.insert(tk.END, f"dy = |{y2} - {y1}| = {dy}\n")
                self.info_text.insert(tk.END, f"Начальная ошибка: err = dx - dy = {dx} - {dy} = {dx - dy}\n\n")
                
                # Симуляция первых нескольких шагов
                sx = 1 if x1 < x2 else -1
                sy = 1 if y1 < y2 else -1
                err = dx - dy
                x, y = x1, y1
                
                self.info_text.insert(tk.END, "Первые итерации:\n")
                for i in range(min(5, len(points))):
                    self.info_text.insert(tk.END, f"Шаг {i}: ({x}, {y}), err={err}\n")
                    
                    if x == x2 and y == y2:
                        break
                    
                    e2 = 2 * err
                    if e2 > -dy:
                        err -= dy
                        x += sx
                    if e2 < dx:
                        err += dx
                        y += sy
            
            elif algorithm == "bresenham_circle":
                xc = int(self.xc_var.get())
                yc = int(self.yc_var.get())
                r = int(self.r_var.get())
                
                self.info_text.insert(tk.END, f"Центр: ({xc}, {yc})\n")
                self.info_text.insert(tk.END, f"Радиус: {r}\n")
                self.info_text.insert(tk.END, f"Начальное значение параметра решения: d = 3 - 2*r = 3 - 2*{r} = {3 - 2*r}\n\n")
                
                # Симуляция первых нескольких шагов
                x = 0
                y = r
                d = 3 - 2 * r
                
                self.info_text.insert(tk.END, "Первые итерации:\n")
                for i in range(min(5, r + 1)):
                    self.info_text.insert(tk.END, f"Шаг {i}: x={x}, y={y}, d={d}\n")
                    self.info_text.insert(tk.END, f"  → 8 точек: ({xc}±{x}, {yc}±{y}), ({xc}±{y}, {yc}±{x})\n")
                    
                    if y < x:
                        break
                    
                    x += 1
                    if d > 0:
                        y -= 1
                        d = d + 4 * (x - y) + 10
                        self.info_text.insert(tk.END, f"  d > 0: y--, d = d + 4*(x-y) + 10\n")
                    else:
                        d = d + 4 * x + 6
                        self.info_text.insert(tk.END, f"  d ≤ 0: d = d + 4*x + 6\n")
            
            self.info_text.insert(tk.END, f"\n{'='*40}\n")
            self.info_text.insert(tk.END, "Легенда:\n")
            self.info_text.insert(tk.END, "• Синие клетки - растеризованные точки\n")
            if algorithm != "bresenham_circle":
                self.info_text.insert(tk.END, "• Зеленая клетка - начальная точка\n")
                self.info_text.insert(tk.END, "• Красная клетка - конечная точка\n")
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверные параметры: {str(e)}\nВведите целые числа.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")


def main():
    """Главная функция запуска приложения"""
    root = tk.Tk()
    app = RasterVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
