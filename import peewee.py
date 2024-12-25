import peewee
import random

# Подключение к базе данных SQLite
db = peewee.SqliteDatabase('warriors.db')

class Warrior(peewee.Model):
    """Модель бойца."""
    name = peewee.CharField(unique=True)
    health = peewee.IntegerField(default=100)
    armor = peewee.IntegerField(default=50)
    endurance = peewee.IntegerField(default=50)

    class Meta:
        database = db

    def attack(self, opponent):
        """Метод атаки: атакующий теряет 10 очков выносливости, противник теряет здоровье и броню."""
        if self.endurance > 0:
            damage = random.randint(10, 30)
            opponent.health -= damage
            self.endurance -= 10
            print(f"{self.name} атакует! У {opponent.name} теряет {damage} здоровья. {self.name} теряет 10 выносливости.")
        else:
            print(f"{self.name} атакует с ослаблением из-за низкой выносливости!")
            damage = random.randint(0, 10)
            opponent.health -= damage
            print(f"{self.name} наносит ослабленный урон! У {opponent.name} теряет {damage} здоровья.")

    def defend(self, opponent):
        """Метод защиты: защитник теряет здоровье и броню в зависимости от атаки."""
        if self.armor > 0:
            damage_health = random.randint(0, 20)
            damage_armor = random.randint(0, 10)
            self.health -= damage_health
            self.armor -= damage_armor
            print(f"{self.name} защищается! Теряет {damage_health} здоровья и {damage_armor} брони.")
        else:
            damage_health = random.randint(10, 30)
            self.health -= damage_health
            print(f"{self.name} защищается! Броня закончилась, теряет {damage_health} здоровья.")

    def is_alive(self):
        """Проверка, жив ли боец (здоровье больше 10)."""
        return self.health > 10

    @classmethod
    def create_warrior(cls, name):
        """Создание бойца и сохранение в базе данных."""
        warrior = cls.create(name=name)
        return warrior

    @classmethod
    def get_warrior_by_name(cls, name):
        """Получение бойца по имени."""
        return cls.get(cls.name == name)

    def execute_query(self, query):
        """Функция для выполнения произвольных запросов без дублирования кода SQL."""
        return db.execute_sql(query)


def initialize_database():
    """Функция для инициализации базы данных и создания таблиц."""
    if not Warrior.table_exists():
        db.connect()
        db.create_tables([Warrior])
        print("База данных и таблицы созданы.")
    else:
        print("База данных уже существует.")


def battle(warrior1, warrior2):
    """Функция для боя двух бойцов."""
    while warrior1.is_alive() and warrior2.is_alive():
        action1 = random.choice(["attack", "defend"])
        action2 = random.choice(["attack", "defend"])

        if action1 == "attack" and action2 == "attack":
            warrior1.attack(warrior2)
            warrior2.attack(warrior1)
        elif action1 == "attack" and action2 == "defend":
            warrior1.attack(warrior2)
            warrior2.defend(warrior1)
        elif action1 == "defend" and action2 == "attack":
            warrior1.defend(warrior2)
            warrior2.attack(warrior1)
        else:
            warrior1.defend(warrior2)
            warrior2.defend(warrior1)

        print(f"{warrior1.name}: здоровье = {warrior1.health}, броня = {warrior1.armor}, выносливость = {warrior1.endurance}")
        print(f"{warrior2.name}: здоровье = {warrior2.health}, броня = {warrior2.armor}, выносливость = {warrior2.endurance}")

    if warrior1.is_alive():
        print(f"{warrior1.name} победил!")
    else:
        print(f"{warrior2.name} победил!")

def test_warrior_class():
    """Тестирование класса Warrior и работы с базой данных."""
    warrior1 = Warrior.create_warrior("Воин 1")
    warrior2 = Warrior.create_warrior("Воин 2")

    assert Warrior.get_warrior_by_name("Воин 1") == warrior1, "Ошибка: Воин 1 не найден"
    assert Warrior.get_warrior_by_name("Воин 2") == warrior2, "Ошибка: Воин 2 не найден"
    
    print("Тестирование классов прошло успешно!")


if __name__ == "__main__":
    # Инициализация базы данных
    initialize_database()

    # Тестирование функционала
    test_warrior_class()

    # Запуск боя между двумя бойцами
    warrior1 = Warrior.get_warrior_by_name("Воин 1")
    warrior2 = Warrior.get_warrior_by_name("Воин 2")

    battle(warrior1, warrior2)
