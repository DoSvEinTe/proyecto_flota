"""
Script para corregir las relaciones de viajes de ida y vuelta.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_flota.settings')
django.setup()

from viajes.models import Viaje

def fix_viajes_relaciones():
    """Corrige las relaciones de viajes de ida y vuelta."""
    
    print("\n🔍 Analizando viajes de ida y vuelta...\n")
    
    # Obtener todos los viajes marcados como ida_vuelta
    viajes_ida_vuelta = Viaje.objects.filter(es_ida_vuelta=True).order_by('id')
    
    procesados = set()
    
    for viaje in viajes_ida_vuelta:
        if viaje.id in procesados:
            continue
            
        # Si tiene viaje relacionado
        if viaje.viaje_relacionado:
            relacionado = viaje.viaje_relacionado
            
            # Verificar si la relación es bidireccional (incorrecta)
            if relacionado.viaje_relacionado and relacionado.viaje_relacionado.id == viaje.id:
                print(f"⚠️  Relación bidireccional detectada:")
                print(f"   Viaje #{viaje.id} (Bus: {viaje.bus.placa}) ↔️ Viaje #{relacionado.id}")
                print(f"   Viaje #{viaje.id}: {viaje.origen_ciudad} → {viaje.destino_ciudad} @ {viaje.fecha_salida}")
                print(f"   Viaje #{relacionado.id}: {relacionado.origen_ciudad} → {relacionado.destino_ciudad} @ {relacionado.fecha_salida}")
                
                # Determinar cuál es IDA y cuál es VUELTA por fecha
                if viaje.fecha_salida <= relacionado.fecha_salida:
                    # viaje es IDA, relacionado es VUELTA
                    viaje.tipo_trayecto = 'ida'
                    relacionado.tipo_trayecto = 'vuelta'
                    relacionado.viaje_relacionado = None  # La vuelta no apunta de regreso
                    print(f"   ✅ Corregido: #{viaje.id} = IDA, #{relacionado.id} = VUELTA")
                else:
                    # relacionado es IDA, viaje es VUELTA
                    relacionado.tipo_trayecto = 'ida'
                    viaje.tipo_trayecto = 'vuelta'
                    viaje.viaje_relacionado = None
                    relacionado.viaje_relacionado = viaje
                    print(f"   ✅ Corregido: #{relacionado.id} = IDA, #{viaje.id} = VUELTA")
                
                viaje.save()
                relacionado.save()
                procesados.add(viaje.id)
                procesados.add(relacionado.id)
                print()
            else:
                # Relación unidireccional normal
                viaje.tipo_trayecto = 'ida'
                relacionado.tipo_trayecto = 'vuelta'
                viaje.save()
                relacionado.save()
                procesados.add(viaje.id)
                procesados.add(relacionado.id)
                print(f"✅ Relación normal: #{viaje.id} (IDA) → #{relacionado.id} (VUELTA)")
        else:
            # Viaje de ida sin vuelta asignada todavía
            viaje.tipo_trayecto = 'ida'
            viaje.save()
            print(f"⚠️  Viaje #{viaje.id} marcado como IDA sin vuelta relacionada")
    
    print("\n✨ Proceso completado!\n")

if __name__ == '__main__':
    try:
        fix_viajes_relaciones()
        print("🎉 ¡Script ejecutado exitosamente!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
