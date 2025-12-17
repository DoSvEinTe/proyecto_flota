"""
Script para limpiar todos los datos de viajes y costos.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_flota.settings')
django.setup()

from viajes.models import Viaje, ViajePasajero
from costos.models import CostosViaje, Peaje, PuntoRecarga

def limpiar_datos():
    """Elimina todos los viajes y datos relacionados."""
    
    print("\n🗑️  Limpiando datos de viajes y costos...\n")
    
    # Contar registros antes de eliminar
    total_viajes = Viaje.objects.count()
    total_costos = CostosViaje.objects.count()
    total_peajes = Peaje.objects.count()
    total_recargas = PuntoRecarga.objects.count()
    total_viaje_pasajeros = ViajePasajero.objects.count()
    
    print(f"📊 Registros actuales:")
    print(f"   - Viajes: {total_viajes}")
    print(f"   - Costos de viajes: {total_costos}")
    print(f"   - Peajes: {total_peajes}")
    print(f"   - Puntos de recarga: {total_recargas}")
    print(f"   - Asignaciones viaje-pasajero: {total_viaje_pasajeros}")
    
    respuesta = input("\n⚠️  ¿Estás seguro de que deseas eliminar todos estos datos? (si/no): ")
    
    if respuesta.lower() != 'si':
        print("\n❌ Operación cancelada.")
        return
    
    print("\n🔥 Eliminando datos...\n")
    
    # Eliminar en orden para evitar problemas de integridad
    ViajePasajero.objects.all().delete()
    print("✅ Asignaciones viaje-pasajero eliminadas")
    
    PuntoRecarga.objects.all().delete()
    print("✅ Puntos de recarga eliminados")
    
    Peaje.objects.all().delete()
    print("✅ Peajes eliminados")
    
    CostosViaje.objects.all().delete()
    print("✅ Costos de viajes eliminados")
    
    Viaje.objects.all().delete()
    print("✅ Viajes eliminados")
    
    print("\n✨ ¡Todos los datos han sido eliminados exitosamente!")
    print("📝 Ahora puedes comenzar a testear desde cero.\n")

if __name__ == '__main__':
    try:
        limpiar_datos()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
