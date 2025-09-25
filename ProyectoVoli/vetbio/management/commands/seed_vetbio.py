from django.core.management.base import BaseCommand
from vetbio.models import Tutor, Mascota, Servicio, Atencion, DetalleAtencion
from django.utils import timezone
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed database with sample data for vetbio app'

    def handle(self, *args, **kwargs):
        fake = Faker('es_CL')

        # Limpiar datos existentes
        DetalleAtencion.objects.all().delete()
        Atencion.objects.all().delete()
        Mascota.objects.all().delete()
        Tutor.objects.all().delete()
        Servicio.objects.all().delete()

        # Crear servicios básicos
        servicios = []
        tipos = ['consulta', 'vacuna', 'procedimiento']
        for i in range(5):
            servicio = Servicio.objects.create(
                nombre=fake.unique.word().capitalize(),
                precio_base=round(random.uniform(5000, 30000), 2),
                tipo=random.choice(tipos)
            )
            servicios.append(servicio)

        # Crear tutores y mascotas
        tutores = []
        for _ in range(10):
            tutor = Tutor.objects.create(
                nombre=fake.name(),
                email=fake.unique.email(),
                telefono=fake.msisdn()[:9]
            )
            tutores.append(tutor)
            for _ in range(random.randint(1, 3)):
                Mascota.objects.create(
                    tutor=tutor,
                    nombre=fake.first_name(),
                    especie=random.choice(['perro', 'gato', 'otro']),
                    fecha_nacimiento=fake.date_of_birth(minimum_age=1, maximum_age=15)
                )

        mascotas = Mascota.objects.all()

        # Crear atenciones y detalles
        for _ in range(30):
            mascota = random.choice(mascotas)
            atencion = Atencion.objects.create(
                mascota=mascota,
                fecha=fake.date_between(start_date='-1y', end_date='today'),
                estado=random.choice(['pendiente', 'completada', 'cancelada']),
                monto_total=0
            )
            detalles = []
            for _ in range(random.randint(1, 3)):
                servicio = random.choice(servicios)
                cantidad = random.randint(1, 2)
                monto_lineal = servicio.precio_base * cantidad
                detalle = DetalleAtencion.objects.create(
                    atencion=atencion,
                    servicio=servicio,
                    cantidad=cantidad,
                    monto_lineal=monto_lineal
                )
                detalles.append(detalle)
            # Actualizar monto_total
            atencion.monto_total = sum(d.monto_lineal for d in detalles)
            atencion.save()

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo creados exitosamente.'))