import pygame
import random

# 游戏配置
TILE_SIZE = 80 #格子大小
N=10  #列数
M=20  #行数

WIDTH, HEIGHT = TILE_SIZE*N, TILE_SIZE*M+TILE_SIZE

COLS, ROWS = WIDTH // TILE_SIZE, (HEIGHT-TILE_SIZE) // TILE_SIZE

# 颜色定义
COLORS = [(102, 102, 255), (102, 255, 153), (255, 204, 102), (153, 102, 255)]
GRID = [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pop Star Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

steps =0
game_over = False  # 游戏结束标志

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = GRID[row][col]
            if color is not None:  # 只绘制有效颜色
                pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE+TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_steps():
    text = font.render(f"Steps: {steps}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

def draw_game_over(score):
    text = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
    restart_text = font.render("Click to Restart", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
 
def remove_connected_colors(row, col):
    global steps
    
    color = GRID[row][col]
    
    if(color!=None):
        steps = steps+1
    
    for c in range(COLS):
        if GRID[row][c]==color:
            GRID[row][c]=None
    
    # 垂直下落
    for col in range(COLS):
        empty_spots = 0
        for row in range(ROWS-1, -1, -1):
            if GRID[row][col] is None:
                empty_spots += 1
            elif empty_spots > 0:
                GRID[row + empty_spots][col] = GRID[row][col]
                GRID[row][col] = None

def is_game_over():
    for row in GRID:
        if any(color is not None for color in row):
            return False
    return True

def reset_game():
    global GRID, steps, game_over
    GRID = [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]
    steps = 0
    game_over = False
    
def main():
    global game_over
    running = True
    while running:
        screen.fill((255, 255, 255))
        
        if game_over:
            draw_game_over(steps)  # 绘制游戏结束信息
        else:
            draw_steps()  # 绘制步数
            draw_grid()
            if is_game_over():
                game_over = True  # 如果游戏结束，设置标志

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    reset_game()  # 点击重置游戏
                else:
                    mouse_x, mouse_y = event.pos
                    col = mouse_x // TILE_SIZE
                    row = (mouse_y - TILE_SIZE) // TILE_SIZE  # 调整y坐标

                    if row == ROWS-1 and 0 <= col < COLS:
                        remove_connected_colors(row, col)

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()