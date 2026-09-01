# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alimentos(models.Model):
    grupo = models.ForeignKey('GruposAlimentos', models.DO_NOTHING)
    subgrupo = models.CharField(max_length=150, blank=True, null=True)
    nombre = models.CharField(max_length=150)
    poblacion = models.TextField()  # This field type is a guess.
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
    creado_en = models.DateTimeField()

    # A unique constraint could not be introspected.
    class Meta:
        managed = False
        db_table = 'alimentos'
        unique_together = (('grupo', 'poblacion'),)


class GruposAlimentos(models.Model):
    nombre = models.CharField(unique=True, max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupos_alimentos'
