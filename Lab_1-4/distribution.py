from scipy import stats as st
import math
import numpy as np

names = ["Normal distribution", "Cauchy distribution", "Laplace distribution", "Poisson distribution",
         "Uniform distribution"]


class Distribution:
    def __init__(self, name=None, size=0, repeat_num=1000):
        self.a = None
        self.b = None
        self.name = name
        self.size = size
        self.random_numbers = None
        self.density = None
        self.pdf = None
        self.cdf = None
        self.repeat_num = repeat_num
        self.x = None

    def __repr__(self):
        return f"{self.name}\nOn interval: [{self.a}, {self.b}]\nSize: {self.size}\nRandom numbers: " \
               f"{self.random_numbers}\nDensity: {self.density}\n\n"

    def set_distribution(self):
        if self.name == names[0]:
            self.random_numbers = st.norm.rvs(size=self.size)
            self.density = st.norm()
        elif self.name == names[1]:
            self.random_numbers = st.cauchy.rvs(size=self.size)
            self.density = st.cauchy()
        elif self.name == names[2]:
            self.random_numbers = st.laplace.rvs(size=self.size)
            self.density = st.laplace(scale=1 / math.sqrt(2), loc=0)
        elif self.name == names[3]:
            self.random_numbers = st.poisson.rvs(mu=10, size=self.size)
            self.density = st.poisson(10)  # mu = 10
        elif self.name == names[4]:
            a = -math.sqrt(3)
            step = 2 * math.sqrt(3)
            self.random_numbers = st.uniform.rvs(size=self.size, loc=a, scale=step)
            self.density = st.uniform(loc=a, scale=step)

    def set_x_pdf(self):
        if self.name == names[3]:
            self.x = np.arange(self.density.ppf(0.01), self.density.ppf(0.99))
            self.pdf = self.density.pmf(self.x)
        else:
            self.x = np.linspace(self.density.ppf(0.01), self.density.ppf(0.99), num=100)
            self.pdf = self.density.pdf(self.x)

    def set_x_cdf_pdf(self, param: str):
        self.x = np.linspace(self.a, self.b, self.repeat_num)
        if self.name == names[0]:
            self.pdf = st.norm.pdf(self.x)
            self.cdf = st.norm.cdf(self.x)
        elif self.name == names[1]:
            self.pdf = st.cauchy.pdf(self.x)
            self.cdf = st.cauchy.cdf(self.x)
        elif self.name == names[2]:
            self.pdf = st.laplace.pdf(self.x, loc=0, scale=1 / math.sqrt(2))
            self.cdf = st.laplace.cdf(self.x, loc=0, scale=1 / math.sqrt(2))
        elif self.name == names[3]:
            if param == 'kde':
                self.x = np.linspace(self.a, self.b, -self.a + self.b + 1)
            self.pdf = st.poisson(10).pmf(self.x)
            self.cdf = st.poisson(10).cdf(self.x)
        elif self.name == names[4]:
            a = -math.sqrt(3)
            step = 2 * math.sqrt(3)
            self.x = np.linspace(self.a, self.b, self.repeat_num)
            self.pdf = st.uniform.pdf(self.x, loc=a, scale=step)
            self.cdf = st.uniform.cdf(self.x, loc=a, scale=step)

    def set_a_b(self, a, b, a_poisson, b_poisson):
        if self.name == names[3]:
            self.a, self.b = a_poisson, b_poisson
        else:
            self.a, self.b = a, b
