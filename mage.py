import glob
import random
from random import sample, randint
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from flask import send_file

def make_map(size, background):
    # determine map size
    z = 0
    if size == '32':
        z = 32
    elif size == '48':
        z = 48
    elif size == '64':
        z = 64

    # list of points on map
    pointlist = []
    for a in range(z):
        for b in range(z):
            pointlist.append([a, b])

    # list of points on map excluding edges
    maprange = []
    for a in range(5, z - 5):
        for b in range(5, z - 5):
            maprange.append([a, b])

    # determine edges
    updown = []
    for a in range(1, z - 1):
        updown.append([0, a])
        updown.append([z - 1, a])

    startrow = []
    for a in range(z):
        startrow.append([a, 0])

    endrow = []
    for a in range(z):
        endrow.append([a, z - 1])

    # list of points from where rooms will start (rmcrn = room corner)
    rmcrn = sample(maprange, int(z / 3))

    rsp = []
    for x in rmcrn:
        a = x[0] - 1
        b = x[1] - 1
        rsp.append([a, b])

    # create rooms
    wdh = []
    hgt = []
    tempval = []
    for x in rmcrn:
        width = randint(3, 5)
        for _ in range(width):
            wdh.append([abs(x[0]), x[1]])
            x[0] -= 1
    for x in wdh:
        heigth = randint(3, 5)
        for i in range(width):
            hgt.append([x[0], abs(x[1])])
            x[1] -= 1

    # create roads (rsp = road starting points)

    roads = []
    y = 0
    for x in rsp:
        turns = randint(8, 12)
        a = 1
        for t in range(turns):
            y = x
            steps = randint(5, 7)
            direction = a
            if direction == 1:
                a = random.choice([1, 3, 4])
                for _ in range(steps):
                    if x[0] < steps:
                        t -= 1
                        continue
                    else:
                        x[0] -= 1
                        roads.append([abs(x[0]), x[1]])
                        x = [x[0], x[1]]

            elif direction == 2:
                a = random.choice([2, 3, 4])
                for _ in range(steps):
                    if x[0] > z - steps:
                        t -= 1
                        continue
                    else:
                        x[0] += 1
                        roads.append([x[0], x[1]])
                        x = [x[0], x[1]]

            elif direction == 3:
                a = random.choice([1, 2, 3])
                for _ in range(steps):
                    if x[1] > z - steps:
                        t -= 1
                        continue
                    else:
                        x[1] += 1
                        roads.append([x[0], x[1]])
                        x = [x[0], x[1]]

            elif direction == 4:
                a = random.choice([1, 2, 4])
                for _ in range(steps):
                    if x[1] < steps:
                        t -= 1
                        continue
                    else:
                        x[1] -= 1
                        roads.append([abs(x[0]), x[1]])
                        x = [x[0], x[1]]

    rowlist = []
    solidwall = []
    intersectie = []
    t_dr = []
    t_st = []
    t_sus = []
    t_jos = []
    l_dr_sus = []
    l_dr_jos = []
    l_st_sus = []
    l_st_jos = []
    sus_jos = []
    st_dr = []
    u_sus = []
    u_jos = []
    u_st = []
    u_dr = []

    # print map according to coordinates in pointlist
    for x in pointlist:
        if x in hgt:
            rowlist.append(' ')
        elif (x in roads or x in hgt) and ([x[0] - 1, x[1]] in roads or [x[0] - 1, x[1]] in hgt) and ([x[0], x[1] - 1] in roads or [x[0], x[1] - 1] in hgt) and ([x[0], x[1] + 1] in roads or [x[0], x[1] + 1] in hgt) and ([x[0] + 1, x[1]] in roads or [x[0] + 1, x[1]] in hgt):
            intersectie.append(x)
        elif (x in roads or x in hgt) and ([x[0] - 1, x[1]] in roads or [x[0] - 1, x[1]] in hgt) and ([x[0], x[1] - 1] in roads or [x[0], x[1] - 1] in hgt) and ([x[0] + 1, x[1]] in roads or [x[0] + 1, x[1]] in hgt):
            t_st.append(x)
        elif (x in roads or x in hgt) and ([x[0] - 1, x[1]] in roads or [x[0] - 1, x[1]] in hgt) and ([x[0], x[1] + 1] in roads or [x[0], x[1] + 1] in hgt) and ([x[0] + 1, x[1]] in roads or [x[0] + 1, x[1]] in hgt):
            t_dr.append(x)
        elif (x in roads or x in hgt) and ([x[0] - 1, x[1]] in roads or [x[0] - 1, x[1]] in hgt) and ([x[0], x[1] - 1] in roads or [x[0], x[1] - 1] in hgt) and ([x[0], x[1] + 1] in roads or [x[0], x[1] + 1] in hgt):
            t_sus.append(x)
        elif (x in roads or x in hgt) and ([x[0], x[1] - 1] in roads or [x[0], x[1] - 1] in hgt) and ([x[0] + 1, x[1]] in roads or [x[0] + 1, x[1]] in hgt) and ([x[0], x[1] + 1] in roads or [x[0], x[1] + 1] in hgt):
            t_jos.append(x)
        elif (x in roads or x in hgt) and ([x[0] - 1, x[1]] in roads or [x[0] - 1, x[1]] in hgt) and ([x[0], x[1] - 1] in roads or [x[0], x[1] - 1] in hgt):
            l_st_sus.append(x)
        elif (x in roads or x in hgt) and ([x[0] - 1, x[1]] in roads or [x[0] - 1, x[1]] in hgt) and ([x[0], x[1] + 1] in roads or [x[0], x[1] + 1] in hgt):
            l_dr_sus.append(x)
        elif (x in roads or x in hgt) and ([x[0], x[1] + 1] in roads or [x[0], x[1] + 1] in hgt) and ([x[0] + 1, x[1]] in roads or [x[0] + 1, x[1]] in hgt):
            l_st_jos.append(x)
        elif (x in roads or x in hgt) and ([x[0], x[1] - 1] in roads or [x[0], x[1] - 1] in hgt) and ([x[0] + 1, x[1]] in roads or [x[0] + 1, x[1]] in hgt):
            l_dr_jos.append(x)
        elif (x in roads or x in hgt) and ([x[0] - 1, x[1]] in roads or [x[0] - 1, x[1]] in hgt) and ([x[0] + 1, x[1]] in roads or [x[0] + 1, x[1]] in hgt):
            sus_jos.append(x)
        elif (x in roads or x in hgt) and ([x[0], x[1] - 1] in roads or [x[0], x[1] - 1] in hgt) and ([x[0], x[1] + 1] in roads or [x[0], x[1] + 1] in hgt):
            st_dr.append(x)
        elif (x in roads or x in hgt) and ([x[0] - 1, x[1]] in roads or [x[0] - 1, x[1]] in hgt):
            u_sus.append(x)
        elif (x in roads or x in hgt) and ([x[0] + 1, x[1]] in roads or [x[0] + 1, x[1]] in hgt):
            u_jos.append(x)
        elif (x in roads or x in hgt) and ([x[0], x[1] + 1] in roads or [x[0], x[1] + 1] in hgt):
            u_st.append(x)
        elif (x in roads or x in hgt) and ([x[0], x[1] - 1] in roads or [x[0], x[1] - 1] in hgt):
            u_dr.append(x)


    # draw map canvas
    h = z * 24
    background = Image.new('RGB', (h, h), 'black')

    # open image files
    room = Image.open('resources/room_blurr.png')
    img_intersectie = Image.open('resources/intersectie.png')
    img_t_dr = Image.open('resources/T_dr.png')
    img_t_st = Image.open('resources/T_st.png')
    img_t_sus = Image.open('resources/T_sus.png')
    img_t_jos = Image.open('resources/T_jos.png')
    img_l_dr_sus = Image.open('resources/L_dr_sus.png')
    img_l_dr_jos = Image.open('resources/L_dr_jos.png')
    img_l_st_sus = Image.open('resources/L_st_sus.png')
    img_l_st_jos = Image.open('resources/L_st_jos.png')
    img_sus_jos = Image.open('resources/sus_jos.png')
    img_st_dr = Image.open('resources/st_dr.png')
    img_u_sus = Image.open('resources/U_sus.png')
    img_u_jos = Image.open('resources/U_jos.png')
    img_u_st = Image.open('resources/U_st.png')
    img_u_dr = Image.open('resources/U_dr.png')



    # draw map in image file
    for x in hgt:
        background.paste(room, (x[0] * 24, x[1] * 24))

    for x in intersectie:
        background.paste(img_intersectie, (x[0] * 24, x[1] * 24))

    for x in t_dr:
        background.paste(img_t_dr, (x[0] * 24, x[1] * 24))

    for x in t_st:
        background.paste(img_t_st, (x[0] * 24, x[1] * 24))

    for x in t_sus:
        background.paste(img_t_sus, (x[0] * 24, x[1] * 24))

    for x in t_jos:
        background.paste(img_t_jos, (x[0] * 24, x[1] * 24))

    for x in l_dr_sus:
        background.paste(img_l_dr_sus, (x[0] * 24, x[1] * 24))

    for x in l_dr_jos:
        background.paste(img_l_dr_jos, (x[0] * 24, x[1] * 24))

    for x in l_st_sus:
        background.paste(img_l_st_sus, (x[0] * 24, x[1] * 24))

    for x in l_st_jos:
        background.paste(img_l_st_jos, (x[0] * 24, x[1] * 24))

    for x in sus_jos:
        background.paste(img_sus_jos, (x[0] * 24, x[1] * 24))

    for x in st_dr:
        background.paste(img_st_dr, (x[0] * 24, x[1] * 24))

    for x in u_sus:
        background.paste(img_u_sus, (x[0] * 24, x[1] * 24))

    for x in u_jos:
        background.paste(img_u_jos, (x[0] * 24, x[1] * 24))

    for x in u_st:
        background.paste(img_u_st, (x[0] * 24, x[1] * 24))

    for x in u_dr:
        background.paste(img_u_dr, (x[0] * 24, x[1] * 24))

    ## struct ex: 'The [adj] [noun] [of opt]'

    adjective = ['ruined ', 'forgotten ', 'twisted ', 'lost ', 'dark ', 'deep ', 'scattered ', 'buried ', 'ancient ',
                 'whispering ', 'haunted ', 'horrid ', 'barren ', 'corrupted ', 'crushing ', 'delirious ', 'evil ', 'grim ',
                 'destructive ', 'insidious ', 'pernicious ', 'sinister ', 'baleful ', 'dire ', 'ominous ', 'deceiving ',
                 'malign ', 'hundred ', ]
    noun = ['paths ', 'ways ', 'cellars ', 'depths ', 'catacombs ', 'serpents ', 'tunnels ', 'crawls ', 'lairs ', 'echoes ',
            'mists ', 'twists ', 'maze ', ]
    optional = ['of the voiceless', '', 'of Antiquity', '', 'of madness', '', 'of crushing despair', '', 'of solitude', '',
                'of silence', 'of the past', 'of nowhere', 'of nothingness', 'of dust', 'of bestial rage', 'of shadows',
                'of eons past', 'of entropy', 'of Priestown', ]

    adj = random.choice(adjective)
    subst = random.choice(noun)
    opt = random.choice(optional)

    text = 'The ' + adj + subst + opt

    draw = ImageDraw.Draw(background)

    frame = [0, h - 65, h - 1, h - 1]
    x1, y1, x2, y2 = frame

    font = ImageFont.truetype('resources/Alkhemikal.ttf', size=z)

    w, h = draw.textsize(text, font=font)

    x = (x2 - x1 - w) / 2 + x1
    y = (y2 - y1 - h) / 2 + y1

    draw.text((x, y), text, font=font)

    img_io = BytesIO()
    background.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')







