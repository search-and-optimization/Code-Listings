__all__ = ['simulated_annealing']

import math
import random
COOLING_SCHEDULES = ['linear', 'geometric', 'logarithmic', 'exponential', 'linear_inverse']


class simulated_annealing:

    def __init__(self, problem_obj, max_iter=1000, max_iter_per_temp=10,
                 initial_temp=5230.0, final_temp=0.1,
                 cooling_schedule='linear_inverse', cooling_alpha=0.9) -> None:
        self.problem_obj = problem_obj
        self.max_iter = max_iter if max_iter > 0 else 1000
        self.max_iter_per_temp = max_iter_per_temp if max_iter_per_temp > 0 else 10
        self.initial_temp = initial_temp if initial_temp >= 10 else 1000
        self.final_temp = final_temp if 1 >= final_temp > 0 else 0.1
        
        if cooling_schedule not in COOLING_SCHEDULES:
            raise ValueError("Undefined cooling function " + cooling_schedule + ", it must be one of ",
                             str(COOLING_SCHEDULES))
        self.__cooling_schedule = cooling_schedule

        self.__cooling_alpha = cooling_alpha    

        if self.__cooling_schedule == 'linear_inverse' and self.__cooling_alpha <= 0:
            raise ValueError("For cooling function " + self.__cooling_schedule +
                             ", cooling alpha must be greater than 0")
        elif self.__cooling_schedule == 'geometric' and 0.8 > self.__cooling_alpha or self.__cooling_alpha > 0.9:
            raise ValueError("For cooling function " + self.__cooling_schedule +
                             ", cooling alpha must be in range [0.8, 0.9]")

    def init_annealing(self):
        self.t = self.initial_temp
        self.iter = 1
        self.s_best = self.problem_obj.get_init_solution()
        self.val_best = self.problem_obj.eval_solution(self.s_best)
        self.s_cur = self.s_best
        self.val_cur = self.val_best

    def annealing_step(self):
        s_cand = self.problem_obj.get_neighbour_solution(self.s_cur)
        val_cand = self.problem_obj.eval_solution(s_cand)
        val_diff = val_cand - self.val_cur
        if val_diff < 0 or random.random() < math.exp(-1*val_diff/self.t):
            self.s_cur = s_cand
            self.val_cur = val_cand
            if val_cand < self.val_best:
                self.s_best = s_cand
                self.val_best = val_cand

    def update_temperature(self):
        if self.__cooling_schedule == 'linear':
            self.t = self.initial_temp - (self.initial_temp - self.final_temp) * self.iter / self.max_iter
        elif self.__cooling_schedule == 'geometric':
            self.t = self.initial_temp * self.__cooling_alpha ** self.iter
        elif self.__cooling_schedule == 'logarithmic':
            self.t = self.initial_temp / math.log( 1 + self.iter)
        elif self.__cooling_schedule == 'exponential':
            self.t = self.initial_temp * math.exp( -1 * self.__cooling_alpha * self.iter ** (1 / self.max_iter))
        elif self.__cooling_schedule == 'linear_inverse':
            self.t = self.initial_temp / (1 + self.__cooling_alpha * self.iter)
        else:
            raise ValueError("Undefined cooling function " + self.__cooling_schedule)

    def run(self):
        self.init_annealing()
        while self.t > self.final_temp and self.iter <= self.max_iter:
            for _ in range(self.max_iter_per_temp):
                self.annealing_step()
            self.update_temperature()
            self.iter += 1