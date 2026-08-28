"""Clear the executable-stack flag on ELF shared objects.

PyTorch 1.10's prebuilt libraries carry a PT_GNU_STACK segment marked
executable. Linux 6.x and later refuse to load those, so `import torch` dies
with

    ImportError: libtorch_cpu.so: cannot enable executable stack as shared
    object requires: Invalid argument

The fix is a one-bit edit: clear PF_X in the PT_GNU_STACK program header. This
is what `execstack -c` does, without needing the prelink package installed.
Only the flag changes; no code is touched.
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

PT_GNU_STACK = 0x6474E551
PF_X = 0x1


def clear(path: Path) -> bool:
    data = bytearray(path.read_bytes())
    if data[:4] != b"\x7fELF":
        return False
    if data[4] != 2:  # 64-bit only; nothing here ships 32-bit
        return False
    little = data[5] == 1
    end = "<" if little else ">"

    e_phoff = struct.unpack_from(end + "Q", data, 0x20)[0]
    e_phentsize = struct.unpack_from(end + "H", data, 0x36)[0]
    e_phnum = struct.unpack_from(end + "H", data, 0x38)[0]

    changed = False
    for i in range(e_phnum):
        off = e_phoff + i * e_phentsize
        p_type = struct.unpack_from(end + "I", data, off)[0]
        if p_type != PT_GNU_STACK:
            continue
        flags_off = off + 4
        p_flags = struct.unpack_from(end + "I", data, flags_off)[0]
        if p_flags & PF_X:
            struct.pack_into(end + "I", data, flags_off, p_flags & ~PF_X)
            changed = True
    if changed:
        path.write_bytes(bytes(data))
    return changed


def main(roots: list[str]) -> None:
    n = 0
    for root in roots:
        for p in Path(root).rglob("*.so*"):
            if p.is_symlink() or not p.is_file():
                continue
            try:
                if clear(p):
                    print(f"cleared execstack: {p}")
                    n += 1
            except (OSError, struct.error) as e:
                print(f"skipped {p}: {e}", file=sys.stderr)
    print(f"{n} file(s) patched")


if __name__ == "__main__":
    main(sys.argv[1:] or ["."])
