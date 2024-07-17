import os
import pandas as pd
from django.conf import settings
from machineLearning.models import MachineLearningResult
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


class MLService(object):
    COLUMN_NAMES = [
        "duration",
        "protocol_type",
        "service",
        "flag",
        "src_bytes",
        "dst_bytes",
        "land",
        "wrong_fragment",
        "urgent",
        "hot",
        "num_failed_logins",
        "logged_in",
        "num_compromised",
        "root_shell",
        "su_attempted",
        "num_root",
        "num_file_creations",
        "num_shells",
        "num_access_files",
        "num_outbound_cmds",
        "is_host_login",
        "is_guest_login",
        "count",
        "srv_count",
        "serror_rate",
        "srv_serror_rate",
        "rerror_rate",
        "srv_rerror_rate",
        "same_srv_rate",
        "diff_srv_rate",
        "srv_diff_host_rate",
        "dst_host_count",
        "dst_host_srv_count",
        "dst_host_same_srv_rate",
        "dst_host_diff_srv_rate",
        "dst_host_same_src_port_rate",
        "dst_host_srv_diff_host_rate",
        "dst_host_serror_rate",
        "dst_host_srv_serror_rate",
        "dst_host_rerror_rate",
        "dst_host_srv_rerror_rate",
        "label"
    ]

    @classmethod
    def process(cls, instance: MachineLearningResult) -> None:
        """
        Ниже приведен пример программы, которая демонстрирует использование
        машинного обучения для обнаружения сетевых атак. В данном пример
        используется набор данных KDD Cup 99, который является популярным
        набором данных для обнаружения аномалий в сетевом трафике.
        Этот код занимается обработкой и моделированием данных из набора
        данных KDD Cup 99 для задачи классификации сетевого трафика. Подробное описание каждого шага.
        Этот процесс включает предобработку данных, обучение модели, прогнозирование и оценку результатов,
        что является стандартной процедурой для решения задач машинного обучения.
        """

        # Загрузка CSV-файла (KDD Cup 99), содержащего набор данных,
        # и именование его столбцов в соответствии с cls.COLUMN_NAMES.
        dataset = pd.read_csv(os.path.join(settings.MEDIA_ROOT, str(instance.dataset)), names=cls.COLUMN_NAMES)

        # Преобразуем текстовые метки в числовые
        protocol_type_mapping = {"tcp": 0, "udp": 1, "icmp": 2}
        dataset["protocol_type"] = dataset["protocol_type"].map(protocol_type_mapping)

        # Преобразование категориальных признаков protocol_type и flag в числовые значения с помощью словарей.
        flag_mapping = {"SF": 0, "S0": 1, "REJ": 2, "RSTR": 3, "RSTO": 4, "SH": 5, "S1": 6, "S2": 7, "S3": 8, "OTH": 9}
        dataset["flag"] = dataset["flag"].map(flag_mapping)

        # Встроенное преобразование категориального признака service в числовые значения,
        # где каждому уникальному значению присваивается уникальный индекс.
        service_mapping = {name: index for index, name in enumerate(dataset["service"].unique())}
        dataset["service"] = dataset["service"].map(service_mapping)

        # Преобразуем метку на 0 (нормальный трафик) и 1 (атака)
        dataset["label"] = dataset["label"].apply(lambda x: 0 if x == "normal." else 1)

        #  Разделение данных на матрицу признаков X (все столбцы, кроме label) и вектор меток y (столбец label).
        X = dataset.drop("label", axis=1)
        y = dataset["label"]

        # Разделение данных на обучающую (70%) и тестовую (30%) выборки
        # с фиксированным случайным состоянием для воспроизводимости.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Масштабирование признаков с использованием StandardScaler.
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Обучаем модель RandomForestClassifier
        # Создание и обучение модели случайного леса с 100 деревьями и фиксированным случайным состоянием.
        classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        classifier.fit(X_train, y_train)

        # Прогнозируем на тестовой выборке
        y_pred = classifier.predict(X_test)

        # Получение отчета классификации и сохранение этого отчета и точности модели в экземпляре instance.
        report = classification_report(y_test, y_pred)
        instance.report = report
        instance.accuracy = accuracy_score(y_test, y_pred)
        instance.is_processed = True
        instance.save()
