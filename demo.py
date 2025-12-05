import pygame
import random
from enum import Enum

# 定义方向枚举类，包含四个方向及其对应的坐标变化值
class Direction(Enum):
    UP = (0, -1)      # 上方向：x坐标不变，y坐标减1
    DOWN = (0, 1)     # 下方向：x坐标不变，y坐标加1
    LEFT = (-1, 0)    # 左方向：x坐标减1，y坐标不变
    RIGHT = (1, 0)    # 右方向：x坐标加1，y坐标不变

# 贪吃蛇游戏主类
class SnakeGame:
    # 初始化方法，设置游戏窗口大小、网格大小等参数
    def __init__(self, width=640, height=480, grid_size=20):
        pygame.init()                           # 初始化pygame库
        self.width = width                      # 设置游戏窗口宽度
        self.height = height                    # 设置游戏窗口高度
        self.grid_size = grid_size              # 设置每个网格的像素大小
        self.screen = pygame.display.set_mode((width, height))  # 创建游戏窗口
        pygame.display.set_caption("贪吃蛇")    # 设置窗口标题
        self.clock = pygame.time.Clock()        # 创建时钟对象控制游戏帧率
        self.reset()                            # 初始化游戏状态
    
    # 重置游戏状态到初始状态
    def reset(self):
        # 初始化蛇的位置在屏幕中央（以网格为单位）
        self.snake = [(self.width // (2 * self.grid_size), self.height // (2 * self.grid_size))]
        self.direction = Direction.RIGHT        # 初始方向向右
        self.next_direction = Direction.RIGHT   # 下一步方向也向右
        self.food = self.spawn_food()           # 生成第一个食物
        self.score = 0                          # 初始分数为0
    
    # 在随机位置生成一个新的食物
    def spawn_food(self):
        while True:
            # 随机生成食物的x和y坐标（以网格为单位）
            x = random.randint(0, (self.width // self.grid_size) - 1)
            y = random.randint(0, (self.height // self.grid_size) - 1)
            # 确保食物不会出现在蛇的身体上
            if (x, y) not in self.snake:
                return (x, y)
    
    # 处理游戏事件（如键盘输入、退出事件）
    def handle_events(self):
        # 遍历所有待处理的事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # 如果是退出事件
                return False                    # 返回False表示游戏结束
            if event.type == pygame.KEYDOWN:    # 如果是按键按下事件
                # 根据按下的键更新蛇的移动方向，防止反向移动
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
        return True                             # 返回True表示游戏继续
    
    # 更新游戏状态（移动蛇、检查碰撞等）
    def update(self):
        self.direction = self.next_direction    # 更新当前移动方向
        dx, dy = self.direction.value           # 获取x和y方向上的移动增量
        head_x, head_y = self.snake[0]          # 获取蛇头当前位置
        new_head = (head_x + dx, head_y + dy)   # 计算新的蛇头位置
        
        # 检查是否发生碰撞（撞墙或撞到自己）
        if (new_head[0] < 0 or new_head[0] >= self.width // self.grid_size or
            new_head[1] < 0 or new_head[1] >= self.height // self.grid_size or
            new_head in self.snake):
            return False                        # 发生碰撞，返回False表示游戏结束
        
        self.snake.insert(0, new_head)          # 将新头部插入到蛇身前端
        
        # 检查蛇是否吃到食物
        if new_head == self.food:
            self.score += 10                    # 吃到食物得分加10
            self.food = self.spawn_food()       # 生成新的食物
        else:
            self.snake.pop()                    # 没吃到食物则移除尾部，保持蛇身长度
        
        return True                             # 游戏继续进行，返回True
    
    # 绘制游戏画面
    def draw(self):
        self.screen.fill((0, 0, 0))             # 用黑色填充整个屏幕
        
        # 绘制蛇身的每一节
        for segment in self.snake:
            # 创建矩形对象表示蛇的一节
            rect = pygame.Rect(segment[0] * self.grid_size, segment[1] * self.grid_size, 
                             self.grid_size - 1, self.grid_size - 1)
            pygame.draw.rect(self.screen, (0, 255, 0), rect)  # 用绿色绘制蛇身
        
        # 绘制食物
        rect = pygame.Rect(self.food[0] * self.grid_size, self.food[1] * self.grid_size,
                          self.grid_size - 1, self.grid_size - 1)
        pygame.draw.rect(self.screen, (255, 0, 0), rect)      # 用红色绘制食物
        
        pygame.display.flip()                   # 更新显示内容
    
    # 运行游戏主循环
    def run(self):
        running = True                          # 游戏运行标志
        while running:                          # 游戏主循环
            running = self.handle_events()      # 处理游戏事件
            if not self.update():               # 更新游戏状态
                print(f"游戏结束！得分: {self.score}")  # 游戏结束时打印最终得分
                break                           # 跳出游戏循环
            self.draw()                         # 绘制游戏画面
            self.clock.tick(10)                 # 控制游戏帧率为每秒10帧
        pygame.quit()                           # 退出pygame

# 程序入口点
if __name__ == "__main__":
    game = SnakeGame()                      # 创建游戏实例
    game.run()                              # 运行游戏