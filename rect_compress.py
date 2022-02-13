from save import num_to_chr, chr_to_num, full_LZ77_compress, allowed_letters, LZ77_compress, next_letters, letters
import math

tiles = list(range(4, 44))
world = [[12, 13, 14, 15, 12, 13, 14, 15, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [13, 12, 13, 13, 13, 13, 13, 12, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [12, 13, 13, 13, 12, 13, 13, 13, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [13, 12, 12, 23, 23, 23, 12, 12, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [12, 13, 13, 23, 23, 23, 13, 13, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [13, 12, 12, 23, 23, 23, 14, 14, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [12, 13, 13, 13, 12, 13, 13, 13, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [13, 12, 13, 13, 13, 13, 13, 12, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [12, 13, 12, 13, 12, 13, 12, 13, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def rectangle_make(map):
    extra_data = (len(map), len(map[0]))
    output = []
    width = 0
    for tile_type in tiles:
        y = 0
        while y < len(map):
            if width != 0:
                cur_y = y
                while cur_y < len(map):
                    try:
                        cur_w = get_width_of_line(map, x - width, cur_y, tile_type)
                    except IndexError:
                        cur_w = 0
                    if cur_w < width:
                        break
                    cur_y += 1
                output.append((x - width, y - 1, width, cur_y - (y - 1), tile_type))
                width = 0
            x = 0
            row = map[y]
            while x < len(row):
                skip = False
                for i, rect in enumerate(output):
                    last_rect = most_recent_of_length(output, i, 5)
                    if len(rect) == 5 or len(rect) == 4:
                        start_x = rect[0]
                        start_y = rect[1]
                        end_x = rect[0] + rect[2]
                        end_y = rect[1] + rect[3]
                    elif len(rect) == 3:
                        start_x = rect[0]
                        start_y = rect[1]
                        end_x = rect[0] + rect[2]
                        end_y = rect[1] + last_rect[3]
                    elif len(rect) == 2:
                        start_x = rect[0]
                        start_y = rect[1]
                        end_x = rect[0] + last_rect[2]
                        end_y = rect[1] + last_rect[3]
                    elif len(rect) == 1:
                        start_x = rect[0]
                        start_y = last_rect[1]
                        end_x = rect[0] + last_rect[2]
                        end_y = last_rect[1] + last_rect[2]

                    if start_x <= x < end_x:
                        if start_y <= y < end_y:
                            if width == 0:
                                skip = True
                                break
                if skip:
                    x += 1
                    continue
                tile = row[x]
                if tile == tile_type:
                    width += 1
                    x += 1
                    continue
                elif width != 0:
                    cur_y = y + 1
                    while cur_y < len(map):
                        try:
                            cur_w = get_width_of_line(map, x - width, cur_y, tile_type)
                        except IndexError:
                            cur_w = 0
                        if cur_w < width:
                            break
                        cur_y += 1
                    if len(output) == 0:
                        output.append(((x - width) + 1, y+1, width, cur_y - y, tile_type))
                    else:
                        last = most_recent_of_length(output, len(output)-1, 5)
                        if last[4] != tile_type:
                            output.append(((x - width) + 1, y+1, width, cur_y - y, tile_type))
                        else:
                            if last[3] != cur_y - y:
                                output.append(((x - width) + 1, y+1, width, cur_y - y))
                            else:
                                if last[2] != width:
                                    output.append(((x - width) + 1, y+1, width))
                                else:
                                    if last[1] != y:
                                        output.append(((x - width) + 1, y+1))
                                    else:
                                        if last[0] != x:
                                            output.append(((x - width) + 1, ))
                                        else:
                                            output.append(tuple())
                    width = 0
                x += 1
            y += 1
    output.insert(0, extra_data)
    return output


def make_map_from_rectangle(compressed):
    decompressed = []
    last_full = []
    for rect in compressed:
        final_rect = [0, 0, 0, 0, 0]
        if len(rect) == 2:
            if not decompressed:
                decompressed = [[0 for _ in range(rect[1])] for _ in range(rect[0])]
                continue
        if len(rect) == 5:
            last_full = rect[:]
            final_rect = rect[:]
        if len(rect) == 4:
            final_rect[0] = rect[0]
            final_rect[1] = rect[1]
            final_rect[2] = rect[2]
            final_rect[3] = rect[3]
            final_rect[4] = last_full[4]
        if len(rect) == 3:
            final_rect[0] = rect[0]
            final_rect[1] = rect[1]
            final_rect[2] = rect[2]
            final_rect[3] = last_full[3]
            final_rect[4] = last_full[4]
        if len(rect) == 2:
            final_rect[0] = rect[0]
            final_rect[1] = rect[1]
            final_rect[2] = last_full[2]
            final_rect[3] = last_full[3]
            final_rect[4] = last_full[4]
        if len(rect) == 1:
            final_rect[0] = rect[0]
            final_rect[1] = last_full[1]
            final_rect[2] = last_full[2]
            final_rect[3] = last_full[3]
            final_rect[4] = last_full[4]
        fill_with_rect(final_rect, decompressed, final_rect[4])
    return decompressed


def most_recent_of_length(arr, i, length):
    while i >= 0:
        if len(arr[i]) == length:
            return arr[i]
        i -= 1
    return []


def fill_with_rect(rect, map, tile):
    start_x = rect[0]-1
    start_y = rect[1]-1
    end_x = start_x + rect[2]
    end_y = start_y + rect[3]
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            map[y][x] = tile


def get_width_of_line(world, x, y, tile):
    cur_x = x
    while cur_x < len(world[y]):
        if world[y][cur_x] != tile:
            return cur_x - x
        cur_x += 1
    return cur_x - x


def full_rect_compress(world):
    out = ""
    width, height = 0, 0
    for rect in rectangle_make(world):
        final_rect = [0, 0, 0, 0, 0]
        if len(rect) == 2:
            if width == 0:
                width = rect[1]
                height = rect[0]
                base = max(width, height, 44) + 1
                width_chr = num_to_chr(rect[0])
                width_chars = list(width_chr)
                width_chars[-1] = next_letters[letters.index(width_chars[-1])]
                height_chr = num_to_chr(rect[1])
                height_chars = list(height_chr)
                height_chars[-1] = next_letters[letters.index(height_chars[-1])]
                out += "".join(width_chars) + "".join(height_chars)
                continue
        if len(rect) == 5:
            final_rect = rect[:]
        if len(rect) == 4:
            final_rect[0] = rect[0]
            final_rect[1] = rect[1]
            final_rect[2] = rect[2]
            final_rect[3] = rect[3]
            final_rect[4] = 0
        if len(rect) == 3:
            final_rect[0] = rect[0]
            final_rect[1] = rect[1]
            final_rect[2] = rect[2]
            final_rect[3] = 0
            final_rect[4] = 0
        if len(rect) == 2:
            final_rect[0] = rect[0]
            final_rect[1] = rect[1]
            final_rect[2] = 0
            final_rect[3] = 0
            final_rect[4] = 0
        if len(rect) == 1:
            final_rect[0] = rect[0]
            final_rect[1] = 0
            final_rect[2] = 0
            final_rect[3] = 0
            final_rect[4] = 0

        chars = num_to_chr(final_rect[0] + final_rect[1]*base + final_rect[2]*(base**2) + final_rect[3]*(base**3)
                           + final_rect[4]*(base**4))
        print(chr_to_num(chars))
        chars = list(chars)
        chars[-1] = next_letters[letters.index(chars[-1])]
        out += "".join(chars)
    return out


def full_rect_decompress(code):
    current_run = ""
    width = height = 0
    decompressed = []
    for char in code:
        current_run += char
        if char in next_letters:
            if current_run != "":
                current_chars = list(current_run)
                current_chars[-1] = letters[next_letters.index(current_chars[-1])]
                num = chr_to_num("".join(current_chars))
                if height == 0:
                    height = num
                elif width == 0:
                    width = num
                    base = max(width, height, 44) + 1
                else:
                    rect_fetched = []
                    cur_num = num
                    cur_base = 4
                    while cur_base >= 0:
                        if cur_num//(base**cur_base) != 0:
                            rect_fetched.insert(0, cur_num//(base**cur_base))
                        cur_num %= (base**cur_base)
                        cur_base -= 1
                    decompressed.append(rect_fetched)
                current_run = ""
    decompressed.insert(0, (height, width))
    return make_map_from_rectangle(decompressed)

# print(make_map_from_rectangle(rectangle_make(world)))
# rects = rectangle_make(world)
# print(make_map_from_rectangle(rects) == world)


print(full_rect_decompress("倮偂൩壠偈偌倜傢傦傪僓戙儀儱兞兢兦冔冼冾净凂๝垢ȃ薷倕狺檆僑僙儂扈儯Ǿ肀歆再粴ད噤偊扷၅唦偋៪捻ǹ煤")\
      == world)
# print(full_rect_compress(world))