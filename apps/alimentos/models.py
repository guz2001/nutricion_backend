from django.db import models

# Create your models here.

class GrupoAlimento(models.Model):#s el nombre del grupo, como "Frutas". Cada nombre debe ser único, por eso dice unique=True.s
    nombre=models.CharField(max_length=100,unique=True)
    descripcion=models.TextField(blank=True,null=True)

    class Meta:
        managed=False
        db_table='grupos_alimentos'

    def __str__(self):
        return self.nombre
class Alimento(models.Model):
    POBLACION_CHOICES = []