from pulp import LpMaximize, LpProblem, LpVariable, PULP_CBC_CMD, value

def optimize_production(water, sugar, lemon_juice, fruit_puree):
    """
    Optimizes production of beverages to maximize total output

    Parameters:
        water(int): Available water units (max 100)
        sugar(int): Available sugar units (max 50)
        lemon_juice(int): Available lemon juice units (max 30)
        fruit_puree(int): Available fruit puree units (max 40)

    Returns:
        dict: Dictionary with optimization results or empty dict if failed.
    """
    # validation of input data
    if (water > 0 and sugar > 0 and lemon_juice > 0 and fruit_puree > 0):
        # create optimization problem
        problem = LpProblem("Maximize_Production", LpMaximize)
        
        # define variables (how many products to produce)
        lemonade = LpVariable("Lemonade", lowBound=0, cat="Integer")
        fruit_juice = LpVariable("Fruit_Juice", lowBound=0, cat="Integer")
        
        # objective function: maximize total products
        problem += lemonade + fruit_juice, "Total_Products"
        
        # constraints based on resources
        problem += 2 * lemonade + fruit_juice <= water, "Water_Constraint"
        problem += lemonade <= sugar, "Sugar_Constraint"
        problem += lemonade <= lemon_juice, "Lemon_Juice_Constraint"
        problem += 2 * fruit_juice <= fruit_puree, "Fruit_Puree_Constraint"
        
        # solve the problem
        problem.solve(PULP_CBC_CMD(msg=0))
        
        # check if solution found
        if problem.status == 1:
            # prepare results
            results = {
                "status": "Рішення знайдено",
                "total_products": int(value(problem.objective)),
                "lemonade": int(value(lemonade)),
                "fruit_juice": int(value(fruit_juice)),
                "water_used": 2 * int(value(lemonade)) + int(value(fruit_juice)),
                "sugar_used": int(value(lemonade)),
                "lemon_juice_used": int(value(lemonade)),
                "fruit_puree_used": 2 * int(value(fruit_juice))
            }
            # return data
            return results
        else:
            # if solution not found, returns empty dict
            return {}
    else:
        # if input data aren't correct, returns an empty dict
        return {}


def print_results(results, water, sugar, lemon_juice, fruit_puree):
    """
    Prints optimization results in formatted way

    Parameters:
        results(dict): Dictionary with optimization results
        water(int): Total available water
        sugar(int): Total available sugar
        lemon_juice(int): Total available lemon juice
        fruit_puree(int): Total available fruit puree
    """
    if results:
        print("=" * 40)
        print("ОПТИМІЗАЦІЯ ВИРОБНИЦТВА")
        print("=" * 40)
        print(f"\nСтатус: {results['status']}")
        print(f"Максимальна кількість напоїв: {results['total_products']}")
        print("\nОптимальний план виробництва напоїв:")
        print(f"  Лимонад: {results['lemonade']} од.")
        print(f"  Фруктовий сік: {results['fruit_juice']} од.")
        print("\nВикористання ресурсів:")
        print(f"  Вода: {results['water_used']} од. (з {water})")
        print(f"  Цукор: {results['sugar_used']} од. (з {sugar})")
        print(f"  Лимонний сік: {results['lemon_juice_used']} од. (з {lemon_juice})")
        print(f"  Фруктове пюре: {results['fruit_puree_used']} од. (з {fruit_puree})")
    else:
        print("Помилка: не вдалося знайти рішення або некоректні вхідні дані")


if __name__ == "__main__":
    # define available resources
    WATER = 100
    SUGAR = 50
    LEMON_JUICE = 30
    FRUIT_PUREE = 40
    
    # run optimization
    results = optimize_production(WATER, SUGAR, LEMON_JUICE, FRUIT_PUREE)
    
    # print results
    print_results(results, WATER, SUGAR, LEMON_JUICE, FRUIT_PUREE)