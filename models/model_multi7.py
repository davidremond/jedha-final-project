import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.utils.class_weight import compute_class_weight

def preprocessing():

    """
    Prépare les générateurs d'images pour l'entraînement et la validation.

    Returns:
        tuple: Un tuple contenant les générateurs d'images pour l'entraînement et la validation.
    """

    img_generator = ImageDataGenerator(
        rescale=1/255.,
        validation_split=0.2 
    )

    train_generator = img_generator.flow_from_directory(
        'data/Main_dataset_Sample_Multi7',
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        color_mode="grayscale",
        subset="training",
        seed = 42
    )

    valid_generator = img_generator.flow_from_directory(
        'data/Main_dataset_Sample_Multi7',
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        color_mode="grayscale",
        subset="validation",
        shuffle=False,
        seed = 42
    )

    return(train_generator, valid_generator)


def main():

    """
    Fonction principale pour l'entraînement et l'évaluation d'un modèle de classification binaire.

    Cette fonction configure MLflow pour le suivi des expériences, prépare les données,
    construit et entraîne un modèle de classification binaire, puis enregistre les métriques et les artefacts dans MLflow.

    Returns:
        None
    """

    MLFLOW_SERVER_URI = 'https://david-rem-jedha-final-project-mlops.hf.space'
    EXPERIMENT_NAME = 'multi' 
    CLASSES = 7
    EPOCHS = 20
    TRAINER = 'final_models' 
    MODEL_TYPE = 'finalmodel_multi7_v4' 
    mlflow.set_tracking_uri(MLFLOW_SERVER_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)
    mlflow.tensorflow.autolog()
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    mlflow.start_run(experiment_id = experiment.experiment_id)

    img_generator_flow_train, img_generator_flow_valid = preprocessing()

    base_model = tf.keras.applications.InceptionV3(input_shape=(224, 224, 3), 
                                                     include_top=False,
                                                     weights = "imagenet",
                                                     name="InceptionV3",
                                                    )
    base_model.trainable = True
    fine_tune_at = len(base_model.layers) - 20
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False
    for layer in base_model.layers[fine_tune_at:]:
        layer.trainable = True
    
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(224, 224, 1)),
        tf.keras.layers.Conv2D(3, (1, 1)),
        base_model, 
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(CLASSES, activation="softmax")  
    ])  

    initial_learning_rate = 0.001
    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate,
        decay_steps=1000,
        decay_rate=0.96,
        staircase=True)
    optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)

    model.compile(
        optimizer=optimizer,
        loss=tf.keras.losses.CategoricalCrossentropy(),
        metrics=[tf.keras.metrics.CategoricalAccuracy()]
    )

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True 
    )

    history = model.fit(
        img_generator_flow_train, 
        epochs=EPOCHS, 
        validation_data=img_generator_flow_valid, 
        callbacks=[early_stopping],
        shuffle=True,
    )

    mlflow.log_param("trainer", TRAINER) 
    mlflow.log_param("epochs", EPOCHS) 
    mlflow.log_param("model_type", MODEL_TYPE)
    mlflow.keras.log_model(model, "model")
    history = model.history
    for epoch in range(len(history.history['loss'])):
        mlflow.log_metric('loss', history.history['loss'][epoch], step=epoch)
        mlflow.log_metric('categorical_accuracy', history.history['categorical_accuracy'][epoch], step=epoch)
        mlflow.log_metric('val_loss', history.history['val_loss'][epoch], step=epoch)
        mlflow.log_metric('val_categorical_accuracy', history.history['val_categorical_accuracy'][epoch], step=epoch)
    predictions = model.predict(img_generator_flow_valid)
    y_pred = np.argmax(predictions, axis=1)
    y_true = img_generator_flow_valid.classes
    report = classification_report(y_true, y_pred)
    with open("classification_report.txt", "w") as file:
        file.write(report)
    report = classification_report(y_pred, y_true, output_dict=True)
    mlflow.log_artifact('classification_report.txt', artifact_path="model")
    mlflow.log_metric('global_accuracy', report['accuracy'])
    mlflow.log_metric('macro_avg_precision', report['macro avg']['precision'])
    mlflow.log_metric('macro_avg_recall', report['macro avg']['recall'])
    mlflow.log_metric('macro_avg_f1_score', report['macro avg']['f1-score'])
    mlflow.log_metric('macro_avg_support', report['macro avg']['support'])
    mlflow.log_metric('weighted_avg_precision', report['weighted avg']['precision'])
    mlflow.log_metric('weighted_avg_recall', report['weighted avg']['recall'])
    mlflow.log_metric('weighted_avg_f1_score', report['weighted avg']['f1-score'])
    mlflow.log_metric('weighted_avg_support', report['weighted avg']['support'])
    for class_mesure in list(report.items())[:CLASSES]:
        for m_name, m_value in class_mesure[1].items():
            mlflow.log_metric(m_name, m_value, step=int(class_mesure[0]))
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=img_generator_flow_valid.class_indices.keys())
    disp.plot()
    plt.title("Matrice de Confusion")
    plt.xticks(rotation=90)
    plt.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png", artifact_path='model')
    mlflow.end_run()


if __name__ == "__main__":
    main()
