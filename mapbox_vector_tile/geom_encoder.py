
cmd_bits = 3

CMD_MOVE_TO = 1
CMD_LINE_TO = 2
CMD_SEG_END = 7
CMD_FAKE = 0


def omit_last(iterator):
    try:
        next_elmt = next(iterator)
        while True:
            elmt = next_elmt
            next_elmt = next(iterator)
            yield elmt
    except StopIteration:
        pass


class GeometryEncoder:
    """
    """
    def __init__(self, geometry, y_coord_down, extents, round_fn):
        self._geometry = geometry
        self._y_coord_down = y_coord_down
        self._extents = extents
        self._round = round_fn
        self._cmd_idx = -1
        self._geom_size = 0
        self.last_x, self.last_y = 0, 0

    def _encode_cmd_length(self, cmd, length):
        return (length << cmd_bits) | (cmd & ((1 << cmd_bits) - 1))

    def reserve_space_for_cmd(self):
        self._geometry.append(CMD_FAKE)
        self._cmd_idx = self._geom_size
        self._geom_size += 1

    def append_cmd(self, cmd, length):
        cmd_encoded = self._encode_cmd_length(cmd, length)
        self._geometry.append(cmd_encoded)
        self._geom_size += 1

    def set_back_cmd(self, cmd):
        length = (self._geom_size - self._cmd_idx) >> 1
        cmd_encoded = self._encode_cmd_length(cmd, length)
        self._geometry[self._cmd_idx] = cmd_encoded

    def append_coords(self, fx, fy, force=False):
        if isinstance(fx, float):
            x = int(self._round(fx))
        else:
            x = fx
        if isinstance(fy, float):
            y = int(self._round(fy))
        else:
            y = fy
        if not self._y_coord_down:
            y = self._extents - y

        dx = x - self.last_x
        dy = y - self.last_y
        if not force and dx == 0 and dy == 0:
            # print("...Aborted")
            return
        self._geometry.append((dx << 1) ^ (dx >> 31))
        self._geometry.append((dy << 1) ^ (dy >> 31))
        self.last_x = x
        self.last_y = y
        self._geom_size += 2

    def append_ring(self, arc):
        it = iter(arc.coords)
        x, y = next(it)
        self.append_cmd(CMD_MOVE_TO, 1)
        self.append_coords(x, y, True)
        self.reserve_space_for_cmd()
        for x, y in omit_last(it):
            self.append_coords(x, y)
        self.set_back_cmd(CMD_LINE_TO)
        self.append_cmd(CMD_SEG_END, 1)

    def append_arc(self, arc):
        it = iter(arc.coords)
        x, y = next(it)
        self.append_cmd(CMD_MOVE_TO, 1)
        self.append_coords(x, y, True)
        self.reserve_space_for_cmd()
        for x, y in it:
            self.append_coords(x, y)
        self.set_back_cmd(CMD_LINE_TO)

    def append_polygon(self, shape):
        self.append_ring(shape.exterior)
        for arc in shape.interiors:
            self.append_ring(arc)

    def encode_point(self, shape):
        self.append_cmd(CMD_MOVE_TO, 1)
        self.append_coords(shape.x, shape.y, True)

    def encode_points(self, shape):
        self.append_cmd(CMD_MOVE_TO, len(shape.geoms))
        # map ? apply ?
        for point in shape.geoms:
            self.append_coords(point.x, point.y, True)

    def encode_linestring(self, shape):
        self.append_arc(shape)

    def encode_linestrings(self, shape):
        for arc in shape.geoms:
            self.append_arc(arc)

    def encode_polygon(self, shape):
        self.append_polygon(shape)

    def encode_polygons(self, shape):
        for polygon in shape.geoms:
            self.append_polygon(polygon)
