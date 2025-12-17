"""
Script para corregir el tipo_trayecto de los viajes existentes.
Este script identifica y marca correctamente los viajes de ida y vuelta.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_flota.settings')
django.setup()

from viajes.models import Viaje

def fix_viajes_tipo_trayecto():
    """Corrige el tipo_trayecto de todos los viajes."""
    
    # Obtener todos los viajes
    viajes = Viaje.objects.all()
    actualizados = 0
    
    print(f"\n📊 Analizando {viajes.count()} viajes...\n")
    
    for viaje in viajes:
        cambio = False
        tipo_original = viaje.tipo_trayecto
        
        # Si tiene viaje relacionado y es_ida_vuelta es True
        if viaje.es_ida_vuelta:
            if viaje.viaje_relacionado:
                # Es un viaje de IDA
                if viaje.tipo_trayecto != 'ida':
                    viaje.tipo_trayecto = 'ida'
                    cambio = True
            else:
                # Buscar si este viaje es el viaje relacionado de otro
                viaje_padre = Viaje.objects.filter(viaje_relacionado=viaje).first()
                if viaje_padre:
                    # Es un viaje de VUELTA
                    if viaje.tipo_trayecto != 'vuelta':
                        viaje.tipo_trayecto = 'vuelta'
                        cambio = True
                else:
                    # Es un viaje de IDA sin vuelta creada todavía
                    if viaje.tipo_trayecto != 'ida':
                        viaje.tipo_trayecto = 'ida'
                        cambio = True
        else:
            # Es un viaje simple
            if viaje.tipo_trayecto != 'simple':
                viaje.tipo_trayecto = 'simple'
                cambio = True
        
        if cambio:
            viaje.save()
            actualizados += 1
            print(f"✅ Viaje #{viaje.id} ({viaje.bus.placa}): {tipo_original} → {viaje.tipo_trayecto}")
    
    print(f"\n✨ Proceso completado: {actualizados} viajes actualizados de {viajes.count()} totales\n")

if __name__ == '__main__':
    try:
        fix_viajes_tipo_trayecto()
        print("🎉 ¡Script ejecutado exitosamente!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
