from django.core.management.base import BaseCommand
from costos.models import CostosViaje
from viajes.models import Viaje


class Command(BaseCommand):
    help = 'Actualiza los estados de los viajes con costos registrados a COMPLETADO'

    def handle(self, *args, **options):
        # Obtener todos los viajes que tienen costos registrados
        viajes_con_costos = CostosViaje.objects.values_list('viaje_id', flat=True)
        
        # Actualizar el estado de estos viajes a 'completado'
        actualizados = Viaje.objects.filter(id__in=viajes_con_costos).exclude(estado='completado').update(estado='completado')
        
        self.stdout.write(
            self.style.SUCCESS(f'Se actualizaron {actualizados} viajes a estado COMPLETADO')
        )
