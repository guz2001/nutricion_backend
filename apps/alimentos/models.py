from django.db import models

# Create your models here.

class GrupoAlimento(models.Model):
    nombre=models.CharField(max_length=100,unique=True)#s el nombre del grupo, como "Frutas". Cada nombre debe ser único, por eso dice unique=True.
    descripcion=models.TextField(blank=True,null=True)#descripcion: Describe lo que incluye ese grupo. Puede estar vacía o no (por eso dice blank=True y null=True).

    class Meta:
        managed=False #indica que python no tendra poder sobre esta base de datos
        db_table='grupos_alimentos' #EL nombre exacto de la tabla en la db

    def __str__(self):
        return self.nombre # devuelve el nombre del grupo

"""
    Como PostgreSQL maneja el ENUM a su manera y Django no tiene un tipo ENUM nativo simple,
    lo representamos como texto con una lista fija de opciones válidas. 
    Django valida contra esa lista en formularios y en el admin, pero a nivel de base de datos sigue siendo el ENUM real de PostgreSQL — Django no lo toca.
"""  
class Alimento(models.Model):
    POBLACION_CHOICES = [
         ('niños_y_adultos', 'Niños y adultos'),
        ('adultos', 'Adultos'),
        ('niños', 'Niños'),
        ('menores_de_dos_anios', 'Menores de dos años'),

    ]#Se crea esta tupla para garantinzar que las opciones de la columna poblacion solo sean estas

    grupo = models.ForeignKey(GrupoAlimento, on_delete=models.DO_NOTHING)
    subgrupo = models.CharField(max_length=150, blank=True, null=True)
    nombre = models.CharField(max_length=150)
    poblacion = models.CharField(max_length=30, choices=POBLACION_CHOICES)
    porcion_g = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    unidad_medida = models.TextField(blank=True, null=True)
    kcal = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    proteina_g = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    grasa_total_g = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    ags_g = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    agm_g = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    agp_g = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    colesterol_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    cho_g = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    fibra_g = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    calcio_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    fosforo_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    hierro_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    sodio_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    potasio_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    magnesio_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    zinc_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    cobre_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    manganeso_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    vit_a_er = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    tiamina_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    riboflavina_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    niacina_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    ac_pantotenico_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    piridoxina_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    folato_mcg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    vit_b12_mcg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    vit_c_mg = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    creado_en = models.DateTimeField()#Dato de tiempo en formato de fecha sql entonces se deja asi en python


    class Meta:
        managed=False #indica que python no tendra poder sobre esta base de datos
        db_table='alimentos'
        unique_together=(('grupo', 'subgrupo', 'nombre', 'poblacion', 'porcion_g', 'unidad_medida'),) #EL nombre exacto de la tabla en la db


    def __str__(self):
        return self.nombre # devuelve el nombre del grupo