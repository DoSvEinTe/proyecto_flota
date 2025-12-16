from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Conductor, Pasajero, Lugar
from flota.models import Bus
from viajes.models import Viaje, ViajePasajero


class Command(BaseCommand):
    help = 'Carga datos de prueba en la base de datos (Buses, Conductores, Viajes, Pasajeros)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Elimina todos los datos de prueba antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['clean']:
            self.stdout.write(self.style.WARNING('\n🗑️  Limpiando datos de prueba anteriores...'))
            
            # Eliminar en orden para respetar las relaciones
            deleted_viaje_pasajero = ViajePasajero.objects.all().delete()[0]
            deleted_viajes = Viaje.objects.all().delete()[0]
            deleted_pasajeros = Pasajero.objects.all().delete()[0]
            deleted_buses = Bus.objects.all().delete()[0]
            deleted_conductores = Conductor.objects.all().delete()[0]
            deleted_lugares = Lugar.objects.all().delete()[0]
            
            self.stdout.write(f'  ✅ Eliminados: {deleted_viaje_pasajero} asignaciones, {deleted_viajes} viajes, {deleted_pasajeros} pasajeros, {deleted_buses} buses, {deleted_conductores} conductores, {deleted_lugares} lugares')
        
        self.stdout.write(self.style.SUCCESS('\n🚀 Iniciando carga de datos de prueba...'))
        
        # Crear Conductores
        self.stdout.write('\n👤 Creando conductores...')
        conductores_data = [
            {
                'nombre': 'Juan',
                'apellido': 'Pérez',
                'cedula': '12345678-9',
                'email': 'juan.perez@flota.com',
                'telefono': '+56912345678',
                'fecha_contratacion': timezone.now().date() - timedelta(days=365),
                'licencias': 'A3, B',
                'activo': True
            },
            {
                'nombre': 'María',
                'apellido': 'González',
                'cedula': '98765432-1',
                'email': 'maria.gonzalez@flota.com',
                'telefono': '+56987654321',
                'fecha_contratacion': timezone.now().date() - timedelta(days=730),
                'licencias': 'A2, A3',
                'activo': True
            },
            {
                'nombre': 'Carlos',
                'apellido': 'Rodríguez',
                'cedula': '11223344-5',
                'email': 'carlos.rodriguez@flota.com',
                'telefono': '+56911223344',
                'fecha_contratacion': timezone.now().date() - timedelta(days=180),
                'licencias': 'A3',
                'activo': True
            },
            {
                'nombre': 'Ana',
                'apellido': 'Martínez',
                'cedula': '55667788-9',
                'email': 'ana.martinez@flota.com',
                'telefono': '+56955667788',
                'fecha_contratacion': timezone.now().date() - timedelta(days=90),
                'licencias': 'A2, B',
                'activo': True
            },
        ]
        
        conductores = []
        for data in conductores_data:
            conductor, created = Conductor.objects.get_or_create(
                cedula=data['cedula'],
                defaults=data
            )
            conductores.append(conductor)
            if created:
                self.stdout.write(f'  ✅ Conductor creado: {conductor.nombre} {conductor.apellido}')
            else:
                self.stdout.write(f'  ℹ️  Conductor ya existe: {conductor.nombre} {conductor.apellido}')
        
        # Crear Buses
        self.stdout.write('\n🚌 Creando buses...')
        buses_data = [
            {
                'placa': 'AA2233',
                'modelo': 'Mercedes-Benz Sprinter',
                'marca': 'Mercedes-Benz',
                'año_fabricacion': 2020,
                'capacidad_pasajeros': 20,
                'numero_motor': 'MB2020-001',
                'numero_chasis': 'CHASIS-001',
                'kilometraje_ingreso': 15000,
                'estado': 'activo',
                'fecha_adquisicion': timezone.now().date() - timedelta(days=1460)  # ~4 años
            },
            {
                'placa': 'BB4455',
                'modelo': 'Iveco Daily',
                'marca': 'Iveco',
                'año_fabricacion': 2019,
                'capacidad_pasajeros': 16,
                'numero_motor': 'IVECO2019-002',
                'numero_chasis': 'CHASIS-002',
                'kilometraje_ingreso': 28000,
                'estado': 'activo',
                'fecha_adquisicion': timezone.now().date() - timedelta(days=1825)  # ~5 años
            },
            {
                'placa': 'CC6677',
                'modelo': 'Ford Transit',
                'marca': 'Ford',
                'año_fabricacion': 2021,
                'capacidad_pasajeros': 15,
                'numero_motor': 'FORD2021-003',
                'numero_chasis': 'CHASIS-003',
                'kilometraje_ingreso': 8500,
                'estado': 'activo',
                'fecha_adquisicion': timezone.now().date() - timedelta(days=1095)  # ~3 años
            },
            {
                'placa': 'DD8899',
                'modelo': 'Volkswagen Crafter',
                'marca': 'Volkswagen',
                'año_fabricacion': 2018,
                'capacidad_pasajeros': 18,
                'numero_motor': 'VW2018-004',
                'numero_chasis': 'CHASIS-004',
                'kilometraje_ingreso': 45000,
                'estado': 'activo',
                'fecha_adquisicion': timezone.now().date() - timedelta(days=2190)  # ~6 años
            },
            {
                'placa': 'EE1122',
                'modelo': 'Hyundai H350',
                'marca': 'Hyundai',
                'año_fabricacion': 2022,
                'capacidad_pasajeros': 17,
                'numero_motor': 'HY2022-005',
                'numero_chasis': 'CHASIS-005',
                'kilometraje_ingreso': 3200,
                'estado': 'activo',
                'fecha_adquisicion': timezone.now().date() - timedelta(days=730)  # ~2 años
            },
        ]
        
        buses = []
        for data in buses_data:
            bus, created = Bus.objects.get_or_create(
                placa=data['placa'],
                defaults=data
            )
            buses.append(bus)
            if created:
                self.stdout.write(f'  ✅ Bus creado: {bus.placa} - {bus.modelo}')
            else:
                self.stdout.write(f'  ℹ️  Bus ya existe: {bus.placa} - {bus.modelo}')
        
        # Crear Lugares
        self.stdout.write('\n📍 Creando lugares...')
        lugares_data = [
            {
                'nombre': 'Terminal Central',
                'ciudad': 'Santiago',
                'provincia': 'Santiago',
                'pais': 'Chile',
                'latitud': -33.4489,
                'longitud': -70.6693
            },
            {
                'nombre': 'Terminal Valparaíso',
                'ciudad': 'Valparaíso',
                'provincia': 'Valparaíso',
                'pais': 'Chile',
                'latitud': -33.0472,
                'longitud': -71.6127
            },
            {
                'nombre': 'Terminal Viña del Mar',
                'ciudad': 'Viña del Mar',
                'provincia': 'Valparaíso',
                'pais': 'Chile',
                'latitud': -33.0245,
                'longitud': -71.5518
            },
            {
                'nombre': 'Terminal Rancagua',
                'ciudad': 'Rancagua',
                'provincia': 'Cachapoal',
                'pais': 'Chile',
                'latitud': -34.1704,
                'longitud': -70.7407
            },
            {
                'nombre': 'Terminal Concepción',
                'ciudad': 'Concepción',
                'provincia': 'Concepción',
                'pais': 'Chile',
                'latitud': -36.8270,
                'longitud': -73.0498
            },
        ]
        
        lugares = []
        for data in lugares_data:
            lugar, created = Lugar.objects.get_or_create(
                nombre=data['nombre'],
                ciudad=data['ciudad'],
                defaults=data
            )
            lugares.append(lugar)
            if created:
                self.stdout.write(f'  ✅ Lugar creado: {lugar.nombre}, {lugar.ciudad}')
            else:
                self.stdout.write(f'  ℹ️  Lugar ya existe: {lugar.nombre}, {lugar.ciudad}')
        
        # Crear Pasajeros
        self.stdout.write('\n👥 Creando pasajeros...')
        pasajeros_data = [
            {
                'nombre_completo': 'Pedro Sánchez López',
                'rut': '15234567-8',
                'telefono': '+56915234567',
                'correo': 'pedro.sanchez@email.com'
            },
            {
                'nombre_completo': 'Laura Fernández Castro',
                'rut': '16345678-9',
                'telefono': '+56916345678',
                'correo': 'laura.fernandez@email.com'
            },
            {
                'nombre_completo': 'Diego Torres Muñoz',
                'rut': '17456789-0',
                'telefono': '+56917456789',
                'correo': 'diego.torres@email.com'
            },
            {
                'nombre_completo': 'Carmen Silva Rojas',
                'rut': '18567890-1',
                'telefono': '+56918567890',
                'correo': 'carmen.silva@email.com'
            },
            {
                'nombre_completo': 'Roberto Vargas Díaz',
                'rut': '19678901-2',
                'telefono': '+56919678901',
                'correo': 'roberto.vargas@email.com'
            },
            {
                'nombre_completo': 'Patricia Morales Vera',
                'rut': '20789012-3',
                'telefono': '+56920789012',
                'correo': 'patricia.morales@email.com'
            },
            {
                'nombre_completo': 'John Smith',
                'pasaporte': 'US123456789',
                'telefono': '+1234567890',
                'correo': 'john.smith@email.com'
            },
            {
                'nombre_completo': 'Maria García',
                'pasaporte': 'AR987654321',
                'telefono': '+5491123456789',
                'correo': 'maria.garcia@email.com'
            },
        ]
        
        pasajeros = []
        for data in pasajeros_data:
            if 'rut' in data and data.get('rut'):
                pasajero, created = Pasajero.objects.get_or_create(
                    rut=data['rut'],
                    defaults=data
                )
            elif 'pasaporte' in data and data.get('pasaporte'):
                pasajero, created = Pasajero.objects.get_or_create(
                    pasaporte=data['pasaporte'],
                    defaults=data
                )
            else:
                continue
            pasajeros.append(pasajero)
            if created:
                doc = data.get('rut') or data.get('pasaporte')
                self.stdout.write(f'  ✅ Pasajero creado: {pasajero.nombre_completo} ({doc})')
            else:
                self.stdout.write(f'  ℹ️  Pasajero ya existe: {pasajero.nombre_completo}')
        
        # Crear Viajes
        self.stdout.write('\n🚍 Creando viajes...')
        
        # Viaje 1: IDA Y VUELTA Santiago-Valparaíso
        viaje_ida_data = {
            'bus': buses[0],
            'conductor': conductores[0],
            'origen_nombre': 'Terminal Central',
            'origen_ciudad': 'Santiago',
            'origen_provincia': 'Santiago',
            'origen_pais': 'Chile',
            'latitud_origen': -33.4489,
            'longitud_origen': -70.6693,
            'destino_nombre': 'Terminal Valparaíso',
            'destino_ciudad': 'Valparaíso',
            'destino_provincia': 'Valparaíso',
            'destino_pais': 'Chile',
            'latitud_destino': -33.0472,
            'longitud_destino': -71.6127,
            'fecha_salida': timezone.now() + timedelta(days=1, hours=8),
            'fecha_llegada_estimada': timezone.now() + timedelta(days=1, hours=10),
            'distancia_km': 120.5,
            'estado': 'programado',
            'es_ida_vuelta': True,
            'tipo_trayecto': 'ida',
            'observaciones': 'Viaje de ida y vuelta Santiago-Valparaíso'
        }
        
        # Buscar viaje de ida existente
        viaje_ida = Viaje.objects.filter(
            bus=viaje_ida_data['bus'],
            conductor=viaje_ida_data['conductor'],
            origen_ciudad=viaje_ida_data['origen_ciudad'],
            destino_ciudad=viaje_ida_data['destino_ciudad'],
            estado='programado',
            tipo_trayecto='ida'
        ).first()
        
        if not viaje_ida:
            viaje_ida = Viaje.objects.create(**viaje_ida_data)
            
            # Crear viaje de vuelta
            viaje_vuelta = Viaje.objects.create(
                bus=viaje_ida.bus,
                conductor=viaje_ida.conductor,
                origen_nombre=viaje_ida.destino_nombre,
                origen_ciudad=viaje_ida.destino_ciudad,
                origen_provincia=viaje_ida.destino_provincia,
                origen_pais=viaje_ida.destino_pais,
                latitud_origen=viaje_ida.latitud_destino,
                longitud_origen=viaje_ida.longitud_destino,
                destino_nombre=viaje_ida.origen_nombre,
                destino_ciudad=viaje_ida.origen_ciudad,
                destino_provincia=viaje_ida.origen_provincia,
                destino_pais=viaje_ida.origen_pais,
                latitud_destino=viaje_ida.latitud_origen,
                longitud_destino=viaje_ida.longitud_origen,
                fecha_salida=viaje_ida.fecha_llegada_estimada + timedelta(minutes=30),
                fecha_llegada_estimada=viaje_ida.fecha_llegada_estimada + timedelta(hours=2, minutes=30),
                distancia_km=viaje_ida.distancia_km,
                estado='programado',
                es_ida_vuelta=True,
                tipo_trayecto='vuelta',
                observaciones='Viaje de vuelta Valparaíso-Santiago'
            )
            
            # Vincular ambos viajes
            viaje_ida.viaje_relacionado = viaje_vuelta
            viaje_ida.save(update_fields=['viaje_relacionado'])
            viaje_vuelta.viaje_relacionado = viaje_ida
            viaje_vuelta.save(update_fields=['viaje_relacionado'])
            
            self.stdout.write(f'  ✅ Viaje 1 IDA creado: {viaje_ida.origen_ciudad} → {viaje_ida.destino_ciudad}')
            self.stdout.write(f'  ✅ Viaje 1 VUELTA creado: {viaje_vuelta.origen_ciudad} → {viaje_vuelta.destino_ciudad}')
        else:
            self.stdout.write(f'  ℹ️  Viaje 1 ya existe: {viaje_ida.origen_ciudad} → {viaje_ida.destino_ciudad}')
        
        # Resto de viajes simples
        viajes_data = [
            {
                'bus': buses[1],
                'conductor': conductores[1],
                'origen_nombre': 'Terminal Santiago',
                'origen_ciudad': 'Santiago',
                'origen_provincia': 'Santiago',
                'origen_pais': 'Chile',
                'latitud_origen': -33.4489,
                'longitud_origen': -70.6693,
                'destino_nombre': 'Terminal Viña del Mar',
                'destino_ciudad': 'Viña del Mar',
                'destino_provincia': 'Valparaíso',
                'destino_pais': 'Chile',
                'latitud_destino': -33.0245,
                'longitud_destino': -71.5518,
                'fecha_salida': timezone.now() + timedelta(days=2, hours=9),
                'fecha_llegada_estimada': timezone.now() + timedelta(days=2, hours=11, minutes=30),
                'distancia_km': 130.8,
                'estado': 'programado',
                'observaciones': 'Viaje especial con grupo turístico'
            },
            {
                'bus': buses[2],
                'conductor': conductores[2],
                'origen_nombre': 'Terminal Santiago',
                'origen_ciudad': 'Santiago',
                'origen_provincia': 'Santiago',
                'origen_pais': 'Chile',
                'latitud_origen': -33.4489,
                'longitud_origen': -70.6693,
                'destino_nombre': 'Terminal Rancagua',
                'destino_ciudad': 'Rancagua',
                'destino_provincia': 'Cachapoal',
                'destino_pais': 'Chile',
                'latitud_destino': -34.1704,
                'longitud_destino': -70.7407,
                'fecha_salida': timezone.now() + timedelta(days=3, hours=7),
                'fecha_llegada_estimada': timezone.now() + timedelta(days=3, hours=8, minutes=30),
                'distancia_km': 87.3,
                'estado': 'programado',
                'observaciones': 'Viaje diario'
            },
            {
                'bus': buses[3],
                'conductor': conductores[3],
                'origen_nombre': 'Terminal Santiago',
                'origen_ciudad': 'Santiago',
                'origen_provincia': 'Santiago',
                'origen_pais': 'Chile',
                'latitud_origen': -33.4489,
                'longitud_origen': -70.6693,
                'destino_nombre': 'Terminal Concepción',
                'destino_ciudad': 'Concepción',
                'destino_provincia': 'Concepción',
                'destino_pais': 'Chile',
                'latitud_destino': -36.8270,
                'longitud_destino': -73.0498,
                'fecha_salida': timezone.now() + timedelta(days=4, hours=6),
                'fecha_llegada_estimada': timezone.now() + timedelta(days=4, hours=12),
                'distancia_km': 515.2,
                'estado': 'programado',
                'observaciones': 'Viaje interurbano largo'
            },
            {
                'bus': buses[4],
                'conductor': conductores[0],
                'origen_nombre': 'Terminal Valparaíso',
                'origen_ciudad': 'Valparaíso',
                'origen_provincia': 'Valparaíso',
                'origen_pais': 'Chile',
                'latitud_origen': -33.0472,
                'longitud_origen': -71.6127,
                'destino_nombre': 'Terminal Viña del Mar',
                'destino_ciudad': 'Viña del Mar',
                'destino_provincia': 'Valparaíso',
                'destino_pais': 'Chile',
                'latitud_destino': -33.0245,
                'longitud_destino': -71.5518,
                'fecha_salida': timezone.now() + timedelta(days=5, hours=10),
                'fecha_llegada_estimada': timezone.now() + timedelta(days=5, hours=10, minutes=30),
                'distancia_km': 8.5,
                'estado': 'programado',
                'observaciones': 'Viaje corto entre ciudades costeras'
            },
        ]
        
        viajes_creados = [viaje_ida] if viaje_ida else []
        
        for i, data in enumerate(viajes_data):
            # Buscar viaje existente por origen-destino-bus-conductor
            viaje = Viaje.objects.filter(
                bus=data['bus'],
                conductor=data['conductor'],
                origen_ciudad=data['origen_ciudad'],
                destino_ciudad=data['destino_ciudad'],
                estado='programado'
            ).first()
            
            if viaje:
                # Actualizar fechas si el viaje existe
                viaje.fecha_salida = data['fecha_salida']
                viaje.fecha_llegada_estimada = data['fecha_llegada_estimada']
                viaje.save()
                viajes_creados.append(viaje)
                self.stdout.write(f'  ℹ️  Viaje {i+2} ya existe (fechas actualizadas): {viaje.origen_ciudad} → {viaje.destino_ciudad}')
            else:
                # Crear nuevo viaje
                viaje = Viaje.objects.create(**data)
                viajes_creados.append(viaje)
                self.stdout.write(f'  ✅ Viaje {i+2} creado: {viaje.origen_ciudad} → {viaje.destino_ciudad}')
        
        # Asignar pasajeros a viajes
        self.stdout.write('\n🎫 Asignando pasajeros a viajes...')
        if viajes_creados and pasajeros:
            # Viaje 1 (Santiago-Valparaíso): 4 pasajeros
            if len(viajes_creados) > 0 and len(pasajeros) >= 4:
                for idx, pasajero in enumerate(pasajeros[:4], 1):
                    viaje_pasajero, created = ViajePasajero.objects.get_or_create(
                        viaje=viajes_creados[0],
                        pasajero=pasajero,
                        defaults={'asiento': f'A{idx}'}
                    )
                    if created:
                        self.stdout.write(f'  ✅ {pasajero.nombre_completo} asignado a Viaje 1 (Asiento A{idx})')
            
            # Viaje 2 (Santiago-Viña del Mar): 3 pasajeros
            if len(viajes_creados) > 1 and len(pasajeros) >= 7:
                for idx, pasajero in enumerate(pasajeros[4:7], 1):
                    viaje_pasajero, created = ViajePasajero.objects.get_or_create(
                        viaje=viajes_creados[1],
                        pasajero=pasajero,
                        defaults={'asiento': f'B{idx}'}
                    )
                    if created:
                        self.stdout.write(f'  ✅ {pasajero.nombre_completo} asignado a Viaje 2 (Asiento B{idx})')
            
            # Viaje 3 (Santiago-Rancagua): 2 pasajeros (incluyendo extranjeros)
            if len(viajes_creados) > 2 and len(pasajeros) >= 8:
                for idx, pasajero in enumerate(pasajeros[6:8], 1):
                    viaje_pasajero, created = ViajePasajero.objects.get_or_create(
                        viaje=viajes_creados[2],
                        pasajero=pasajero,
                        defaults={'asiento': f'C{idx}'}
                    )
                    if created:
                        self.stdout.write(f'  ✅ {pasajero.nombre_completo} asignado a Viaje 3 (Asiento C{idx})')
            
            # Viaje 4 (Santiago-Concepción): 5 pasajeros (viaje largo)
            if len(viajes_creados) > 3 and len(pasajeros) >= 5:
                for idx, pasajero in enumerate(pasajeros[:5], 1):
                    viaje_pasajero, created = ViajePasajero.objects.get_or_create(
                        viaje=viajes_creados[3],
                        pasajero=pasajero,
                        defaults={'asiento': f'D{idx}'}
                    )
                    if created:
                        self.stdout.write(f'  ✅ {pasajero.nombre_completo} asignado a Viaje 4 (Asiento D{idx})')
            
            # Viaje 5 (Valparaíso-Viña): 2 pasajeros (viaje corto)
            if len(viajes_creados) > 4 and len(pasajeros) >= 2:
                for idx, pasajero in enumerate(pasajeros[:2], 1):
                    viaje_pasajero, created = ViajePasajero.objects.get_or_create(
                        viaje=viajes_creados[4],
                        pasajero=pasajero,
                        defaults={'asiento': f'E{idx}'}
                    )
                    if created:
                        self.stdout.write(f'  ✅ {pasajero.nombre_completo} asignado a Viaje 5 (Asiento E{idx})')
        
        # Resumen
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ Datos de prueba cargados exitosamente!'))
        self.stdout.write('='*60)
        self.stdout.write(f'📊 Resumen:')
        self.stdout.write(f'  • Conductores: {Conductor.objects.count()}')
        self.stdout.write(f'  • Buses: {Bus.objects.count()}')
        self.stdout.write(f'  • Lugares: {Lugar.objects.count()}')
        self.stdout.write(f'  • Pasajeros: {Pasajero.objects.count()}')
        self.stdout.write(f'  • Viajes: {Viaje.objects.count()}')
        self.stdout.write(f'  • Asignaciones Pasajero-Viaje: {ViajePasajero.objects.count()}')
        self.stdout.write('='*60)
