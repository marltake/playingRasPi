import copy


rainbow0 = [0xC7000B, 0xD28300, 0xDFD000, 0x00873C, 0x005AA0, 0x181878, 0x800073] * 10
rainbowA = [0x730009, 0x753000, 0x794C00, 0x7E6400, 0x7F7800, 0x676D00, 0x47610F, 0x11561C,
            0x004C22, 0x004D35, 0x004F4B, 0x005060, 0x005074, 0x004368, 0x00345B, 0x00234E,
            0x0E1044, 0x300C43, 0x490341, 0x5F0040, 0x72003F, 0x720035, 0x720027, 0x730019]
rainbowB = [0x390004, 0x3A1800, 0x3C2600, 0x3F3200, 0x3F3C00, 0x333600, 0x233007, 0x082B0E,
            0x002611, 0x00261A, 0x002725, 0x002830, 0x00283A, 0x002134, 0x001A2D, 0x001127,
            0x070822, 0x180621, 0x240120, 0x2F0020, 0x39001F, 0x39001A, 0x390013, 0x39000C]
rainbowC = [0x1C0002, 0x1D0C00, 0x1E1300, 0x1F1900, 0x1F1E00, 0x191B00, 0x111803, 0x041507, 
            0x001308, 0x00130D, 0x001312, 0x001418, 0x00141D, 0x00101A, 0x000D16, 0x000813, 
            0x030411, 0x0C0310, 0x120010, 0x170010, 0x1C000F, 0x1C000D, 0x1C0009, 0x1C0006]
rainbow = [0x0E0001, 0x0E0600, 0x0F0900, 0x0F0C00, 0x0F0F00, 0x0C0D00, 0x080C01, 0x020A03, 
           0x000904, 0x000906, 0x000909, 0x000A0C, 0x000A0E, 0x00080D, 0x00060B, 0x000409, 
           0x010208, 0x060108, 0x090008, 0x0B0008, 0x0E0007, 0x0E0006, 0x0E0004, 0x0E0003] * 4
# rainbow = (rainbow + rainbow)[::2]

def stream():
    for i in range(23, -1, -1):
        yield rainbow[i:i+60]

def wave():
    for i in range(59):
        yield rainbow[:i] + [0] * (60 - i)
    for i in range(59):
        yield [0] * i + rainbow[i:]

def ping_pong():
    for i in range(12):
        yield rainbow[12 - i:24] + [0] * (48 + i)
    for i in range(48):
        yield ([0] * i + rainbow[:24] + [0] * 36)[:60]
    for i in range(48):
        yield ([0] * (48 - i) + rainbow[:24] + [0] * 36)[:60]
    for i in range(12):
        yield rainbow[i:24] + [0] * (36 + i)

def in_out():
    yield [0] * 60
    for i in list(range(1, 60)) + list(range(60, 0, -1)):
        yield rainbow[-i:] + [0] * (60 - i)

def spring():
    for i in range(23, -1, -1):
        yield rainbow[i:i+30][::-1] + rainbow[i:i+30]


def go_back():
    for i in range(23, 0, -1):
        yield rainbow[i:i+60]
    for i in range(23):
        yield rainbow[i:i+60]

def black_ping_pong():
    for i in range(59, 0, -1):
        yield rainbow[:i] + [0] + rainbow[i+1:]
    for i in range(59):
        yield rainbow[:i] + [0] + rainbow[i+1:]

def black_cross():
    for i in range(59):
        d = copy.copy(rainbow)
        d[i] = 0
        d[59 - i] = 0
        yield d


def get_generator(pattern_index):
    generators = [stream, wave, ping_pong, in_out, spring, go_back, black_ping_pong, black_cross]
    return generators[pattern_index % len(generators)]
