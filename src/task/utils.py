from typing import Iterable, Callable, List, Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import timeit


class FunctionIterator:
    '''
    Iterates a value n in a range and return func(n)

    Input
    _____
        func: Callable
            function which call on each iteration
        min: int = 0
            minimum of values which iterator pass to func
        max: int = None
            maximum of values which iterator pass to func
            *this param cant be None. Default Nonevalue need for this exemple:
                FunctionIterator(func, 1, 10)
                iterate through all values n ​​from 1 to 10 and return results of func(n)
        step: int = 1
            step of iteration
            if step < 0:
                iterate through all values n from max to min and return result of func(n)
            else:
                iterate from min to max and return result of func(n)
    Return
    ______
        res: 
            1: cur: int
                current value in range on iteration
            2: func(self.cur): Any
                function from cur
        
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


class TimesOfExecutionIterator:
    '''
    Iterator which test times of execution of list or one func 
    
    Input
    _____
        funcs: List[Callable]|Callable
            list of tested functions
        test_data_iterator: Iterable
            Iterator for create test data
        unpack_test_data: bool = False
            if func depends from on many arguments set this param to True
        validators: List[Callable] = [lambda x: x, lambda x: x.tolist()]
            list of function which use before data from get_test_data pass to current func in funcs
        count_of_tests_on_one_data: int = 1
            counts of tests on one test data
    Return
    ______
        tuple:
            1: datasize: int
                datasize of test data which test_data_iterator return
            2... : *time: float
                time of execution of current function
                count of return time == count of input functions
    '''
    
    def __init__(self, funcs: Dict[str, Callable], test_data_iterator: Iterable, unpack_test_data: bool = False, validators: List[Callable] = [lambda x: x, lambda x: x.tolist()], count_of_execution_on_one_data: int = 1):
        self.funcs = funcs
        self.test_data_iterator = test_data_iterator
        self.unpack_test_data = unpack_test_data
        self.validators = validators
        self.count_of_execution_on_one_data = count_of_execution_on_one_data
    def __iter__(self):
        return self
    def __next__(self):
        test_data = next(self.test_data_iterator)
        if self.unpack_test_data:
            return tuple([test_data[0]]) + tuple(timeit.timeit(lambda: func(*data), number=self.count_of_execution_on_one_data) for func, data in zip(self.funcs.values(), (validator(test_data[1]) for validator in self.validators)))
        return tuple([test_data[0]]) + tuple(timeit.timeit(lambda: func(data), number=self.count_of_execution_on_one_data) for func, data in zip(self.funcs.values(), (validator(test_data[1]) for validator in self.validators)))


def get_times_of_execution_of_funcs(time_of_execution_iterator: Iterable):
    '''
    Input
    _____
        time_of_execution_iterator: Iterable
    Return
    ______
        data: np.recarray, 2d(count_of_tests, count_of_tested_funcs + 1)
            1: datasize: np.int32
                datasize of test
            2...: *time of func execution: np.float64
                count of times == count of funcs
                
    '''
    return np.fromiter(time_of_execution_iterator, dtype=np.dtype([('datasize', np.int32), *[(name, np.float64) for name in time_of_execution_iterator.funcs.keys()]])).view(np.recarray)

def build_graph_of_times_of_execution_of_funcs(title: str, show: bool = True, save: bool = True, tested_param: str = 'x', data: np.recarray = None, count_of_execution_on_one_data: int = None, more_data: List[str]|Tuple[str]|str = None):
    '''
    Input
    _____
        title: str
            title of graph
        show: bool = True
            Is show graph
        save: bool = True
            Is save graph
        tested_param: str = 'x'
            first line of x axis
        data: np.recarray, 2d(count_of_tests, count_of_tested_funcs + 1)
            1: datasize: np.int32
                datasize of test
            2...: *time of func execution: np.float64
                count of times == count of funcs
        count_of_execution_on_one_data: int = 1
            positive int
        more_data: List[str]|str
            more param 
    Return
    ______
        fig: matplotlib.figure

        ax: matplotlib.axes.Axes
            graph of times of execution of funcs
                
    '''
    fig, ax = plt.subplots()
    for name in data.dtype.names[1:]:
        ax.plot(data.datasize, getattr(data, name), label=name)
    ax.set_title(title)
    ax.set_xlabel(tested_param + '\n\n' + (('\n'.join(more_data) + '\n') if type(more_data) in [list, tuple] else (more_data + '\n') if more_data else '') + f'Количество итераций на одних данных: {count_of_execution_on_one_data}' if not count_of_execution_on_one_data is None else '')
    ax.set_ylabel('Время (с)')
    ax.grid()
    ax.legend()
    if show:
        fig.show()
    if save:
        fig.savefig(path_to_graphes + ('/' if path_to_graphes[-1] != '/' else '') + title, bbox_inches='tight', dpi=500)
    return fig, ax