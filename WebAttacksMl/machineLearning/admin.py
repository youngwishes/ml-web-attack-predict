from urllib.request import Request
from django.contrib import admin
from django.db.models import QuerySet
from machineLearning.models import MachineLearningResult
from machineLearning.service import MLService


def run_ml_model_instance(modeladmin: admin.ModelAdmin, request: Request, queryset: QuerySet) -> None:
    instance = queryset.first()
    MLService.process(instance)


@admin.register(MachineLearningResult)
class MachineLearningResultAdmin(admin.ModelAdmin):
    list_display = ["pk", "accuracy", "dataset", "created_at"]
    readonly_fields = ("accuracy", "created_at", "is_processed")
    actions = (run_ml_model_instance,)

    run_ml_model_instance.short_description = "Запустить"
