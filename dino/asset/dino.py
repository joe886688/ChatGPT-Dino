import pygame
import random
import sys
import random  # 添加随机模块


# 初始化 Pygame
pygame.init()

# 屏幕设置
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_HEIGHT = 300

# 创建屏幕和时钟
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Google Dino Game with Animations")
clock = pygame.time.Clock()

# 加载恐龙动画帧图片（按需替换为自己的图片）
dino_run_images = [
    pygame.image.load("image/DinoMove1.jpg"),  # TODO: 替换为奔跑图片1
    pygame.image.load("image/DinoMove2.jpg"),  # TODO: 替换为奔跑图片2
]
dino_run_images = [pygame.transform.scale(img, (50, 50)) for img in dino_run_images]  # 调整大小

# 加载跳跃图片
dino_jump_image = pygame.image.load("image/DinoDrump.jpg")  # TODO: 替换为跳跃图片
dino_jump_image = pygame.transform.scale(dino_jump_image, (50, 50))  # 调整大小

# 加载障碍物图片
obstacle_images = [
    pygame.image.load("image/obstacle1.jpg"),  # TODO: 替换为障碍物图片1
    pygame.image.load("image/obstacle2.jpg"),  # TODO: 替换为障碍物图片2
    pygame.image.load("image/obstacle3.jpg"),  # TODO: 替换为障碍物图片3
]
# 可选：调整障碍物图片大小（按需修改尺寸）
obstacle_images = [pygame.transform.scale(img, (35, 35)) for img in obstacle_images]

# 加载背景图片
background_img = pygame.image.load("image/Background.jpg")  # TODO: 替换为背景图片路径
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 字体设置
font = pygame.font.Font(None, 36)  # 使用 Pygame 默认字体，字号 36

# 恐龙类
class Dino:
    def __init__(self):
        self.x = 50
        self.y = GROUND_HEIGHT - 50
        self.width = 50
        self.height = 50
        self.jump = False
        self.jump_speed = 22
        self.gravity = 1.6
        self.velocity = 0
        self.jump_count = 0  # 当前跳跃次数
        self.MAX_JUMPS = 2  # 最大跳跃次数
        self.frame = 0  # 动画帧索引
        self.animation_timer = 0  # 动画计时器

    def update(self):
        # 跳跃逻辑
        if self.jump:
            self.velocity -= self.gravity
            self.y -= self.velocity
            if self.y >= GROUND_HEIGHT - self.height:
                self.y = GROUND_HEIGHT - self.height
                self.jump = False
                self.velocity = 0
                self.jump_count = 0  # 恢复跳跃次数
        else:
            # 奔跑动画：切换帧
            self.animation_timer += 1
            if self.animation_timer % 3 == 0:  # 每 10 帧切换一次图片
                self.frame = (self.frame + 1) % len(dino_run_images)

    def draw(self):
        # 绘制恐龙
        if self.jump:
            screen.blit(dino_jump_image, (self.x, self.y))
        else:
            screen.blit(dino_run_images[self.frame], (self.x, self.y))

    def handle_jump(self):
        if self.jump_count < self.MAX_JUMPS:  # 判断是否还能跳跃
            self.jump = True
            self.velocity = self.jump_speed
            self.jump_count += 1  # 增加跳跃次数
# 障碍物类
class Obstacle:
    def __init__(self, x, speed):
        self.x = x
        self.speed = speed
        self.original_image = pygame.image.load(random.choice([
            "image/obstacle1.jpg", 
            "image/obstacle2.jpg", 
            "image/obstacle3.jpg"
        ]))  # 随机选择图片
        self.image = self.scale_image(self.original_image)  # 等比例缩放
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.y = GROUND_HEIGHT - self.height  # 根据图片高度调整位置

    def scale_image(self, image):
        # 原始宽度和高度
        original_width, original_height = image.get_size()
        # 随机选择一个新高度，宽度根据比例计算
        new_height = random.randint(30, 55)
        aspect_ratio = original_width / original_height  # 计算宽高比
        new_width = int(new_height * aspect_ratio)  # 等比例计算新宽度
        # 返回缩放后的图片
        return pygame.transform.scale(image, (new_width, new_height))

    def update(self):
        self.x -= self.speed
        if self.x + self.width < 0:
            # 循环回到屏幕外并重新生成随机属性
            self.x = SCREEN_WIDTH + random.randint(100, 300)
            self.image = self.scale_image(self.original_image)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.y = GROUND_HEIGHT - self.height

    def draw(self):
        # 绘制图片
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        # 获取矩形区域，用于碰撞检测
        return pygame.Rect(self.x, self.y, self.width, self.height)

# 主游戏函数
def main():
    # 初始化恐龙和障碍物
    dino = Dino()
    obstacles = [Obstacle(SCREEN_WIDTH + i * 300, speed=7) for i in range(3)]
    running = True
    game_active = True  # 游戏状态：True 表示游戏进行中，False 表示游戏结束
    score = 0
    speed_increment_timer = 0

    while running:
        screen.blit(background_img, (0, 0))  # 绘制背景图片

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 按下 ESC 键退出游戏
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # 如果游戏结束，按下空格或上方向键重启
            if event.type == pygame.KEYDOWN:
                if not game_active and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    main()  # 重新调用 main 函数
                    return  # 退出当前循环，防止叠加
                elif game_active and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    dino.handle_jump()

        if game_active:
            # 游戏更新逻辑
            dino.update()
            for obstacle in obstacles:
                obstacle.update()

                # 碰撞检测
                if pygame.Rect(dino.x, dino.y, dino.width, dino.height).colliderect(obstacle.get_rect()):
                    game_active = False  # 游戏结束

            # 更新得分
            score += 1
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))  # 绘制得分在屏幕左上角

            # 绘制地面
            pygame.draw.line(screen, BLACK, (0, GROUND_HEIGHT), (SCREEN_WIDTH, GROUND_HEIGHT), 2)

            # 绘制角色和障碍物
            dino.draw()
            for obstacle in obstacles:
                obstacle.draw()

            # 增加障碍物速度
            speed_increment_timer += 1
            if speed_increment_timer % 300 == 0:  # 每隔 300 帧（大约 10 秒）
                for obstacle in obstacles:
                    if obstacle.speed < 40:  # 最大速度为 10
                        obstacle.speed += 1  # 每个障碍物速度加快 3
        else:
            # 游戏结束界面
            pygame.time.wait(500)  # 等待 500 毫秒（0.5 秒）
            game_over_text = font.render("Game Over! Press Space or Up to Restart", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 80))
            final_score_text = font.render(f"Final Score: {score}", True, BLACK)
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))


        # 更新屏幕
        pygame.display.flip()
        clock.tick(30)  # 限制帧率为 30 FPS

# 启动游戏
if __name__ == "__main__":
    main()
