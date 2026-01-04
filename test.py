"""Monte Carlo method for numerical integration"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi


def f(x):
    """Визначення функції та межі інтегрування: f(x) = x^2"""
    return x ** 2


a = 0  # Нижня межа
b = 2  # Верхня межа


def monte_carlo_integral(func, lower_bound, upper_bound, num_samples=100000):
    """Обчислює інтеграл методом Монте-Карло"""
    x_range = np.linspace(lower_bound, upper_bound, 1000)
    y_range = func(x_range)
    max_y = np.max(y_range)

    # Generating random points in the rectangle
    x_random = np.random.uniform(lower_bound, upper_bound, num_samples)
    y_random = np.random.uniform(0, max_y, num_samples)

    # Counting points under the curve
    points_under_curve = np.sum(y_random <= func(x_random))

    # Area of the rectangle
    rectangle_area = (upper_bound - lower_bound) * max_y

    # Area under the curve (integral)
    integral = (points_under_curve / num_samples) * rectangle_area

    return integral


# Counting integral by Monte Carlo method
n_samples = 100000
mc_result = monte_carlo_integral(f, a, b, n_samples)

# Checking through scipy.integrate.quad
quad_result, quad_error = spi.quad(f, a, b)

# Analytical calculation:
analytical_result = (b**3 - a**3) / 3

print("=" * 50)
print("ОБЧИСЛЕННЯ ІНТЕГРАЛА f(x) = x^2 від 0 до 2")
print("=" * 50)
print(f"\nМетод Монте-Карло (n={n_samples:,}): {mc_result:.6f}")
print(f"Метод quad (scipy):                    {quad_result:.6f} ± {quad_error:.2e}")
print(f"Аналітичний розрахунок:                 {analytical_result:.6f}")
print(f"\nПомилка методу Монте-Карло:            {abs(mc_result - analytical_result):.6f}")
print(f"Відносна помилка:                       {abs(mc_result - analytical_result) / analytical_result * 100:.4f}%")

x = np.linspace(-0.5, 2.5, 400)
y = f(x)

fig, ax = plt.subplots()

ax.plot(x, y, 'r', linewidth=2)

ix = np.linspace(a, b)
iy = f(ix)

# Added the area to the legend of the graph to make it more informative
ax.fill_between(ix, iy, color='gray', alpha=0.3, label=f'Area = {mc_result:.4f}')

ax.set_xlim([x[0], x[-1]])
ax.set_ylim([0, max(y) + 0.1])
ax.set_xlabel('x')
ax.set_ylabel('f(x)')

ax.axvline(x=a, color='gray', linestyle='--')
ax.axvline(x=b, color='gray', linestyle='--')
ax.set_title('Графік інтегрування f(x) = x^2 від ' + str(a) + ' до ' + str(b))
ax.legend(loc='center')
plt.grid()
plt.show()