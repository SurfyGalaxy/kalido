def hex_to_rbg(stops):
    rgb_stops = []
    stops = [code[1:] for code in stops] # Strip the leading # to make my life easier

    for code in stops:
        red = int(code[:2], 16)
        green = int(code[2:4], 16)
        blue = int(code[4:], 16)
        rgb_stops.append((red, green, blue))
    return rgb_stops

def rgb_to_hex(stops):
    hex_list = []
    index = 0
    for rgb in stops:
        hex_colour = "#{:02X}{:02X}{:02X}".format(*stops[index])
        hex_list.append(hex_colour)
        index += 1
    return hex_list
    


def create_gradient(stops, count):
    stops = hex_to_rbg(stops) # to get pure RGB
    percent = 1 / (count + 1)
    gradient = [] 
    segments = len(stops) - 1 # to count how many we need to generate

    for index in range(segments):
        red_1, green_1, blue_1 = stops[index]
        red_2, green_2, blue_2 = stops[index + 1]

        # Actually generate the parts
        for step in range(count):
            # Percent raises to fill out the gap
            percent = step / count
            
            red = int(red_1 + (percent * (red_2 - red_1)))
            green = int(green_1 + (percent * (green_2 - green_1)))
            blue = int(blue_1 + (percent * (blue_2 - blue_1)))
            
            gradient.append((red, green, blue))
            
    # Tidy it up
    gradient.append(stops[-1])
    return gradient

def colour_char(char: str, colour: tuple) -> str:
    return f"\x1b[38;2;{colour[0]};{colour[1]};{colour[2]}m{char}"

def colourise(stops, char, index):
    colour = stops[index]
    return colour_char(char, colour)