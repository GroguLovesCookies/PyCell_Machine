allowed_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,./'[]-=<>?:\"{}_+)(*&^%$#@!)\001\002\003" \
                  "\004\005"
letters = ""
next_letters = ""

for i in range(500, 20500):
    letters += chr(i)
for i in range(20500, 40500):
    next_letters += chr(i)


def warp_row(row, width, map):
    item_num = 0
    cur_row = []
    for item in row:
        if item_num >= width:
            map.append(cur_row[:])
            item_num = 0
            cur_row = []
        cur_row.append(item)
        item_num += 1
    map.append(cur_row[:])


def full_LZ77_compress(world):
    string = num_to_chr(len(world[0])) + ";"
    new_part = ""
    for row in world:
        for tile in row:
            new_part += allowed_letters[tile]
    return string + LZ77_compress(new_part)


def full_LZ77_decompress(code):
    row = []
    map = []
    width = chr_to_num(code.split(";")[0])
    code_part = code.split(";")[1]
    decompressed = LZMA_decompress(code_part)
    for char in decompressed:
        row.append(allowed_letters.index(char))
    warp_row(row, width, map)
    return map


def compress(world):
    width = len(world[0])
    string = num_to_chr(width) + ";"
    prev_tile = -1
    run_length = -1
    for row in world:
        for tile in row:
            run_length += 1
            if prev_tile != -1 and prev_tile != tile:
                if run_length == 1:
                    string += allowed_letters[prev_tile]
                else:
                    string += allowed_letters[prev_tile] + num_to_chr(run_length)
                run_length = 0
            prev_tile = tile
    if run_length == 1:
        string += allowed_letters[prev_tile]
    else:
        string += allowed_letters[prev_tile] + num_to_chr(run_length)

    return string


def decompress(code):
    map = []
    row = []
    current_tile = ""
    width = chr_to_num(code.split(";")[0])
    current_chr_run = ""
    expected = True
    for char in code.split(";")[1]:
        if char in allowed_letters:
            if expected:
                if current_chr_run != "":
                    current_run = chr_to_num(current_chr_run)
                    for _ in range(current_run):
                        row.append(allowed_letters.index(current_tile))
                    current_chr_run = ""
                current_tile = char
                expected = False
            else:
                current_run = 1
                for _ in range(current_run):
                    row.append(allowed_letters.index(current_tile))
                current_chr_run = ""
                current_tile = char
                expected = False
        else:
            current_chr_run += char
            expected = True
    if expected:
        if current_chr_run != "":
            current_run = chr_to_num(current_chr_run)
            for _ in range(current_run):
                row.append(allowed_letters.index(current_tile))
    else:
        current_run = 1
        for _ in range(current_run):
            row.append(allowed_letters.index(current_tile))
    warp_row(row, width, map)
    return map


def LZ77_compress(expanded):
    patterns = []
    encoded = ""
    i = 0
    last_pattern_start = -1
    last_pattern_length = -1
    just_skipped_start = False
    prev_skipped_start = False
    while i < len(expanded):
        letter = expanded[i]
        if letter in patterns:
            j = expanded.index(letter)
            original_j = j
            original = i
            full = ""
            while expanded[i] == expanded[j] and j < original and len(full) < len(letters)//2:
                full += expanded[i]
                if i < len(expanded)-1:
                    i += 1
                    j += 1
                else:
                    break
            if i < len(expanded)-1:
                i -= 1
            if last_pattern_start == original_j:
                append = letters[:len(letters)//2][len(full)-1]
                just_skipped_start = True
            elif last_pattern_length == len(full) and not just_skipped_start:
                append = letters[len(letters)//2:][original_j]
            elif original_j < len(letters)//2:
                append = letters[:len(letters)//2][len(full)-1]+letters[len(letters)//2:][original_j]
            else:
                append = letter
                i = original
            if len(append) > len(full):
                i = original
                append = letter
                just_skipped_start = False
            encoded += append
            if append != letter:
                last_pattern_start = original_j
                last_pattern_length = len(full)
        else:
            patterns.append(letter)
            encoded += letter
        if just_skipped_start and prev_skipped_start == just_skipped_start:
            just_skipped_start = False
        prev_skipped_start = just_skipped_start
        i += 1
    if encoded[-1] == "_":
        listed = list(encoded)
        del listed[-1]
        encoded = "".join(listed)
    return encoded


def LZMA_decompress(compressed):
    expanded = ""
    i = 0
    read_state = -1
    pattern_start = -1
    pattern_length = -1
    prev_pattern_start = -1
    prev_pattern_length = -1
    while i < len(compressed):
        if i == len(compressed) and read_state >= 0:
            i -= 1
            read_state = -1
        letter = compressed[i]
        if letter == "_":
            pass
        if letter in allowed_letters:
            if read_state < 0:
                expanded += letter
            else:
                pattern_start = prev_pattern_start
                i -= 1
                read_state = -1

        elif letter.isnumeric():
            if read_state == -1:
                string_length = ""
                while letter.isnumeric():
                    string_length += letter
                    if i < len(compressed) - 1:
                        i += 1
                        letter = compressed[i]
                    else:
                        break
                if i < len(compressed) - 1:
                    i -= 1
                pattern_length = int(string_length)
                read_state += 1
            else:
                string_index = ""
                while letter.isnumeric():
                    string_index += letter
                    if i < len(compressed) - 1:
                        i += 1
                        letter = compressed[i]
                    else:
                        break
                    if i < len(compressed) - 1:
                        i -= 1
                    read_state = -1
                    pattern_start = int(string_index)
        elif not letter.isspace():
                if letter in letters[:len(letters)//2]:
                    if read_state == -1:
                        pattern_length = letters[:len(letters)//2].index(letter) + 1
                        read_state = 1
                    else:
                        pattern_start = prev_pattern_start
                        i -= 1
                        read_state = -1
                else:
                    pattern_start = letters[len(letters)//2:].index(letter)
                    if read_state == -1:
                        pattern_length = prev_pattern_length
                    read_state = -1
        if pattern_length >= 0 and pattern_start >= 0:
            expanded += expanded[pattern_start:pattern_start + pattern_length]
            prev_pattern_start = pattern_start
            prev_pattern_length = pattern_length
            pattern_length = -1
            pattern_start = -1

        i += 1
    if read_state != -1:
        pattern_start = prev_pattern_start
    expanded += expanded[pattern_start:pattern_start + pattern_length]
    return expanded


def num_to_chr(num):
    result = ""
    quotient = num
    while quotient >= 1:
        res = list(result)
        res.insert(0, letters[quotient % len(letters)])
        result = "".join(res)
        quotient //= len(letters)
    return result


def chr_to_num(char):
    num = 0
    place_val = 1
    for character in reversed(char):
        num += place_val * letters.index(character)
        place_val *= len(letters)
    return num


world_map = full_LZ77_decompress("Ȣ;aaǵᕼǷǻȃȓȳǽqqǵᘆǷǻȃǶȉᕼiHǵᘿǷǶzzǵᙊǷǶaqǾᕼKǴmnopǷᙤǴiǶᘿǴǴǴǶǴȍᙊnǵᙤnnnnǵǶᘿǴǶǴǶȏᙊnnǵᙤnnǴiǵᘿᙀiᘿᙀiȍᙊnmmxxxmǵᙤǶᘿǴǴǴǴǴǶȏᙊnǶᛱnnmiǵᘿᙀiᘿᙀiȍᙊnmmǺᛱiiiiiiiiiiȏᙊnnǵᙤnnǴȊᕼqǾǵᙢnᙤnnnnǵȊᕼqǾǷᙢǵᙤǵǵǴȊᕼqǾȬᘆɽᕼɽɽɁ")
print(num_to_chr(254803967))