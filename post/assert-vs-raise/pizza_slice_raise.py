def calculate_pizza_area(pizza_radius, people_eating=1):
    '''
    Calculates the area of the pizza that each person will receive, assuming
    the pizza is split equally among all people.
    '''
    if people_eating==0:
        raise ZeroDivisionError
    return (3.1415*(pizza_radius**2))/people_eating


print(calculate_pizza_area(3))
print(calculate_pizza_area(3, people_eating=0))
