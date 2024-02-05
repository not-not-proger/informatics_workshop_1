from typing import Iterable, Callable, List, Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import timeit


class BaseIterator:
    '''
    Input
    _____
        func: Callable
            function which call on each iteration
        min: int = 0
            minimum of values which iterator pass to func
        max: int = None
            maximum of values which iterator pass to func
            *this param cant be None. Default Nonevalue need for this exemple:
                BaseIterator(func, 1, 10)
                iterate through all values n ​​from 1 to 10 and return results of func(n)
        step: int = 1
            step of iteration
            if step < 0:
                iterate through all values n from max to min and return result of func(n)
            else:
                iterate from min to max and return result of func(n)
    Return
        cur: int
            current value on iteration
        func(self.cur): Any
            function of current cur
    ______
        
    '''
    
    def __init__(self, func, min = 0, max = None , step = 1):
        assert step != 0
        if max is None:
            assert min != 0
            max = min
            min = 0
        assert min <= max
        self.func = func
        self.min = min
        self.max = max
        self.step = step
        self.cur = min if step >= 0 else max
    def __iter__(self):
        return self
    def __next__(self):
        if self.min <= self.cur <= self.max:
            res = (self.cur, self.func(self.cur))
            self.cur += self.step
            return res
        raise StopIteration


class DataSetIterator:
    '''
    Iterator for create dataset
    
    Input
    _____
        funcs: List[Callable]|Callable
            list of tested functions
        testDataIterator: Iterable
            Iterator for create test data
        count_of_tests_on_one_data: int = 1
            counts of tests on one test data
    Return
    ______
        datasize: int
            datasize of test data which testDataIterator return
        *time: float
            time of execution of current function
            count of return time == count of input functions
    '''
    
    def __init__(self, funcs: List[Callable]|Callable, testDataIterator: Iterable, unpack_test_data: bool = False, validators: List[Callable] = [lambda x: x, lambda x: x.tolist()], count_of_tests_on_one_data: int = 1):
        if not type(funcs) is tuple and not type(funcs) is list:
            funcs = [funcs]
        self.funcs = funcs
        self.testDataIterator = testDataIterator
        self.unpack_test_data = unpack_test_data
        self.validators = validators
        self.count_of_executions_on_one_data = count_of_tests_on_one_data
    def __iter__(self):
        return self
    def __next__(self):
        testData = next(self.testDataIterator)
        if self.unpack_test_data:
            return tuple([testData[0]]) + tuple(timeit.timeit(lambda: func(*data), number=self.count_of_executions_on_one_data) for func, data in zip(self.funcs, (validator(testData[1]) for validator in self.validators)))
        return tuple([testData[0]]) + tuple(timeit.timeit(lambda: func(data), number=self.count_of_executions_on_one_data) for func, data in zip(self.funcs, (validator(testData[1]) for validator in self.validators)))


def get_times_of_executions_of_funcs(funcs: List[Callable], get_test_data: Callable = lambda x: x, unpack_test_data: bool = False, validators: List[Callable] = [lambda x: x, lambda x: x.tolist()], min: int = 0, max: int = None, step: int = 1, count_of_executions_on_one_data: int = 1):
    '''
    Input
    _____
        funcs: Dict[str, Callable]
            Dict of functions
            ____
            key:
                name of function
            value:
                callable object
        get_test_data: Callable = lambda x: x
            function depending on one parameter which return test data
        min: 
    
    '''
    assert not min is None
    return np.fromiter(DataSetIterator(funcs, BaseIterator(get_test_data, min=min, max=max, step=step), unpack_test_data, validators, count_of_executions_on_one_data), dtype=np.dtype([('datasize', np.int32), *[(chr(label + 97), np.float64) for label in range(len(funcs))]])).view(np.recarray)

def build_graph_of_times_of_executions_of_funcs(title: str, show: bool = True, save: bool = True, funcs: Dict[str, Callable] = None, get_test_data: Callable = lambda x: x, unpack_test_data: bool = False, validators: List[Callable] = [lambda x: x, lambda x: x.tolist()], type_of_tested_data: str = 'x', min: int = 0, max: int = None, step: int = 1, count_of_executions_on_one_data: int = 1, more_data: List[str]|Tuple[str]|str = None):
    '''
    '''
    assert not funcs is None
    data = get_times_of_executions_of_funcs(tuple(funcs.values()), get_test_data, unpack_test_data, validators, min, max, step, count_of_executions_on_one_data)
    fig, ax = plt.subplots()
    for name, label in zip(funcs.keys(), np.arange(len(funcs))):
        ax.plot(data.datasize, getattr(data, chr(label + 97)), label=name)
    ax.set_title(title)
    ax.set_xlabel(type_of_tested_data + '\n\n' + (('\n'.join(more_data) + '\n') if type(more_data) in [list, tuple] else (more_data + '\n') if more_data else '') + f'Количество итераций на одних данных: {count_of_executions_on_one_data}')
    ax.set_ylabel('Время (с)')
    ax.grid()
    ax.legend()
    if show:
        fig.show()
    if save:
        fig.savefig(title, bbox_inches='tight', dpi=500)
    