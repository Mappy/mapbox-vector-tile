from .Mapbox import vector_tile_p3_pb2
vector_tile = vector_tile_p3_pb2


def apply_map(fn, x):
    return list(map(fn, x))
