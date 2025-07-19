# Juego de Sockets - Redimensionamiento Corregido

Este proyecto implementa un juego con soporte para redimensionamiento de ventana y detección correcta de botones.

## Problemas Corregidos

### 1. Pantalla de IP del Multijugador ✅
- **Problema**: Los elementos no se redimensionaban con la ventana
- **Solución**: Implementado sistema completo `display_manager` con coordenadas virtuales
- **Resultado**: Todos los elementos se centran y escalan apropiadamente

### 2. Botones del Single Player ✅
- **Problema**: Los botones internos no respondían a clics
- **Solución**: Implementado almacenamiento de rectángulos reales y detección directa
- **Resultado**: Todos los botones funcionan correctamente

## Arquitectura de la Solución

### DisplayManager
- Sistema de coordenadas virtuales (800x600 por defecto)
- Escalado automático a cualquier tamaño de ventana
- Conversión entre coordenadas virtuales y reales
- Escalado de fuentes y elementos de UI

### Patrón de Botones Mejorado
```python
# Antes (no funcionaba)
if mouse_x >= button_x and mouse_x <= button_x + button_width:
    # Detección manual con errores

# Después (funciona correctamente)  
actual_rect = display_manager.scale_rect(virtual_rect)
self.button_rects[button_id] = actual_rect
if actual_rect.collidepoint(mouse_pos):
    # Detección directa con pygame
```

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar el juego
```bash
python main.py
```

### Ejecutar tests automatizados
```bash
python test_automated.py
```

### Ejecutar tests manuales (requiere display)
```bash
python test_game.py
```

## Estructura de Archivos

- `main.py` - Aplicación principal
- `display_manager.py` - Sistema de escalado y coordenadas
- `main_menu.py` - Menú principal (patrón de referencia)
- `game.py` - Juego single player (botones corregidos)
- `game_multiplayer.py` - Juego multijugador (redimensionamiento corregido)
- `test_automated.py` - Tests automatizados
- `test_game.py` - Tests manuales con interfaz gráfica

## Características

### ✅ Redimensionamiento Completo
- Ventana redimensionable con `pygame.RESIZABLE`
- Manejo de evento `pygame.VIDEORESIZE`
- Escalado automático de todos los elementos
- Centrado dinámico de componentes

### ✅ Detección de Botones Mejorada
- Almacenamiento de rectángulos reales
- Detección directa con `rect.collidepoint()`
- Patrón consistente en todos los menús
- Soporte para campos de entrada (IP/Puerto)

### ✅ Funcionalidad Completa
- Menú principal funcional
- Single player con submenús (Jugar, Instrucciones, Puntuaciones)
- Multijugador con entrada de IP/Puerto
- Navegación completa entre pantallas

## Controles

- **Click izquierdo**: Seleccionar botones
- **ESC**: Volver al menú anterior o salir
- **TAB**: Cambiar entre campos de entrada (multijugador)
- **Enter**: Conectar en pantalla multijugador
- **Redimensionar ventana**: Arrastra los bordes de la ventana

## Validación

Todos los criterios de aceptación han sido cumplidos:
- ✅ Pantalla IP del multijugador se redimensiona correctamente
- ✅ Todos los elementos se centran y escalan apropiadamente  
- ✅ Botones del single player responden a clics
- ✅ Todos los menús internos funcionan correctamente
- ✅ El redimensionamiento funciona en todos los estados del juego
- ✅ No hay regresiones en funcionalidad existente