import random
from PIL import Image, ImageDraw, ImageFont


def generation_code():
    '''
    生成随机字符
    :return:
    '''
    valid_code = ''
    for i in range(4):
        string_low = chr(random.randint(97, 122))
        string_upper = chr(random.randint(65, 90))
        num = str(random.randint(0, 9))
        code = random.choice([string_low, string_upper, num])
        valid_code += code
    return valid_code


def get_random_color():
    '''
    生成随机颜色
    :return:
    '''
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def generation_img():
    '''
    生成图片
    :return:
    '''
    check_code = generation_code()
    img = Image.new("RGB", (106, 35), color=get_random_color())
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('../../static/font/calibriz.ttf', size=35)

    i = 1
    # 写入文本
    for c in check_code:
        draw.text((i*21, 4), c, font=font)
        i = i+1

    # 设置图片宽高
    width = 106
    height = 35

    # 写干扰点
    for i in range(20):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
    # 画线干扰
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    # 写干扰圆圈
    for i in range(5):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

        # path = './static/images/pin/' + check_code + '.jpg'
        # img.save(path)
    return img, check_code


if __name__ == '__main__':

    img, pin = generation_img()
    print(img, pin)
