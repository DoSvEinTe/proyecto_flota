from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import timedelta, date

from flota.models import Bus, DocumentoVehiculo, Mantenimiento
from core.models import Conductor, Lugar, Pasajero
from viajes.models import Viaje
from costos.models import CostosViaje


class Command(BaseCommand):
    help = 'Siembra datos de ejemplo para desarrollo: buses, conductores, lugares, pasajeros, viajes y costos.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Iniciando siembra de datos de ejemplo...')

        # Buses
        buses_data = [
            {
                'placa': 'PQR-123',
                'marca': 'Mercedes',
                'modelo': 'Sprinter 2018',
                'año_fabricacion': 2018,
                'capacidad_pasajeros': 20,
                'kilometraje_inicial': 120000,
                'numero_chasis': 'CHS-PQR-123',
                'numero_motor': 'ENG-PQR-01',
                'estado': 'activo',
                'fecha_adquisicion': date.today() - timedelta(days=365 * 4),
            },
            {
                'placa': 'ABC-999',
                'marca': 'Volvo',
                'modelo': 'B9R',
                'año_fabricacion': 2015,
                'capacidad_pasajeros': 45,
                'kilometraje_inicial': 300000,
                'numero_chasis': 'CHS-ABC-999',
                'numero_motor': 'ENG-ABC-09',
                'estado': 'activo',
                'fecha_adquisicion': date.today() - timedelta(days=365 * 6),
            },
            {
                'placa': 'DEF-456',
                'marca': 'Scania',
                'modelo': 'K360',
                'año_fabricacion': 2017,
                'capacidad_pasajeros': 40,
                'kilometraje_inicial': 200000,
                'numero_chasis': 'CHS-DEF-456',
                'numero_motor': 'ENG-DEF-02',
                'estado': 'activo',
                'fecha_adquisicion': date.today() - timedelta(days=365 * 5),
            },
            {
                'placa': 'GHI-321',
                'marca': 'Iveco',
                'modelo': 'Urbanway',
                'año_fabricacion': 2019,
                'capacidad_pasajeros': 30,
                'kilometraje_inicial': 90000,
                'numero_chasis': 'CHS-GHI-321',
                'numero_motor': 'ENG-GHI-03',
                'estado': 'mantenimiento',
                'fecha_adquisicion': date.today() - timedelta(days=365 * 3),
            },
        ]

        buses = []
        for b in buses_data:
            bus, created = Bus.objects.get_or_create(
                placa=b['placa'],
                defaults={
                    'marca': b['marca'],
                    'modelo': b['modelo'],
                    'año_fabricacion': b['año_fabricacion'],
                    'capacidad_pasajeros': b['capacidad_pasajeros'],
                    'kilometraje_inicial': b['kilometraje_inicial'],
                    'numero_chasis': b['numero_chasis'],
                    'numero_motor': b['numero_motor'],
                    'estado': b['estado'],
                    'fecha_adquisicion': b['fecha_adquisicion'],
                }
            )
            buses.append(bus)
            self.stdout.write(f"{'Creado' if created else 'Existe'} Bus: {bus.placa}")

        # Conductores
        conductores_data = [
            {'nombre': 'Juan', 'apellido': 'Pérez', 'cedula': '0102030405', 'email': 'juan.perez@example.com', 'telefono': '0991234567', 'fecha_contratacion': date.today() - timedelta(days=400)},
            {'nombre': 'Luis', 'apellido': 'Martínez', 'cedula': '0102030406', 'email': 'luis.martinez@example.com', 'telefono': '0997654321', 'fecha_contratacion': date.today() - timedelta(days=200)},
            {'nombre': 'María', 'apellido': 'Ramos', 'cedula': '0102030407', 'email': 'maria.ramos@example.com', 'telefono': '0995556666', 'fecha_contratacion': date.today() - timedelta(days=150)},
            {'nombre': 'José', 'apellido': 'Vega', 'cedula': '0102030408', 'email': 'jose.vega@example.com', 'telefono': '0994443333', 'fecha_contratacion': date.today() - timedelta(days=30)},
        ]
        conductores = []
        for c in conductores_data:
            conductor, created = Conductor.objects.get_or_create(
                cedula=c['cedula'],
                defaults={
                    'nombre': c['nombre'],
                    'apellido': c['apellido'],
                    'email': c['email'],
                    'telefono': c['telefono'],
                    'fecha_contratacion': c['fecha_contratacion'],
                }
            )
            conductores.append(conductor)
            self.stdout.write(f"{'Creado' if created else 'Existe'} Conductor: {conductor}")

        # Lugares
        lugares_data = [
            {'nombre': 'Terminal Norte', 'ciudad': 'Quito', 'provincia': 'Pichincha'},
            {'nombre': 'Terminal Sur', 'ciudad': 'Guayaquil', 'provincia': 'Guayas'},
            {'nombre': 'Parada Central', 'ciudad': 'Cuenca', 'provincia': 'Azuay'},
            {'nombre': 'Estación Central', 'ciudad': 'Ambato', 'provincia': 'Tungurahua'},
            {'nombre': 'Parada Plaza', 'ciudad': 'Machala', 'provincia': 'El Oro'},
        ]
        lugares = []
        for l in lugares_data:
            lugar, created = Lugar.objects.get_or_create(
                nombre=l['nombre'], ciudad=l['ciudad'], defaults={'provincia': l.get('provincia', '')}
            )
            lugares.append(lugar)
            self.stdout.write(f"{'Creado' if created else 'Existe'} Lugar: {lugar}")

        # Pasajeros
        pasajeros_data = [
            {'nombre_completo': 'María López', 'rut': 'RUT001', 'telefono': '0991112222', 'correo': 'maria.lopez@example.com'},
            {'nombre_completo': 'Carlos Gómez', 'rut': 'RUT002', 'telefono': '0993334444', 'correo': 'carlos.gomez@example.com'},
            {'nombre_completo': 'Ana Torres', 'rut': 'RUT003', 'telefono': '0997778888', 'correo': 'ana.torres@example.com'},
            {'nombre_completo': 'Pedro Castillo', 'rut': 'RUT004', 'telefono': '0992223333', 'correo': 'pedro.castillo@example.com'},
            {'nombre_completo': 'Lucía Fernández', 'rut': 'RUT005', 'telefono': '0999990000', 'correo': 'lucia.fernandez@example.com'},
        ]
        pasajeros = []
        for p in pasajeros_data:
            pasajero, created = Pasajero.objects.get_or_create(
                rut=p['rut'],
                defaults={'nombre_completo': p['nombre_completo'], 'telefono': p['telefono'], 'correo': p['correo']}
            )
            pasajeros.append(pasajero)
            self.stdout.write(f"{'Creado' if created else 'Existe'} Pasajero: {pasajero}")

        # Viajes (crear uno por bus)
        now = timezone.now()
        for i, bus in enumerate(buses):
            conductor = conductores[i % len(conductores)]
            origen = lugares[i % len(lugares)]
            destino = lugares[(i + 1) % len(lugares)]
            fecha_salida = now + timedelta(days=1 + i)
            fecha_llegada = fecha_salida + timedelta(hours=3 + i)

            viaje, created = Viaje.objects.get_or_create(
                bus=bus,
                conductor=conductor,
                lugar_origen=origen,
                lugar_destino=destino,
                fecha_salida=fecha_salida,
                defaults={
                    'fecha_llegada_estimada': fecha_llegada,
                    'estado': ['programado', 'en_curso', 'completado', 'cancelado'][i % 4],
                    'observaciones': 'Viaje de ejemplo creado por seed_data',
                }
            )
            self.stdout.write(f"{'Creado' if created else 'Existe'} Viaje: {viaje}")

            # Asociar pasajeros al viaje (si no están)
            # Asociar algunos pasajeros al viaje (no todos)
            for j, pasajero in enumerate(pasajeros):
                if j % 2 == i % 2 and not viaje.pasajeros.filter(pk=pasajero.pk).exists():
                    viaje.pasajeros.add(pasajero)

            # Costos del viaje
            if not hasattr(viaje, 'costos'):
                costos = CostosViaje.objects.create(
                    viaje=viaje,
                    combustible=120.00 + i * 25,
                    mantenimiento=30.00 + i * 10,
                    peajes=5.00 + i * 2,
                    otros_costos=2.00,
                )
                costos.save()
                self.stdout.write(f"Creado Costos para viaje {viaje}")
            else:
                self.stdout.write(f"Costos ya existen para viaje {viaje}")

            # Crear algunos peajes de ejemplo
            try:
                from costos.models import Peaje
                for k in range(2):
                    Peaje.objects.get_or_create(
                        viaje=viaje,
                        lugar=f'Peaje {k+1} - {viaje.lugar_origen.ciudad}',
                        defaults={'monto': 2.50 + k, 'fecha_pago': now + timedelta(hours=k+1)}
                    )
            except Exception:
                pass

        # Documentos y mantenimientos ejemplo para todos los buses
        for idx, busx in enumerate(buses):
            docnum = f'SOAT-00{idx+1}'
            doc, created = DocumentoVehiculo.objects.get_or_create(
                bus=busx,
                tipo='soat',
                numero_documento=docnum,
                defaults={
                    'fecha_emision': date.today() - timedelta(days=200 + idx * 10),
                    'fecha_vencimiento': date.today() + timedelta(days=165 - idx * 5),
                    'observaciones': f'SOAT de ejemplo {idx+1}',
                }
            )
            self.stdout.write(f"{'Creado' if created else 'Existe'} DocumentoVehiculo: {doc}")

            mant, created = Mantenimiento.objects.get_or_create(
                bus=busx,
                tipo='preventivo',
                descripcion=f'Mantenimiento {idx+1} - revisión general',
                fecha_mantenimiento=date.today() - timedelta(days=30 + idx * 10),
                defaults={'kilometraje': busx.kilometraje_inicial + 100 * (idx+1), 'costo': 80.00 + idx * 20, 'taller': 'Taller Central'}
            )
            self.stdout.write(f"{'Creado' if created else 'Existe'} Mantenimiento: {mant}")

        self.stdout.write(self.style.SUCCESS('Siembra completada correctamente.'))
