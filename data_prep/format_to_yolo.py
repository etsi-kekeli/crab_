import os
import shutil
import config


IMG_ONLY = os.path.join('..', 'images')

DATA_OUT_DIR = os.path.join('..', 'data')
IMAGES_DIR = os.path.join(DATA_OUT_DIR, 'images')
LABELS_DIR = os.path.join(DATA_OUT_DIR, 'labels')

if not os.path.exists(DATA_OUT_DIR):
    os.mkdir(DATA_OUT_DIR)

    if not os.path.exists(IMAGES_DIR):
        os.mkdir(IMAGES_DIR)
    
    if not os.path.exists(LABELS_DIR):
        os.mkdir(LABELS_DIR)


for set_ in ['train', 'validation', 'test']:
    for dir_ in [os.path.join(IMAGES_DIR, set_),
                 os.path.join(LABELS_DIR, set_)]:
        if os.path.exists(dir_):
            print('Removing {}'.format(dir_))
            shutil.rmtree(dir_)
        os.mkdir(dir_)

target_id = config.CLASS_ID

train_bboxes_filename = os.path.join('.', 'oidv6-train-annotations-bbox.csv')
validation_bboxes_filename = os.path.join('.', 'validation-annotations-bbox.csv')
test_bboxes_filename = os.path.join('.', 'test-annotations-bbox.csv')


for j, filename in enumerate([train_bboxes_filename, validation_bboxes_filename, test_bboxes_filename]):
    set_ = ['train', 'validation', 'test'][j]
    print(filename)
    with open(filename, 'r') as f:
        line = f.readline()
        while len(line) != 0:
            id, _, class_name, _, x1, x2, y1, y2, _, _, _, _, _ = line.split(',')[:13]
            if class_name in [target_id]:
                if not os.path.exists(os.path.join(IMAGES_DIR, set_, f'{id}.jpg')):
                    shutil.copy(os.path.join(IMG_ONLY, f'{id}.jpg'),
                                os.path.join(IMAGES_DIR, set_, f'{id}.jpg'))
                
                with open(os.path.join(LABELS_DIR, set_, f'{id}.txt'), 'a') as f_ann:
                    # class_id, xc, yx, w, h
                    x1, x2, y1, y2 = [float(j) for j in [x1, x2, y1, y2]]
                    xc = (x1 + x2) / 2
                    yc = (y1 + y2) / 2
                    w = x2 - x1
                    h = y2 - y1

                    f_ann.write('0 {} {} {} {}\n'.format(xc, yc, w, h))
                    f_ann.close()

            line = f.readline()