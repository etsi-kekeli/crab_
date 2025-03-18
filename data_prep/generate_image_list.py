import os

crab_id = '/m/0n28_'

train_bboxes_filename = os.path.join('data_prep', 'oidv6-train-annotations-bbox.csv')
validation_bboxes_filename = os.path.join('data_prep', 'validation-annotations-bbox.csv')
test_bboxes_filename = os.path.join('data_prep', 'test-annotations-bbox.csv')

image_list_file_path = os.path.join('data_prep', 'image_list_file.txt')

image_list_file_list = []
for j, filename in enumerate([train_bboxes_filename, validation_bboxes_filename, test_bboxes_filename]):
    print(filename)
    with open(filename, 'r') as f:
        line = f.readline()
        while len(line) != 0:
            id, _, class_name, *_ = line.split(',')[:13]
            if class_name in [crab_id] and id not in image_list_file_list:
                image_list_file_list.append(id)
                with open(image_list_file_path, 'a') as fw:
                    fw.write('{}/{}\n'.format(['train', 'validation', 'test'][j], id))
            line = f.readline()

        f.close()