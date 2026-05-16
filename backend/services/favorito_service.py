from repositories import favorito_repository

def agregar_favorito(usuario_id: int, producto_id: int):
    return favorito_repository.agregar_favorito(usuario_id, producto_id)

def obtener_favoritos(usuario_id: int):
    return favorito_repository.obtener_favoritos(usuario_id)

def eliminar_favorito(favorito_id: int, usuario_id: int):
    return favorito_repository.eliminar_favorito(favorito_id, usuario_id)
    
def toggle_favorito(usuario_id: int, producto_id: int):
    return favorito_repository.toggle_favorito(usuario_id, producto_id)
