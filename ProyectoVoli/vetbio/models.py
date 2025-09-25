from django.db import models


# Create your models here.

class Tutor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.email} {self.telefono}"

class Mascota(models.Model):
    ESPECIES_CHOICES = [('perro', 'Perro'),('gato', 'Gato'), ('otro', 'Otro')]
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="mascotas")
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=10, choices=ESPECIES_CHOICES,default='perro')
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.tutor.nombre} - {self.nombre} ({self.especie})"


class Servicio(models.Model):
    TIPO_CHOICES = [('consulta', 'Consulta'), ('vacuna', 'Vacuna'), ('procedimiento', 'Procedimiento'),]
    nombre = models.CharField(max_length=100, unique=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
    
class Atencion(models.Model):
    ATENCION_CHOICES = [('pendiente', 'Pendiente'), ('completada', 'Completada'), ('cancelada', 'Cancelada')]
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name="atenciones")
    fecha = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ATENCION_CHOICES)
    monto_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Atencion de {self.mascota.nombre} el {self.fecha} - {self.estado}"
    
class DetalleAtencion(models.Model):
    atencion = models.ForeignKey(Atencion, on_delete=models.CASCADE, related_name="detalles")
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    monto_lineal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.servicio.nombre} para {self.atencion.mascota.nombre}"