import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi


def f(x):
    """
    Function to integrate: f(x) = x^2

    Parameters:
        x(float or array): Input value(s)

    Returns:
        float or array: Result of x squared.
    """
    return x ** 2


def monte_carlo_integration(func, a, b, num_points=100000):
    """
    Calculates definite integral using Monte Carlo method

    Parameters:
        func(function): Function to integrate
        a(float): Lower bound of integration
        b(float): Upper bound of integration
        num_points(int): Number of random points (default 100000)

    Returns:
        dict: Dictionary with integration results or empty dict if failed.
    """
    # validation of input data
    if (a < b and num_points > 0):
        # find maximum value of function in interval for bounding box
        x_test = np.linspace(a, b, 1000)
        y_max = max(func(x_test))
        
        # generate random points
        x_random = np.random.uniform(a, b, num_points)
        y_random = np.random.uniform(0, y_max, num_points)
        
        # count points under the curve
        points_under_curve = np.sum(y_random <= func(x_random))
        
        # calculate area of bounding rectangle
        rectangle_area = (b - a) * y_max
        
        # calculate integral (proportion of points * rectangle area)
        integral_value = (points_under_curve / num_points) * rectangle_area
        
        # prepare results
        results = {
            "integral": integral_value,
            "points_total": num_points,
            "points_under_curve": points_under_curve,
            "rectangle_area": rectangle_area,
            "x_random": x_random,
            "y_random": y_random,
            "y_max": y_max
        }
        # return data
        return results
    else:
        # if input data aren't correct, returns empty dict
        return {}


def analytical_integration(a, b):
    """
    Calculates analytical value of integral for f(x) = x^2

    Parameters:
        a(float): Lower bound of integration
        b(float): Upper bound of integration

    Returns:
        float: Analytical value of integral (x^3/3).
    """
    # integral of x^2 is x^3/3
    return (b ** 3 / 3) - (a ** 3 / 3)


def quad_integration(func, a, b):
    """
    Calculates integral using scipy.integrate.quad

    Parameters:
        func(function): Function to integrate
        a(float): Lower bound of integration
        b(float): Upper bound of integration

    Returns:
        tuple: (integral value, error estimate).
    """
    result, error = spi.quad(func, a, b)
    return result, error


def plot_monte_carlo(func, a, b, mc_results):
    """
    Creates visualization of Monte Carlo integration

    Parameters:
        func(function): Function to integrate
        a(float): Lower bound of integration
        b(float): Upper bound of integration
        mc_results(dict): Results from Monte Carlo integration
    """
    # create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # create x values for function plot
    x = np.linspace(-0.5, 2.5, 400)
    y = func(x)
    
    # plot function
    ax.plot(x, y, 'r', linewidth=2, label='f(x) = x²')
    
    # fill area under curve
    ix = np.linspace(a, b, 100)
    iy = func(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3, label='Область інтегрування')
    
    # plot sample of random points (not all to avoid clutter)
    sample_size = min(1000, mc_results["points_total"])
    indices = np.random.choice(mc_results["points_total"], sample_size, replace=False)
    
    x_sample = mc_results["x_random"][indices]
    y_sample = mc_results["y_random"][indices]
    
    # separate points under and above curve
    under_curve = y_sample <= func(x_sample)
    
    ax.scatter(x_sample[under_curve], y_sample[under_curve], 
               c='green', s=1, alpha=0.5, label='Точки під кривою')
    ax.scatter(x_sample[~under_curve], y_sample[~under_curve], 
               c='blue', s=1, alpha=0.5, label='Точки над кривою')
    
    # configure plot
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    
    # add integration bounds
    ax.axvline(x=a, color='gray', linestyle='--')
    ax.axvline(x=b, color='gray', linestyle='--')
    ax.set_title(f'Метод Монте-Карло: інтегрування f(x) = x² від {a} до {b}')
    ax.legend()
    plt.grid()
    plt.show()
    
    # save figure
    # plt.savefig('monte_carlo.png', dpi=150, bbox_inches='tight')
    # print("\n✅ Графік збережено: monte_carlo.png")
    # plt.close()


def print_comparison(mc_result, analytical_result, quad_result, quad_error):
    """
    Prints comparison of all integration methods

    Parameters:
        mc_result(float): Monte Carlo integration result
        analytical_result(float): Analytical integration result
        quad_result(float): Scipy quad integration result
        quad_error(float): Scipy quad error estimate
    """
    print("=" * 50)
    print("ПОРІВНЯННЯ МЕТОДІВ ОБЧИСЛЕННЯ ІНТЕГРАЛА")
    print("=" * 50)
    print(f"\nФункція: f(x) = x²")
    print(f"Межі інтегрування: [0, 2]")
    
    print("\n" + "-" * 50)
    print("РЕЗУЛЬТАТИ:")
    print("-" * 50)
    print(f"  Метод Монте-Карло:    {mc_result:.6f}")
    print(f"  Аналітичний метод:    {analytical_result:.6f}")
    print(f"  Функція quad (SciPy): {quad_result:.6f} (±{quad_error:.2e})")
    
    print("\n" + "-" * 50)
    print("ПОХИБКИ:")
    print("-" * 50)
    mc_error_abs = abs(mc_result - analytical_result)
    mc_error_rel = (mc_error_abs / analytical_result) * 100
    print(f"  Абсолютна похибка Монте-Карло: {mc_error_abs:.6f}")
    print(f"  Відносна похибка Монте-Карло:  {mc_error_rel:.4f}%")


if __name__ == "__main__":
    # define integration bounds
    A = 0  # lower bound
    B = 2  # upper bound
    NUM_POINTS = 100000  # number of random points
    
    # run Monte Carlo integration
    mc_results = monte_carlo_integration(f, A, B, NUM_POINTS)
    
    # check if results obtained
    if mc_results:
        # calculate analytical result
        analytical_result = analytical_integration(A, B)
        
        # calculate quad result
        quad_result, quad_error = quad_integration(f, A, B)
        
        # print comparison
        print_comparison(
            mc_results["integral"],
            analytical_result,
            quad_result,
            quad_error
        )
        
        # create visualization
        plot_monte_carlo(f, A, B, mc_results)
    else:
        print("Помилка: не вдалося обчислити інтеграл")