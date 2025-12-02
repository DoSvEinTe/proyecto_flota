from costos.models import Peaje

# Eliminar peajes que no están asociados a ningún registro de costos
Peaje.objects.filter(costos_viaje__isnull=True).delete()
print('Peajes huérfanos eliminados correctamente.')
