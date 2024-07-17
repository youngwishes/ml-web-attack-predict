from django.db import models


class MachineLearningResult(models.Model):
    accuracy = models.FloatField("точность предсказания", null=True, blank=True)
    dataset = models.FileField("набор данных", upload_to="datasets", null=True)
    created_at = models.DateTimeField("дата и время", auto_now_add=True)
    is_processed = models.BooleanField("модель была запущена", default=False)
    report = models.TextField(
        "отчет",
        blank=True,
        null=True,
        help_text="""
        <i>Этот отчет представляет собой результат работы модели классификации,
        в данном случае — случайного леса (RandomForestClassifier).</i><br><br>
    
        Основные метрики<br><br>
        1. <b>precision</b> (точность):<br><br>
           - Это доля правильно предсказанных положительных событий из всех событий, предсказанных как положительные.<br>
           - Высокая точность означает, что ложных срабатываний мало.\n<br><br>
        
        2. <b>recall</b> (полнота, или чувствительность):<br><br>
           - Это доля правильно предсказанных положительных событий из всех реальных положительных событий.<br>
           - Высокая полнота означает, что модель выявила большинство положительных событий.<br><br>
        
        3. <b>f1-score</b>:<br><br>
           - Среднее гармоническое между точностью и полнотой. F1-метрика балансирует соотношение между ними.<br>
           - Высокое значение f1-score означает, что и точность, и полнота высоки.<br><br>
        4. <b>support</b>:<br><br>
           - Это количество истинных примеров данного класса в выборке.
    """
    )

    def __str__(self) -> str:
        return f"Предсказание №{self.pk}"

    class Meta:
        verbose_name = "результат работы модели"
        verbose_name_plural = "результаты/исходники работы модели"
