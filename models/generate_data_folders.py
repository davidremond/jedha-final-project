"""
    Load the dataset from a CSV file.

    Parameters
    ----------
    file_path : str
        Path to the dataset file.

ratio_malade : >= 0.5 for imbalanced data
test_ratio : we put 20% in this folder for testing later on
ratio_sample : set to 0.20 for light model training, to 1 for training on the whole dataset (70000 images minus the test samples)

    Returns
    -------
    pd.DataFrame
        Loaded dataset as a Pandas DataFrame.

    """

import os
import random
import shutil
import subprocess


def replace_spaces_with_underscores(directory):

    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            new_name = name.replace(' ', '_')
            if new_name != name:
                old_path = os.path.join(root, name)
                new_path = os.path.join(root, new_name)
                shutil.move(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")


def create_folders_multi7(test_ratio=0.2, source_dir='', ratio_sample=1):

    random.seed(42) 
    multi_sample_dir = str(source_dir)+"_Sample_Multi7"
    multi_sample_test_dir = str(source_dir)+"_Sample_Multi7_Test"

    malades_classes = ['Chest_Changes', 'Degenerative_Infectious_Diseases', 'Encapsulated_Lesions',
                   'Higher_Density', 'Lower_Density', 'Mediastinal_Changes', 'Obstructive_Pulmonary_Diseases']

    os.makedirs(multi_sample_dir, exist_ok=True)
    os.makedirs(multi_sample_test_dir, exist_ok=True)
    for class_name in malades_classes:
        dir_train = os.path.join(multi_sample_dir, class_name)
        dir_test = os.path.join(multi_sample_test_dir, class_name)
        os.makedirs(dir_train, exist_ok=True)
        os.makedirs(dir_test, exist_ok=True)

    total_images_perclass = len(os.listdir(os.path.join(source_dir, malades_classes[0])))
    images_test_count = int(test_ratio * total_images_perclass)
    images_train_count = int((total_images_perclass - images_test_count)*ratio_sample)

    for class_name in malades_classes:
        class_path = os.path.join(source_dir, class_name)
        images = os.listdir(class_path)
        random.shuffle(images)

        test_images = images[:images_test_count]
        train_images = images[images_test_count:(images_test_count+images_train_count)]

        dir_train = os.path.join(multi_sample_dir, class_name)
        for img in train_images:
            src_path = os.path.join(class_path, img)
            dest_path = os.path.join(dir_train, img)
            shutil.copy(src_path, dest_path)

        dir_test = os.path.join(multi_sample_test_dir, class_name)
        for img in test_images:
            src_path = os.path.join(class_path, img)
            dest_path = os.path.join(dir_test, img)
            shutil.copy(src_path, dest_path)


def create_folders_binary(ratio_malade=0.875, test_ratio=0.2, source_dir='', ratio_sample=1):

    random.seed(42) 
    binary_sample_dir = str(source_dir)+"_Sample_Binaire_With_Ratio"
    binary_sample_test_dir = str(source_dir)+"_Sample_Binaire_Test"

    os.makedirs(binary_sample_dir, exist_ok=True)
    normal_dir = os.path.join(binary_sample_dir, "Normal")
    malades_dir = os.path.join(binary_sample_dir, "Malades")
    os.makedirs(normal_dir, exist_ok=True)
    os.makedirs(malades_dir, exist_ok=True)

    os.makedirs(binary_sample_test_dir, exist_ok=True)
    test_normal_dir = os.path.join(binary_sample_test_dir, "Normal")
    test_malades_dir = os.path.join(binary_sample_test_dir, "Malades")
    os.makedirs(test_normal_dir, exist_ok=True)
    os.makedirs(test_malades_dir, exist_ok=True)

    malades_classes = ['Chest_Changes', 'Degenerative_Infectious_Diseases', 'Encapsulated_Lesions',
                    'Higher_Density', 'Lower_Density', 'Mediastinal_Changes', 'Obstructive_Pulmonary_Diseases']
    normal_classes = ['Normal']

    normal_total_images = len(os.listdir(os.path.join(source_dir, normal_classes[0])))
    normal_test_count = int(test_ratio * normal_total_images)
    normal_train_count = int((normal_total_images - normal_test_count)*ratio_sample)

    malades_total_images = normal_total_images * 7
    malades_tokeep_images = int(normal_total_images*ratio_malade/(1-ratio_malade))  
    malades_test_count = int(test_ratio * malades_tokeep_images)
    malades_train_count = int((malades_tokeep_images - malades_test_count)*ratio_sample)
    if malades_train_count < malades_total_images*ratio_sample:
        print(f"pas assez d'images de malades pour ces ratio de malades ({ratio_malade} %) \
            et de test ({test_ratio} %) : modifiez ces ratio")

    for class_name in normal_classes:
        class_path = os.path.join(source_dir, class_name)
        images = os.listdir(class_path)
        random.shuffle(images)

        test_images = images[:normal_test_count]
        train_images = images[normal_test_count:(normal_test_count+normal_train_count)]

        for img in train_images:
            src_path = os.path.join(class_path, img)
            dest_path = os.path.join(normal_dir, img)
            shutil.copy(src_path, dest_path)

        for img in test_images:
            src_path = os.path.join(class_path, img)
            dest_path = os.path.join(test_normal_dir, img)
            shutil.copy(src_path, dest_path)

    for class_name in malades_classes:
        class_path = os.path.join(source_dir, class_name)
        images = os.listdir(class_path)
        random.shuffle(images)

        test_images = images[:malades_test_count // len(malades_classes)]
        train_images = images[malades_test_count // len(malades_classes):\
            (malades_test_count+malades_train_count) // len(malades_classes)]

        for img in train_images:
            src_path = os.path.join(class_path, img)
            dest_path = os.path.join(malades_dir, img)
            shutil.copy(src_path, dest_path)

        for img in test_images:
            src_path = os.path.join(class_path, img)
            dest_path = os.path.join(test_malades_dir, img)
            shutil.copy(src_path, dest_path)


def main():
    command1 = "kaggle datasets download -d ghostbat101/lung-x-ray-image-clinical-text-dataset -p data"
    result1 = subprocess.run(command1, shell=True, capture_output=True, text=True)
    if result1.returncode != 0:
        print("Error while loading the dataset: \n", result1.stderr)
    command2 = "unzip -n data/lung-x-ray-image-clinical-text-dataset.zip -d data"
    result2 = subprocess.run(command2, shell=True, capture_output=True, text=True)
    if result2.returncode != 0:
        print("Error while loading the dataset: \n", result2.stderr)
    replace_spaces_with_underscores('data')
    create_folders_multi7(test_ratio=0.2, source_dir="data/Main_dataset", ratio_sample=1)
    create_folders_binary(ratio_malade=0.875, test_ratio=0.2, source_dir="data/Main_dataset", ratio_sample=1)


if __name__ == "__main__":
    main()