from django.db import models

class Responsable(models.Model):
    id_responsable = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    especialidad = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Maquina(models.Model):
    id_maquina = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=[('Operativa', 'Operativa'), ('En mantenimiento', 'En mantenimiento'), ('No operativa', 'No operativa')], default='Operativa')

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - {self.estado}"
    
class Mantencion(models.Model):
    id_mantencion = models.AutoField(primary_key=True)
    id_maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    id_responsable = models.ForeignKey(Responsable, on_delete= models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f"Mantencion de {self.id_maquina.nombre} el {self.fecha} por {self.id_responsable.nombre} {self.id_responsable.apellido}"