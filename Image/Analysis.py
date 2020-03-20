from PIL import ImageFont


def analysis(obj):
    params = dict()
    params['size'] = size(obj)
    params['rgb'] = color(obj)
    params['lines'] = line(obj)
    params['ellipses'] = ellipse_and_rectangle(obj, 'ellipses')
    params['rectangles'] = ellipse_and_rectangle(obj, 'rectangles')
    params['texts'] = text(obj)
    params['store'] = store(obj)
    params['point'] = point(obj)
    params['opacity'] = opacity(obj)
    params['original'] = o if (o := obj.get('original')) else False
    params['colour'] = colour(obj)
    params['album'] = album(obj)
    return params


def opacity(obj):
    if a := o if (o := obj.get('a')) else None:
        return op if 0 <= (op := int(a)) <= 255 else None
    return None


def album(obj):
    data = params.split(',') if (params := obj.get('album')) else None
    if data and len(data) >= 2:
        return [data[0], data[1]]
    return None


def colour(obj):
    data = params.split(',') if (params := obj.get('colour')) else None
    if data and len(data) >= 7:
        return [int(data[0]), (int(data[1]), int(data[2]), int(data[3])), (int(data[4]), int(data[5]), int(data[6]))]
    return None


def store(obj):
    bg = None if not obj.get('store') else obj.get('store').split(',')
    if bg:
        if len(bg) >= 2:
            bg_args = [bg[0], bg[1]]
            return bg_args
        if len(bg) >= 1:
            bg_args = [bg[0], '0']
            return bg_args
    else:
        return None


def point(obj):
    return None if not obj.get('point') else float(obj.get('point'))


def size(obj):
    width = int(obj.get('width') or obj.get('w') or '400')
    height = int(obj.get('height') or obj.get('h') or '300')
    return width, height


def color(obj):
    rgb = (obj.get('rgb') or '200,200,200').split(',')
    rgb[0] = rgb[0] if not obj.get('r') else obj.get('r')
    rgb[1] = rgb[1] if not obj.get('g') else obj.get('g')
    rgb[2] = rgb[2] if not obj.get('b') else obj.get('b')
    return int(rgb[0]), int(rgb[1]), int(rgb[2])


def line(obj):
    lines = list()
    if lines_args := obj.get('lines'):
        line_args = lines_args.split(';')
        for i in line_args:
            try:
                line_arg = i.split(',')
                if len(line_arg) >= 7:
                    lines.append([(int(line_arg[0]), int(line_arg[1]), int(line_arg[2]), int(line_arg[3])),
                                  (int(line_arg[4]), int(line_arg[5]), int(line_arg[6]))])
                elif len(line_arg) >= 4:
                    lines.append([(int(line_arg[0]), int(line_arg[1]), int(line_arg[2]), int(line_arg[3])), (0, 0, 0)])
            except Exception as ex:
                print(str(ex))
    return lines


def ellipse_and_rectangle(obj, shape):
    shapes = list()
    if shapes_args := obj.get(shape):
        shape_args = shapes_args.split(';')
        for i in shape_args:
            try:
                shape_arg = i.split(',')
                if len(shape_arg) >= 10:
                    shapes.append(
                        [(int(shape_arg[0]), int(shape_arg[1]), int(shape_arg[2]), int(shape_arg[3])),
                         (int(shape_arg[4]), int(shape_arg[5]), int(shape_arg[6])),
                         (int(shape_arg[7]), int(shape_arg[8]), int(shape_arg[9]))])
                elif len(shape_arg) >= 7:
                    shapes.append(
                        [(int(shape_arg[0]), int(shape_arg[1]), int(shape_arg[2]), int(shape_arg[3])),
                         (int(shape_arg[4]), int(shape_arg[5]), int(shape_arg[6])),
                         (0, 0, 0)])
                elif len(shape_arg) >= 4:
                    shapes.append(
                        [(int(shape_arg[0]), int(shape_arg[1]), int(shape_arg[2]), int(shape_arg[3])),
                         (0, 0, 0), (0, 0, 0)])
            except Exception as ex:
                print(str(ex))
    return shapes


def text(obj):
    texts = list()
    if texts_args := obj.get('texts'):
        text_args = texts_args.split(';')
        # ttf = '/home/ahri/code/AhriImage/Image/font.ttf'
        ttf = '/project/Image/font.ttf'
        for i in text_args:
            text_arg = i.split(',')
            if len(text_arg) >= 7:
                texts.append([(int(text_arg[0]), int(text_arg[1])), text_arg[2],
                              (int(text_arg[3]), int(text_arg[3]), int(text_arg[5])),
                              ImageFont.truetype(ttf, int(text_arg[6]))])
            elif len(text_arg) >= 6:
                texts.append([(int(text_arg[0]), int(text_arg[1])), text_arg[2],
                              (int(text_arg[3]), int(text_arg[3]), int(text_arg[5])),
                              ImageFont.truetype(ttf, 30)])
            if len(text_args) >= 3:
                texts.append([(int(text_arg[0]), int(text_arg[1])), text_arg[2], (0, 0, 0),
                              ImageFont.truetype(ttf, 30)])
    return texts
