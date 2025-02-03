import os
import random
import shutil
import subprocess


def replace_spaces_with_underscores(directory):

    """
    Remplace les espaces par des underscores dans les noms de dossiers d'un répertoire donné.

    Args:
        directory (str): Le chemin du répertoire dans lequel les noms de dossiers doivent être modifiés.

    Returns:
        None
    """

    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            new_name = name.replace(' ', '_')
            if new_name != name:
                old_path = os.path.join(root, name)
                new_path = os.path.join(root, new_name)
                shutil.move(old_path, new_path)


def create_folders_multi7(test_ratio=0.2, source_dir='', ratio_sample=1):

    """
    Crée des dossiers pour un échantillon multiclasses de données avec un ratio spécifié pour les images du test.

    Args:
        test_ratio (float): Le ratio des images de test par rapport aux images totales.
        source_dir (str): Le chemin du répertoire source contenant les images.
        ratio_sample (float): Le ratio d'échantillonnage des images : si <1 (par exemple 
            0.2 pour un entraînement léger), une partie des images ne sera pas mise dans un dossier.

    Returns:
        None
    """

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

    total_images_perclass = int(len(os.listdir(os.path.join(source_dir, malades_classes[0])))*ratio_sample)
    images_test_count = int(test_ratio * total_images_perclass)

    for class_name in malades_classes:
        class_path = os.path.join(source_dir, class_name)
        images = os.listdir(class_path)
        random.shuffle(images)

        test_images = images[:images_test_count]
        train_images = images[images_test_count:total_images_perclass]

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

    """
    Crée des dossiers pour un échantillon binaire de données avec des ratios spécifiés pour les images malades et de test.

    Args:
        ratio_malade (float): Le ratio des images malades par rapport aux images normales : si >= 0.5, le modèle binaire s'entraînera sur des données imbalanced. 
            Faire attention à de possibles incompatibilités entre ratio_malade et ratio_sample (pas 
            assez d'images dans le dataset pour répondre aux deux conditions en même temps).
        test_ratio (float): Le ratio des images de test par rapport aux images totales.
        source_dir (str): Le chemin du répertoire source contenant les images.
        ratio_sample (float): Le ratio d'échantillonnage des images : si <1 (par exemple 
            0.2 pour un entraînement léger), une partie des images ne sera pas mise dans un dossier.

    Returns:
        None
    """

    random.seed(42) 
    binary_sample_dir = str(source_dir)+"_Sample_Binary_With_Ratio"
    binary_sample_test_dir = str(source_dir)+"_Sample_Binary_Test"

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

    normal_total_images = int(len(os.listdir(os.path.join(source_dir, normal_classes[0])))*ratio_sample)
    normal_test_count = int(test_ratio * normal_total_images)

    malades_total_images = normal_total_images * 7
    malades_tokeep_images = int(normal_total_images*ratio_malade/(1-ratio_malade))  
    malades_test_count = int(test_ratio * malades_tokeep_images)

    for class_name in normal_classes:
        class_path = os.path.join(source_dir, class_name)
        images = os.listdir(class_path)
        random.shuffle(images)

        test_images = images[:normal_test_count]
        train_images = images[normal_test_count:normal_total_images]

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
            malades_tokeep_images // len(malades_classes)]

        for img in train_images:
            src_path = os.path.join(class_path, img)
            dest_path = os.path.join(malades_dir, img)
            shutil.copy(src_path, dest_path)

        for img in test_images:
            src_path = os.path.join(class_path, img)
            dest_path = os.path.join(test_malades_dir, img)
            shutil.copy(src_path, dest_path)


def main():

    """
    Fonction principale qui télécharge un dataset depuis Kaggle, décompresse les fichiers,
    remplace les espaces par des underscores dans les noms de dossiers,
    et crée des dossiers pour les deux types de modèles :
    - modèle binaire : crée le dossier "Main_dataset_Sample_Binary_With_Ratio" pour l'entraînement et la validation 
        avec 80% des images, et le dossier "Main_dataset_Sample_Binary_Test" avec 20% des images pour les tests
    - modèle multiclasses (7 classes): crée le dossier "Main_dataset_Sample_Multi7" pour l'entraînement et la validation 
        avec 80% des images, et le dossier "Main_dataset_Sample_Multi7_Test" avec 20% des images pour les tests.

    Returns:
        None
    """

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