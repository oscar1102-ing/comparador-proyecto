from repositories import historial_repository

def guardar_busqueda(usuario_id: int, busqueda: str):
    if not busqueda.strip():
        return
    historial_repository.guardar_busqueda(usuario_id, busqueda.strip())

def obtener_historial(usuario_id: int):
    return historial_repository.obtener_historial(usuario_id)

def eliminar_historial(usuario_id: int):
    return historial_repository.eliminar_historial(usuario_id)
