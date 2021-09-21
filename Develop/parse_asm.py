import sys
from typing import List, Union, Callable


DumpFuncType = Callable[[bytes], None]

class Line(bytes):
    def dump(self, func: DumpFuncType):
        func(self)


class Function:
    # attribute: near or far
    def __init__(self, name: bytes, attribute: bytes, head: Line):
        self.name: bytes = name
        self.attribute: bytes = attribute
        self.head: Line = head
        self.tail: Line = b''
        self.units: List[Line] = []

    def dump(self, func: DumpFuncType):
        func(self.head)
        for unit in self.units:
            unit.dump(func)
        func(self.tail)


class Segment:
    def __init__(self, name: bytes, head: Line):
        self.name: bytes = name
        self.head: Line = head
        self.tail: Line = b''
        self.units: List[Union[Function, Line]] = []
    
    def dump(self, func: DumpFuncType):
        func(self.head)
        for unit in self.units:
            unit.dump(func)
        func(self.tail)

class File:
    def __init__(self):
        self.units: List[Union[Segment, Line]] = []

    def dump(self, func: DumpFuncType):
        for unit in self.units:
            unit.dump(func)


def parse(lines) -> File:
    file = File()
    current_segment = None
    current_function = None
    for line in lines:
        if line.find(b';') != -1:  # Found ';'
            dat = line[:line.find(b';')].split()
        else:
            dat = line.split()
        if True or line.strip():
            if len(dat) > 1:
                if dat[1] == b'segment':
                    print('SEG BEGIN', dat)
                    current_segment = Segment(name=dat[0], head=Line(line))
                elif dat[1] == b'ends':
                    print('SEG END', dat)
                    current_segment.tail = Line(line)
                    file.units.append(current_segment)
                    current_segment = None
                elif dat[1] == b'proc':
                    print('FUNC BEGIN', dat)
                    current_function = Function(name=dat[0], attribute=dat[1], head=Line(line))
                elif dat[1] == b'endp':
                    print('FUNC END', dat)
                    assert(current_segment)
                    current_function.tail = Line(line)
                    current_segment.units.append(current_function)
                    current_function = None
                else:
                    if current_function:
                        current_function.units.append(Line(line))
                    elif current_segment:
                        current_segment.units.append(Line(line))
                    else:
                        file.units.append(Line(line))
            else:
                if current_function:
                    current_function.units.append(Line(line))
                elif current_segment:
                    current_segment.units.append(Line(line))
                else:
                    file.units.append(Line(line))
    return file


def main(args: List[str]) -> int:
    with open('MTE.asm', 'rb') as f:
        file = parse(f.readlines())
    with open('MTEx.asm', 'wb+') as f:
        file.dump(func=f.write)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
