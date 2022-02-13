import pygame
import save
import os
from copy import deepcopy
import pyperclip as pc

WIDTH = int(1920 * 0.75)
HEIGHT = int(1080 * 0.75)
FPS = 60
TICK_SPEED = 2
GRID_WIDTH = 100
GRID_HEIGHT = 100
CAMERA_X = - WIDTH // 2
CAMERA_Y = - HEIGHT // 2


old_map = []
subticks = [[27], [26], [25], [24], [71], [70], [69], [68], [67], [66], [65], [64], [28, 29, 30, 31], [32, 33, 34, 35],
            [44, 45, 46, 47], [48, 49, 50, 51], [55],
            [54], [53], [52], [63, 62, 61, 60], [59, 57], [56, 58], [75, 73], [74, 72], [79, 78, 77, 76],
            [7], [6], [5], [4], [83], [82], [81], [80]]
brick_files = [os.path.join("img", f) for f in os.listdir("img/") if os.path.isfile(os.path.join("img", f))]
brick_surfaces = [pygame.transform.scale(pygame.image.load(f), (32, 32)) for f in brick_files]
brick_keymap = {1: [7, 55, 83], 2: [11, 15], 3: [19, 43], 4: [20], 5: [27, 67, 71], 6: [31, 35, 47, 51],
                7: [39], 8: [59, 63, 75, 79]}
pushed_pushers = []
pygame_keys_to_numbers = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5,
                          pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8}
for i in reversed(range(len(brick_surfaces))):
    for _ in range(3):
        brick_surfaces.insert(i, pygame.transform.rotate(brick_surfaces[i], 90))

# 0, 1, 2, 3 - BG
# 4 - Down Mover
# 5 - Left Mover
# 6 - Up Mover
# 7 - Right Mover
# 8, 9, 10, 11 - Push
# 12, 14 - Vertical Slide
# 13, 15 - Horizontal Slide
# 16, 17, 18, 19 - Immobile
# 20, 21, 22, 23 - Enemy
# 24 - Down Generator
# 25 - Left Generator
# 26 - Up Generator
# 27 - Right Generator
# 28, 29, 30, 31 - CC Spinner
# 32, 33, 34, 35 - C Spinner
# 36, 37, 38, 39 - Trash
non_updated_generators = []
world = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def draw_world():
    for y, row in enumerate(world):
        for x, tile in enumerate(row):
            img = brick_surfaces[tile]
            img_rect = img.get_rect()
            img_rect.x = (x * 32) - (CAMERA_X + WIDTH // 2)
            img_rect.y = (y * 32) - (CAMERA_Y + HEIGHT // 2)
            screen.blit(img, img_rect)


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyCell Machine")
clock = pygame.time.Clock()


def push_in_dir(map, x, y, dir_x=1, dir_y=0, depth=0):
    if map[y][x] in [0, 1, 2, 3]:
        return True, depth
    elif map[y][x] in [16, 17, 18, 19, 40, 41, 42, 43]:
        return False, depth
    elif map[y][x] in [20, 21, 22, 23]:
        return None, depth
    elif map[y][x] in [36, 37, 38, 39]:
        return None, depth
    elif len(map[0]) > x + dir_x >= 0 and len(map) > y + dir_y >= 0:
        if map[y][x] in [13, 15]:
            result = dir_y == 0 and push_in_dir(map, x + dir_x, y + dir_y, dir_x, dir_y)[0]
            if result is None:
                if map[y + dir_y][x + dir_x] in [36, 37, 38, 39]:
                    map[y][x] = 0
                else:
                    map[y + dir_y][x + dir_x] = 0
                    map[y][x] = 0
                return True, depth
            if result:
                map[y + dir_y][x + dir_x] = map[y][x]
                map[y][x] = 0
            return result, depth
        elif map[y][x] in [12, 14]:
            result = dir_x == 0 and push_in_dir(map, x + dir_x, y + dir_y, dir_x, dir_y)[0]
            if result is None:
                if map[y + dir_y][x + dir_x] in [36, 37, 38, 39]:
                    map[y][x] = 0
                else:
                    map[y + dir_y][x + dir_x] = 0
                    map[y][x] = 0
                return True, depth
            if result:
                map[y + dir_y][x + dir_x] = map[y][x]
                map[y][x] = 0
            return result, depth
        elif map[y][x] in [4, 5, 6, 7]:
            result, depth = push_in_dir(map, x + dir_x, y + dir_y, dir_x, dir_y, depth + 1)
            if result is None:
                if map[y + dir_y][x + dir_x] in [36, 37, 38, 39]:
                    map[y][x] = 0
                else:
                    map[y + dir_y][x + dir_x] = 0
                    map[y][x] = 0
                return True, depth
            if result:
                if depth > 1:
                    pushed_pushers.append((x + dir_x, y + dir_y))
                map[y + dir_y][x + dir_x] = map[y][x]
                map[y][x] = 0
            return result, depth
        elif map[y + dir_y][x + dir_x] != 0:
            result, depth = push_in_dir(map, x + dir_x, y + dir_y, dir_x, dir_y, depth + 1)
            if result is None:
                if map[y + dir_y][x + dir_x] in [36, 37, 38, 39]:
                    map[y][x] = 0
                else:
                    map[y + dir_y][x + dir_x] = 0
                    map[y][x] = 0
                return True, depth
            if result:
                map[y + dir_y][x + dir_x] = map[y][x]
                map[y][x] = 0
            return result, depth
        else:
            map[y + dir_y][x + dir_x] = map[y][x]
            map[y][x] = 0
            return True, depth
    return False, depth


def find_pull_seq(world, x, y, dir_x, dir_y):
    cur_x = x
    cur_y = y
    while 0 <= cur_x < len(row)-1 and 0 <= cur_y < len(world)-1:
        cur_tile = world[cur_y][cur_x]
        if cur_tile in [0, 1, 2, 3, 16, 17, 18, 19, 40, 41, 42, 43]:
            return cur_x, cur_y
        if cur_tile in [13, 15] and dir_y != 0:
            return cur_x, cur_y
        if cur_tile in [12, 14] and dir_x != 0:
            return cur_x, cur_y
        cur_x -= dir_x
        cur_y -= dir_y
    return cur_x, cur_y



def next_brush(current_brush, selection_set):
    if current_brush in brick_keymap[selection_set]:
        brush_set = brick_keymap[selection_set]
        return brush_set[(brush_set.index(current_brush) + 1) % len(brush_set)]
    else:
        return brick_keymap[selection_set][0]


running = True
simulation = False
next_tick_stop = False
tick_countdown = TICK_SPEED
all_sprites = pygame.sprite.Group()
brush = 8
while running:
    clock.tick(FPS)

    screen.fill((100, 100, 100))

    draw_world()
    out = deepcopy(world)

    if pygame.mouse.get_pressed()[0] and not simulation:
        mouse_pos = pygame.mouse.get_pos()
        coord_x = (mouse_pos[0] + (CAMERA_X + WIDTH // 2)) // 32
        coord_y = (mouse_pos[1] + (CAMERA_Y + HEIGHT // 2)) // 32
        try:
            if coord_y > -1 and coord_x > -1:
                out[coord_y][coord_x] = brush
        except IndexError:
            ...
    if pygame.mouse.get_pressed()[2] and not simulation:
        mouse_pos = pygame.mouse.get_pos()
        coord_x = (mouse_pos[0] + (CAMERA_X + WIDTH // 2)) // 32
        coord_y = (mouse_pos[1] + (CAMERA_Y + HEIGHT // 2)) // 32
        try:
            if coord_y > -1 and coord_x > -1:
                out[coord_y][coord_x] = 0
        except IndexError:
            ...

    if tick_countdown <= 0:
        if simulation:
            for tile_type in subticks:
                y = 0 if tile_type != [52] else len(world) - 1
                while (y < len(world)) if tile_type != [52] else (y > 0):
                    row = out[y]
                    x = 0 if tile_type != [55] else len(row) - 1
                    while (x < len(row)) if tile_type != [55] else (x > 0):
                        if (x, y) in pushed_pushers:
                            pushed_pushers.remove((x, y))
                            x += 1 if tile_type != [55] else -1
                            continue
                        if out[y][x] not in tile_type:
                            x += 1 if tile_type != [55] else -1
                            continue
                        tile = row[x]
                        if tile == 7:
                            result, depth = push_in_dir(out, x, y)
                            pushed_pushers.append((x + 1, y))
                        elif tile == 6:
                            result, depth = push_in_dir(out, x, y, 0, -1)
                        elif tile == 5:
                            result, depth = push_in_dir(out, x, y, -1, 0)
                        elif tile == 4:
                            result, depth = push_in_dir(out, x, y, 0, 1)
                            if result:
                                pushed_pushers.append((x, y + 1))

                        elif tile == 27:
                            if x + 1 < len(out[0]) and x - 1 >= 0:
                                if out[y][x - 1] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x + 1, y)
                                    if result:
                                        out[y][x + 1] = out[y][x - 1]
                                        x += 1 if tile_type != [55] else -1
                                        pushed_pushers.append((x + 1, y))
                                    elif result is None and out[y][x + 1] in [20, 21, 22, 23]:
                                        out[y][x + 1] = 0
                                    elif out[y][x - 1] == 0:
                                        non_updated_generators.append((x, y))
                        elif tile == 26:
                            if y + 1 < len(out[0]) and y - 1 >= 0:
                                if out[y + 1][x] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x, y - 1, 0, -1)
                                    if result:
                                        out[y - 1][x] = out[y + 1][x]
                                        pushed_pushers.append((x, y - 1))
                                    elif result is None and out[y - 1][x] in [20, 21, 22, 23]:
                                        out[y - 1][x] = 0
                                    elif out[y + 1][x] == 0:
                                        non_updated_generators.append((x, y))
                        elif tile == 25:
                            if x + 1 < len(out[0]) and x - 1 >= 0:
                                if out[y][x + 1] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x - 1, y, -1, 0)
                                    if result:
                                        out[y][x - 1] = out[y][x + 1]
                                        pushed_pushers.append((x - 1, y))
                                    elif result is None and out[y - 1][x] in [20, 21, 22, 23]:
                                        out[y][x - 1] = 0
                                    elif out[y][x + 1] == 0:
                                        non_updated_generators.append((x, y))
                        elif tile == 24:
                            if y + 1 < len(out[0]) and y - 1 >= 0:
                                if out[y - 1][x] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x, y + 1, 0, 1)
                                    if result:
                                        out[y + 1][x] = out[y - 1][x]
                                        pushed_pushers.append((x, y + 1))
                                    elif result is None and out[y - 1][x] in [20, 21, 22, 23]:
                                        out[y + 1][x] = 0
                                    if out[y - 1][x] == 0:
                                        non_updated_generators.append((x, y))
                        elif tile in [28, 29, 30, 31]:
                            for coord in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                x_off = coord[0]
                                y_off = coord[1]
                                if 0 < x + x_off < len(out[0]) and 0 < y + y_off < len(out):
                                    if out[y + y_off][x + x_off] != 0:
                                        base = out[y + y_off][x + x_off] - (out[y + y_off][x + x_off] % 4)
                                        out[y + y_off][x + x_off] = base + (out[y + y_off][x + x_off] - 1) % 4
                        elif tile in [32, 33, 34, 35]:
                            for coord in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                x_off = coord[0]
                                y_off = coord[1]
                                if 0 <= x + x_off < len(out[0]) and 0 <= y + y_off < len(out):
                                    if out[y + y_off][x + x_off] != 0:
                                        base = out[y + y_off][x + x_off] - (out[y + y_off][x + x_off] % 4)
                                        out[y + y_off][x + x_off] = base + (out[y + y_off][x + x_off] + 1) % 4
                        elif tile in [44, 45, 46, 47]:
                            for coord in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                x_off = coord[0]
                                y_off = coord[1]
                                if 0 <= x + x_off < len(out[0]) and 0 <= y + y_off < len(out):
                                    if out[y + y_off][x + x_off] != 0:
                                        base = out[y + y_off][x + x_off] - (out[y + y_off][x + x_off] % 4)
                                        out[y + y_off][x + x_off] = base + (out[y + y_off][x + x_off] + 2) % 4
                        elif tile in [48, 49, 50, 51]:
                            for coord in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                x_off = coord[0]
                                y_off = coord[1]
                                if 0 <= x + x_off < len(out[0]) and 0 <= y + y_off < len(out):
                                    if out[y + y_off][x + x_off] != 0:
                                        offset = tile - 48
                                        base = out[y + y_off][x + x_off] - (out[y + y_off][x + x_off] % 4)
                                        out[y + y_off][x + x_off] = base + offset
                        elif tile == 52:
                            try:
                                temp = out[y + 1][x]
                                if temp in [16, 17, 18, 19, 40, 41, 42, 43]:
                                    x += 1 if tile_type != [55] else -1
                                    continue
                                out[y + 1][x] = 52
                                out[y][x] = temp
                                if out[y + 1][x] != out[y][x]:
                                    pushed_pushers.append((x, y + 1))
                            except IndexError:
                                ...
                        elif tile == 53:
                            try:
                                temp = out[y][x - 1]
                                if temp in [16, 17, 18, 19, 40, 41, 42, 43] or x == 0:
                                    x += 1 if tile_type != [55] else -1
                                    continue
                                out[y][x - 1] = 53
                                out[y][x] = temp
                            except IndexError:
                                ...
                        elif tile == 54:
                            try:
                                temp = out[y - 1][x]
                                if temp in [16, 17, 18, 19, 40, 41, 42, 43] or y == 0:
                                    x += 1 if tile_type != [55] else -1
                                    continue
                                out[y - 1][x] = 54
                                out[y][x] = temp
                            except IndexError:
                                ...
                        elif tile == 55:
                            try:
                                temp = out[y][x + 1]
                                if temp in [16, 17, 18, 19, 40, 41, 42, 43]:
                                    x += 1 if tile_type != [55] else -1
                                    continue
                                out[y][x + 1] = 55
                                out[y][x] = temp
                                if out[y][x + 1] != out[y][x]:
                                    pushed_pushers.append((x + 1, y))
                            except IndexError:
                                ...
                        elif tile == 67:
                            if x + 1 < len(row):
                                if out[y][x + 1] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x + 1, y, 1, 0)
                                    if result:
                                        out[y][x + 1] = out[y][x + 2]
                                        if out[y][x + 1] == tile:
                                            x += 1
                                    elif result is None and out[y][x + 1] in [20, 21, 22, 23]:
                                        out[y][x + 1] = 0
                        elif tile == 66:
                            if y - 1 > 0:
                                if out[y - 1][x] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x, y - 1, 0, -1)
                                    if result:
                                        out[y - 1][x] = out[y - 2][x]
                                    elif result is None and out[y - 1][x] in [20, 21, 22, 23]:
                                        out[y - 1][x] = 0
                        elif tile == 65:
                            if x - 1 > 0:
                                if out[y][x - 1] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x - 1, y, -1, 0)
                                    if result:
                                        out[y][x - 1] = out[y][x - 2]
                                    elif result is None and out[y][x - 1] in [20, 21, 22, 23]:
                                        out[y][x - 1] = 0
                        elif tile == 71:
                            if y + 1 < len(out[0]) and y - 1 >= 0:
                                if out[y + 1][x] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x, y - 1, 0, -1)
                                    if result:
                                        out[y - 1][x] = out[y + 1][x]
                                        pushed_pushers.append((x, y - 1))
                                    elif result is None and out[y - 1][x] in [20, 21, 22, 23]:
                                        out[y - 1][x] = 0

                            if x + 1 < len(out[0]) and x - 1 >= 0:
                                if out[y][x - 1] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x + 1, y)
                                    if result:
                                        out[y][x + 1] = out[y][x - 1]
                                        pushed_pushers.append((x + 1, y))
                                    elif result is None and out[y][x + 1] in [20, 21, 22, 23]:
                                        out[y][x + 1] = 0
                        elif tile == 70:
                            if y + 1 < len(out[0]) and y - 1 >= 0:
                                if out[y + 1][x] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x, y - 1, 0, -1)
                                    if result:
                                        out[y - 1][x] = out[y + 1][x]
                                        pushed_pushers.append((x, y - 1))
                                    elif result is None and out[y - 1][x] in [20, 21, 22, 23]:
                                        out[y - 1][x] = 0

                            if x + 1 < len(out[0]) and x - 1 >= 0:
                                if out[y][x + 1] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x - 1, y, -1, 0)
                                    if result:
                                        out[y][x - 1] = out[y][x + 1]
                                        pushed_pushers.append((x + 1, y))
                                    elif result is None and out[y][x - 1] in [20, 21, 22, 23]:
                                        out[y][x - 1] = 0
                        elif tile == 69:
                            if y + 1 < len(out[0]) and y - 1 >= 0:
                                if out[y - 1][x] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x, y + 1, 0, 1)
                                    if result:
                                        out[y + 1][x] = out[y - 1][x]
                                        pushed_pushers.append((x, y + 1))
                                    elif result is None and out[y + 1][x] in [20, 21, 22, 23]:
                                        out[y + 1][x] = 0

                            if x + 1 < len(out[0]) and x - 1 >= 0:
                                if out[y][x + 1] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x - 1, y, -1, 0)
                                    if result:
                                        out[y][x - 1] = out[y][x + 1]
                                        pushed_pushers.append((x + 1, y))
                                    elif result is None and out[y][x - 1] in [20, 21, 22, 23]:
                                        out[y][x - 1] = 0
                        elif tile == 68:
                            if y + 1 < len(out[0]) and y - 1 >= 0:
                                if out[y - 1][x] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x, y + 1, 0, 1)
                                    if result:
                                        out[y + 1][x] = out[y - 1][x]
                                        pushed_pushers.append((x, y + 1))
                                    elif result is None and out[y + 1][x] in [20, 21, 22, 23]:
                                        out[y + 1][x] = 0

                            if x + 1 < len(out[0]) and x - 1 >= 0:
                                if out[y][x - 1] not in [0, 40, 41, 42, 43]:
                                    result, depth = push_in_dir(out, x + 1, y, 1, 0)
                                    if result:
                                        out[y][x + 1] = out[y][x - 1]
                                        pushed_pushers.append((x - 1, y))
                                    elif result is None and out[y][x + 1] in [20, 21, 22, 23]:
                                        out[y][x + 1] = 0
                        elif tile in [59, 57]:
                            if x == 0 or x == len(row) - 1:
                                x += 1
                                continue
                            temp_a = out[y][x - 1]
                            temp_b = out[y][x + 1]
                            if temp_b in [16, 17, 18, 19, 40, 41, 42, 43] or temp_a in [16, 17, 18, 19, 40, 41, 42, 43]:
                                x += 1
                                continue
                            out[y][x + 1] = temp_a
                            out[y][x - 1] = temp_b
                            if temp_a in [59, 57, 60, 61, 62, 63]:
                                pushed_pushers.append((x + 1, y))
                        elif tile in [56, 58]:
                            if y == 0 or y == len(world) - 1:
                                x += 1
                                continue
                            temp_a = out[y + 1][x]
                            temp_b = out[y - 1][x]
                            if temp_b in [16, 17, 18, 19, 40, 41, 42, 43] or temp_a in [16, 17, 18, 19, 40, 41, 42, 43]:
                                x += 1
                                continue
                            out[y + 1][x] = temp_b
                            out[y - 1][x] = temp_a
                            if temp_b in [56, 58, 60, 61, 62, 63]:
                                pushed_pushers.append((x, y + 1))
                        elif tile in [60, 61, 62, 63]:
                            if x != 0 and x != len(row) - 1:
                                temp_a = out[y][x - 1]
                                temp_b = out[y][x + 1]
                                if temp_b in [16, 17, 18, 19, 40, 41, 42, 43] or temp_a in [16, 17, 18, 19, 40, 41, 42,
                                                                                            43]:
                                    x += 1
                                    continue
                                out[y][x + 1] = temp_a
                                out[y][x - 1] = temp_b
                                if temp_a in [59, 57, 56, 58, 60, 61, 62, 63]:
                                    pushed_pushers.append((x + 1, y))
                            if y == 0 or y == len(world) - 1:
                                x += 1
                                continue
                            temp_a = out[y + 1][x]
                            temp_b = out[y - 1][x]
                            if temp_b in [16, 17, 18, 19, 40, 41, 42, 43] or temp_a in [16, 17, 18, 19, 40, 41, 42, 43]:
                                x += 1
                                continue
                            out[y + 1][x] = temp_b
                            out[y - 1][x] = temp_a
                            if temp_b in [59, 57, 56, 58, 60, 61, 62, 63]:
                                pushed_pushers.append((x, y + 1))
                        elif tile in [75, 73]:
                            if y == 0 or y == len(world) - 1 or x == 0 or x == len(row) - 1:
                                x += 1
                                continue
                            temp_a = out[y + 1][x - 1]
                            temp_b = out[y - 1][x + 1]
                            if temp_b in [16, 17, 18, 19, 40, 41, 42, 43] or temp_a in [16, 17, 18, 19, 40, 41, 42,
                                                                                        43]:
                                x += 1
                                continue
                            out[y + 1][x - 1] = temp_b
                            out[y - 1][x + 1] = temp_a
                            if temp_b in [75, 73]:
                                pushed_pushers.append((x - 1, y + 1))
                        elif tile in [74, 72]:
                            if y == 0 or y == len(world) - 1 or x == 0 or x == len(row) - 1:
                                x += 1
                                continue
                            temp_a = out[y - 1][x - 1]
                            temp_b = out[y + 1][x + 1]
                            if temp_b in [16, 17, 18, 19, 40, 41, 42, 43] or temp_a in [16, 17, 18, 19, 40, 41, 42,
                                                                                        43]:
                                x += 1
                                continue
                            out[y - 1][x - 1] = temp_b
                            out[y + 1][x + 1] = temp_a
                            if temp_a in [74, 72]:
                                pushed_pushers.append((x + 1, y + 1))
                        elif tile == 79:
                            if y == len(world) - 1 or x == len(row) - 1:
                                x += 1
                                continue
                            temp_a = out[y + 1][x]
                            temp_a_base = temp_a - temp_a % 4
                            temp_b = out[y][x + 1]
                            temp_b_base = temp_b - temp_b % 4
                            if temp_b in [16, 17, 18, 19, 40, 41, 42, 43] or temp_a in [16, 17, 18, 19, 40, 41,
                                                                                           42, 43]:
                                x += 1
                                continue
                            if temp_a == temp_b == 0:
                                x += 1
                                continue
                            out[y + 1][x] = temp_b_base + (temp_b + 1) % 4
                            out[y][x + 1] = temp_a_base + (temp_a + 3) % 4
                            if temp_a in [74, 72]:
                                pushed_pushers.append((x + 1, y + 1))
                        elif tile == 78:
                            if y == len(world) - 1 or y == 0 or x == len(row) - 1:
                                x += 1
                                continue
                            temp_a = out[y - 1][x]
                            temp_a_base = temp_a - temp_a % 4
                            temp_b = out[y][x + 1]
                            temp_b_base = temp_b - temp_b % 4
                            if temp_b in [16, 17, 18, 19, 40, 41, 42, 43] or temp_a in [16, 17, 18, 19, 40, 41,
                                                                                           42, 43]:
                                x += 1
                                continue
                            if temp_a == temp_b == 0:
                                x += 1
                                continue
                            out[y - 1][x] = temp_b_base + (temp_b + 1) % 4
                            out[y][x + 1] = temp_a_base + (temp_a + 3) % 4
                            if temp_a in [74, 72]:
                                pushed_pushers.append((x + 1, y - 1))
                        elif tile == 77:
                            if y == len(world) - 1 or x == len(row) - 1 or y == 0 or x ==0:
                                x += 1
                                continue

                            temp_a = out[y - 1][x]
                            temp_a_base = temp_a - temp_a % 4
                            temp_b = out[y][x - 1]
                            temp_b_base = temp_b - temp_b % 4
                            if temp_b in [16, 17, 18, 19, 40, 41, 42, 43] or temp_a in [16, 17, 18, 19, 40, 41,
                                                                                           42, 43]:
                                x += 1
                                continue
                            if temp_a == temp_b == 0:
                                x += 1
                                continue
                            out[y - 1][x] = temp_b_base + (temp_b + 1) % 4
                            out[y][x - 1] = temp_a_base + (temp_a + 3) % 4
                            if temp_a in [74, 72]:
                                pushed_pushers.append((x - 1, y - 1))
                        elif tile == 76:
                            if y == len(world) - 1 or x == len(row) - 1 or x == 0:
                                x += 1
                                continue

                            temp_a = out[y + 1][x]
                            temp_a_base = temp_a - temp_a % 4
                            temp_b = out[y][x - 1]
                            temp_b_base = temp_b - temp_b % 4
                            if temp_b in [16, 17, 18, 19, 40, 41, 42, 43] or temp_a in [16, 17, 18, 19, 40, 41,
                                                                                           42, 43]:
                                x += 1
                                continue
                            if temp_a == temp_b == 0:
                                x += 1
                                continue
                            out[y + 1][x] = temp_b_base + (temp_b + 1) % 4
                            out[y][x - 1] = temp_a_base + (temp_a + 3) % 4
                            if temp_a in [74, 72]:
                                pushed_pushers.append((x - 1, y + 1))
                        elif tile == 83:
                            if 0 <= x < len(row):
                                if row[x + 1] != 0:
                                    x += 1
                                    continue
                                point_x, point_y = find_pull_seq(out, x, y, 1, 0)
                                push_in_dir(out, point_x+1, point_y)
                                pushed_pushers.append((x+1, y))
                        elif tile == 82:
                            if 0 < y < len(world):
                                if out[y - 1][x] != 0:
                                    x += 1
                                    continue
                                point_x, point_y = find_pull_seq(out, x, y, 0, -1)
                                push_in_dir(out, point_x, point_y-1, 0, -1)
                        elif tile == 81:
                            if 0 <= x < len(row):
                                if row[x - 1] != 0:
                                    x += 1
                                    continue
                                point_x, point_y = find_pull_seq(out, x, y, -1, 0)
                                push_in_dir(out, point_x-1, point_y, -1, 0)
                        elif tile == 80:
                            if 0 < y < len(world) - 1:
                                if out[y + 1][x] != 0:
                                    x += 1
                                    continue
                                point_x, point_y = find_pull_seq(out, x, y, 0, 1)
                                push_in_dir(out, point_x, point_y + 1, 0, 1)
                                pushed_pushers.append((x, y + 1))
                        try:
                            world[y] = row = out[y][:]
                            if y + 1 < len(world):
                                world[y + 1] = out[y + 1][:]
                            world[y - 1] = out[y - 1][:]
                        except IndexError:
                            ...
                        x += 1 if tile_type != [55] else -1
                    y += 1 if tile_type != [52] else -1
        tick_countdown = TICK_SPEED
    else:
        tick_countdown -= 1

    if next_tick_stop:
        simulation = False
        next_tick_stop = False
    world = deepcopy(out)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(save.full_LZ77_compress(world))
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if simulation:
                    world = old_map[:]
                    old_map = []
                else:
                    old_map = world[:]
                simulation = not simulation
            elif event.key == pygame.K_d:
                if not simulation:
                    next_tick_stop = True
                    tick_countdown = 0
                    simulation = True
                    if not old_map:
                        old_map = world[:]
            elif event.key == pygame.K_r:
                if old_map:
                    world = old_map[:]
            elif event.key == pygame.K_s:
                pc.copy(save.full_LZ77_compress(world))
            elif event.key == pygame.K_l:
                try:
                    world = save.full_LZ77_decompress(pc.paste())
                except:
                    ...
            elif event.key == pygame.K_e:
                world = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
            elif event.key in pygame_keys_to_numbers.keys():
                brush = next_brush(brush, pygame_keys_to_numbers[event.key])
            elif event.key == pygame.K_z:
                base = brush - (brush % 4)
                brush = base + (brush + 3) % 4
            elif event.key == pygame.K_c:
                base = brush - (brush % 4)
                brush = base + (brush + 1) % 4
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        CAMERA_X -= 10
    elif keys[pygame.K_RIGHT]:
        CAMERA_X += 10
    if keys[pygame.K_UP]:
        CAMERA_Y -= 10
    elif keys[pygame.K_DOWN]:
        CAMERA_Y += 10
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
