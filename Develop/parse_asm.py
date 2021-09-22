import itertools
import sys
from typing import List, Union, Callable, Dict, Set, Optional


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
        self.tail: Line = Line(b'')
        self.units: List[Line] = []
        self.callees: Set[Function] = set()

    def __repr__(self) -> str:
        return f'<Function: {self.name}>'

    def dump(self, func: DumpFuncType):
        func(self.head)
        for unit in self.units:
            unit.dump(func)
        func(self.tail)


class Segment:
    def __init__(self, name: bytes, head: Line):
        self.name: bytes = name
        self.head: Line = head
        self.tail: Line = Line(b'')
        self.units: List[Union[Function, Line]] = []
        self.callees: Set[Function] = set()

    def __repr__(self) -> str:
        return f'<Segment: {self.name}>'

    def dump(self, func: DumpFuncType):
        func(self.head)
        for unit in self.units:
            unit.dump(func)
        func(self.tail)


class File:
    def __init__(self):
        self.units: List[Union[Segment, Line]] = []
        self.function_map: Dict[bytes, Function] = {}
        self.foreign_functions: Set[Function] = set()

    @property
    def segments(self):
        for unit in self.units:
            if isinstance(unit, Segment):
                yield unit

    def dump(self, func: DumpFuncType):
        for unit in self.units:
            unit.dump(func)

    def dump_lines(self) -> List[bytes]:
        result: List[bytes] = []
        self.dump(result.append)
        return result

    def get_or_insert_function(self, function_name: bytes) -> Function:
        if function_name not in self.function_map:
            foreign_function = Function(name=function_name, attribute=b'', head=Line(b''))
            self.foreign_functions.add(foreign_function)
            self.function_map[function_name] = foreign_function
        return self.function_map[function_name]


# call f   ->  [b'call', b'f']
# f a, b   ->  [b'f', b'a,' b'b']
# f a, b ; a -> [b'f', b'a,', b'b']
def get_line_seq(line: bytes) -> List[bytes]:
    if line.find(b';') != -1:  # Found ';'
        return line[:line.find(b';')].split()
    else:
        return line.split()


def parse(lines) -> File:
    file = File()
    current_segment = None
    current_function = None

    def append_line(line: bytes):
        if current_function:
            current_function.units.append(Line(line))
        elif current_segment:
            current_segment.units.append(Line(line))
        else:
            file.units.append(Line(line))

    for line in lines:
        dat = get_line_seq(line)
        if True or line.strip():
            if len(dat) > 1:
                if dat[1] == b'segment':
                    current_segment = Segment(name=dat[0], head=Line(line))
                elif dat[1] == b'ends':
                    current_segment.tail = Line(line)
                    file.units.append(current_segment)
                    current_segment = None
                elif dat[1] == b'proc':
                    current_function = Function(name=dat[0], attribute=dat[1], head=Line(line))
                    file.function_map[dat[0]] = current_function
                elif dat[1] == b'endp':
                    assert(current_segment)
                    current_function.tail = Line(line)
                    current_segment.units.append(current_function)
                    current_function = None
                else:
                    append_line(line)
            else:
                append_line(line)
    return file


def call_analysis(file: File):
    for file_unit in file.units:
        if isinstance(file_unit, Segment):
            for seg_unit in file_unit.units:
                if isinstance(seg_unit, Function):
                    for line in seg_unit.units:
                        dat = get_line_seq(line)
                        if dat:
                            if dat[0] == b'call':
                                callee_name = dat[-1]
                                seg_unit.callees.add(file.get_or_insert_function(callee_name))
                elif isinstance(seg_unit, Line):
                    dat = get_line_seq(seg_unit)
                    if dat:
                        if dat[0] == b'call':
                            callee_name = dat[-1]
                            file_unit.callees.add(file.get_or_insert_function(callee_name))


def unused_function_analysis(file: File, all_functions: Set[Function]) -> Set[Function]:
    current_all_functions = all_functions
    last_used_functions = set()
    while True:
        used_functions: Set[Function] = set()
        used_functions.add(file.function_map[b'_main'])
        for caller in itertools.chain(file.segments, current_all_functions):
            for callee in caller.callees:
                if callee is not caller:
                    used_functions.add(callee)
        if len(last_used_functions) == len(used_functions):
            break
        last_used_functions = used_functions
        current_all_functions = used_functions
    return all_functions - current_all_functions


def main(args: List[str]) -> int:
    with open('MTE.asm', 'rb') as f:
        data = f.readlines()
        file = parse(data)
        assert(data == file.dump_lines())
        data.clear()
    call_analysis(file)
    all_functions: Set[Function] = set(file.function_map.values())
    unused_functions = unused_function_analysis(file, all_functions)

    print(unused_functions)

    functions = {
        file.function_map[b'sub_10000'],
    }
    for caller in file.function_map.values():
        for callee in caller.callees:
            if callee in functions:
                print(caller)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
