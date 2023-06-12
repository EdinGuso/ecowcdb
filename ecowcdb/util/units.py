# Standard Library Imports
from typing import List, Tuple

# Local Imports - ecowcdb libraries
from ecowcdb.options import DisplayUnit



def __unit_str(unit: DisplayUnit) -> str:
    match unit:
        case DisplayUnit.MicroSecond:
            return 'µs'
        case DisplayUnit.MilliSecond:
            return 'ms'
        case DisplayUnit.Second:
            return 's'
        case DisplayUnit.Minute:
            return 'min'
        case _:
            raise ValueError(f'Unhandled unit type: {unit}')

def __unit_factor(unit: DisplayUnit) -> int | float:
    match unit:
        case DisplayUnit.MicroSecond:
            return 10**6
        case DisplayUnit.MilliSecond:
            return 10**3
        case DisplayUnit.Second:
            return 1
        case DisplayUnit.Minute:
            return 1/60
        case _:
            raise ValueError(f'Unhandled unit type: {unit}')

def generate_header(delay_unit: DisplayUnit, runtime_unit: DisplayUnit) -> List[Tuple[str, str, str]]:
    
    return [('Edges Kept', f'Delay ({__unit_str(delay_unit)})', f'Elapsed Time ({__unit_str(runtime_unit)})')]

def convert_result_units(table: List[Tuple[List[Tuple[int, int]], float, float]], delay_unit: DisplayUnit, runtime_unit: DisplayUnit) -> List[Tuple[str, str, str]]:

    new_table = []

    for entry in table:
        
        new_table.append([entry[0].__str__(), (entry[1] * __unit_factor(delay_unit)).__str__(), (entry[2] * __unit_factor(runtime_unit)).__str__()])

    return new_table
