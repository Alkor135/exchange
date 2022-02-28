class Goom(object):
    items = []  # Список экземпляров класса

    def __init__(self, name, seats, jump):
        """Инициализация"""
        self.name = name
        self.seats = seats
        self.jump = jump
        Goom.items.append(self)  # Добавление в список экземпляров класса

    def __str__(self):
        return "{} {} {}".format(self.name, self.seats, self.jump)


my_goom1 = Goom("Лил", "1", "Нет")
my_goom2 = Goom("Мак", "1", "Есть")
my_goom3 = Goom("Ной", "1", "Есть")

print(Goom.items)
print(Goom.items[0])
print(*[f'{x},' for x in Goom.items])
print(*Goom.items, sep=', ')

# Удаление экземпляров класса с именем Мак
Goom.items = [x for x in Goom.items if x.name != 'Мак']  # List comprehensions

print(*[(f'{x},' if Goom.items.index(x) != len(Goom.items)-1 else x) for x in Goom.items])    # List comprehensions
print(*Goom.items, sep=', ')
