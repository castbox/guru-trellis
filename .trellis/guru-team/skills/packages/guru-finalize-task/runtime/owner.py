"""Mechanical loader for the package-local owner implementation."""

from pathlib import Path as _Path

_OWNER_PARTS = [
    '_owner_part_01.py',
    '_owner_part_02.py',
    '_owner_part_03.py',
    '_owner_part_04.py',
    '_owner_part_05.py',
    '_owner_part_06.py'
]

for _part_name in _OWNER_PARTS:
    _part_path = _Path(__file__).with_name(_part_name)
    exec(compile(_part_path.read_bytes(), str(_part_path), "exec"), globals(), globals())

del _Path, _OWNER_PARTS, _part_name, _part_path
