from django.db import models
from rest_framework import serializers
from apps.alimentos.models import Alimento

class GrupoAlimentoSerializer(serializers.Models):
    class Meta:
        model=Alimento
        fields=