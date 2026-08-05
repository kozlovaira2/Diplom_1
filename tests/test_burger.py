import sys
import os
# Добавляем путь к корневой папке
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:
    """Тесты для класса Burger с использованием моков и параметризации"""
    
    @pytest.fixture
    def burger(self):
        """Фикстура для создания экземпляра бургера"""
        return Burger()
    
    @pytest.fixture
    def mock_bun(self):
        """Фикстура для мок-булочки"""
        bun = Mock(spec=Bun)
        bun.get_name.return_value = "test bun"
        bun.get_price.return_value = 100
        return bun
    
    @pytest.fixture
    def mock_ingredient(self):
        """Фикстура для мок-ингредиента"""
        ingredient = Mock(spec=Ingredient)
        ingredient.get_type.return_value = INGREDIENT_TYPE_SAUCE
        ingredient.get_name.return_value = "test sauce"
        ingredient.get_price.return_value = 50
        return ingredient
    
    # === ТЕСТЫ ДЛЯ МЕТОДА __init__ ===
    
    def test_burger_initialization(self, burger):
        """Тест инициализации бургера"""
        assert burger.bun is None
        assert len(burger.ingredients) == 0
        assert burger.ingredients == []
    
    # === ТЕСТЫ ДЛЯ МЕТОДА set_buns ===
    
    def test_set_buns(self, burger, mock_bun):
        """Тест установки булочки"""
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun
    
    def test_set_buns_overwrites_previous(self, burger, mock_bun):
        """Тест перезаписи булочки"""
        first_bun = Mock(spec=Bun)
        burger.set_buns(first_bun)
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun
    
    def test_set_buns_with_none(self, burger):
        """Тест установки None в качестве булочки"""
        burger.set_buns(None)
        assert burger.bun is None
    
    # === ТЕСТЫ ДЛЯ МЕТОДА add_ingredient ===
    
    def test_add_ingredient(self, burger, mock_ingredient):
        """Тест добавления одного ингредиента"""
        burger.add_ingredient(mock_ingredient)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient
    
    def test_add_multiple_ingredients(self, burger):
        """Тест добавления нескольких ингредиентов"""
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        ingredient3 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.add_ingredient(ingredient3)
        
        assert len(burger.ingredients) == 3
        assert burger.ingredients == [ingredient1, ingredient2, ingredient3]
    
    def test_add_ingredient_preserves_order(self, burger):
        """Тест сохранения порядка при добавлении ингредиентов"""
        ingredients = []
        for i in range(5):
            ing = Mock(spec=Ingredient)
            ing.get_name.return_value = f"ingredient_{i}"
            ingredients.append(ing)
            burger.add_ingredient(ing)
        
        assert burger.ingredients == ingredients
    
    # === ТЕСТЫ ДЛЯ МЕТОДА remove_ingredient ===
    
    def test_remove_ingredient_middle(self, burger):
        """Тест удаления ингредиента из середины"""
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        ingredient3 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.add_ingredient(ingredient3)
        
        burger.remove_ingredient(1)
        assert len(burger.ingredients) == 2
        assert burger.ingredients == [ingredient1, ingredient3]
    
    def test_remove_ingredient_first(self, burger):
        """Тест удаления первого ингредиента"""
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ingredient2
    
    def test_remove_ingredient_last(self, burger):
        """Тест удаления последнего ингредиента"""
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        burger.remove_ingredient(1)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == ingredient1
    
    def test_remove_ingredient_until_empty(self, burger):
        """Тест удаления всех ингредиентов"""
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        burger.remove_ingredient(0)
        burger.remove_ingredient(0)
        
        assert len(burger.ingredients) == 0
        assert burger.ingredients == []
    
    # === ТЕСТЫ ДЛЯ МЕТОДА move_ingredient ===
    
    def test_move_ingredient_forward(self, burger):
        """Тест перемещения ингредиента вперед"""
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        ingredient3 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.add_ingredient(ingredient3)
        
        burger.move_ingredient(2, 0)
        assert burger.ingredients == [ingredient3, ingredient1, ingredient2]
    
    def test_move_ingredient_backward(self, burger):
        """Тест перемещения ингредиента назад"""
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        ingredient3 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.add_ingredient(ingredient3)
        
        burger.move_ingredient(0, 2)
        assert burger.ingredients == [ingredient2, ingredient3, ingredient1]
    
    def test_move_ingredient_to_same_position(self, burger):
        """Тест перемещения ингредиента на ту же позицию"""
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        burger.move_ingredient(0, 0)
        assert burger.ingredients == [ingredient1, ingredient2]
    
    def test_move_ingredient_to_end(self, burger):
        """Тест перемещения ингредиента в конец"""
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        ingredient3 = Mock(spec=Ingredient)
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.add_ingredient(ingredient3)
        
        burger.move_ingredient(0, 3)
        assert burger.ingredients == [ingredient2, ingredient3, ingredient1]
    
    # === ТЕСТЫ ДЛЯ МЕТОДА get_price ===
    
    def test_get_price_without_bun_raises_error(self, burger):
        """Тест: вызов get_price без булочки вызывает ошибку AttributeError"""
        with pytest.raises(AttributeError):
            burger.get_price()
    
    def test_get_price_with_bun_only(self, burger, mock_bun):
        """Тест получения цены только с булочкой"""
        burger.set_buns(mock_bun)
        assert burger.get_price() == 200  # 100 * 2
    
    def test_get_price_with_bun_and_ingredients(self, burger, mock_bun):
        """Тест получения цены с булочкой и ингредиентами"""
        burger.set_buns(mock_bun)
        
        ingredient1 = Mock(spec=Ingredient)
        ingredient1.get_price.return_value = 50
        
        ingredient2 = Mock(spec=Ingredient)
        ingredient2.get_price.return_value = 75
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        assert burger.get_price() == 325  # 100*2 + 50 + 75
    
    @pytest.mark.parametrize("bun_price, ingredient_prices, expected_price", [
        (100, [50, 75], 325),
        (200, [100, 150, 200], 850),
        (150, [25], 325),
        (50, [], 100),
        (0, [10, 20], 30),
        (100.5, [25.5, 30.5], 257.0),
        (75, [10, 20, 30, 40], 250),
    ])
    def test_get_price_parametrized(self, burger, bun_price, ingredient_prices, expected_price):
        """Параметризованный тест получения цены с разными значениями"""
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        
        for price in ingredient_prices:
            ingredient = Mock(spec=Ingredient)
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)
        
        assert burger.get_price() == expected_price
    
    # === ТЕСТЫ ДЛЯ МЕТОДА get_receipt ===
    
    def test_get_receipt_without_bun_raises_error(self, burger):
        """Тест: вызов get_receipt без булочки вызывает ошибку AttributeError"""
        with pytest.raises(AttributeError):
            burger.get_receipt()
    
    def test_get_receipt_with_bun_only(self, burger, mock_bun):
        """Тест получения чека только с булочкой"""
        burger.set_buns(mock_bun)
        receipt = burger.get_receipt()
        
        expected = f"(==== test bun ====)\n(==== test bun ====)\n\nPrice: 200"
        assert receipt == expected
    
    def test_get_receipt_with_bun_and_ingredients(self, burger, mock_bun):
        """Тест получения чека с булочкой и ингредиентами"""
        burger.set_buns(mock_bun)
        
        ingredient1 = Mock(spec=Ingredient)
        ingredient1.get_type.return_value = INGREDIENT_TYPE_SAUCE
        ingredient1.get_name.return_value = "hot sauce"
        ingredient1.get_price.return_value = 100
        
        ingredient2 = Mock(spec=Ingredient)
        ingredient2.get_type.return_value = INGREDIENT_TYPE_FILLING
        ingredient2.get_name.return_value = "cutlet"
        ingredient2.get_price.return_value = 200
        
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        
        receipt = burger.get_receipt()
        
        expected = (
            "(==== test bun ====)\n"
            "= sauce hot sauce =\n"
            "= filling cutlet =\n"
            "(==== test bun ====)\n\n"
            "Price: 500"
        )
        assert receipt == expected
    
    def test_get_receipt_with_multiple_ingredients(self, burger, mock_bun):
        """Тест получения чека с несколькими ингредиентами"""
        burger.set_buns(mock_bun)
        
        ingredients_data = [
            (INGREDIENT_TYPE_SAUCE, "hot sauce"),
            (INGREDIENT_TYPE_FILLING, "cutlet"),
            (INGREDIENT_TYPE_SAUCE, "chili sauce"),
            (INGREDIENT_TYPE_FILLING, "dinosaur"),
        ]
        
        for ing_type, ing_name in ingredients_data:
            ingredient = Mock(spec=Ingredient)
            ingredient.get_type.return_value = ing_type
            ingredient.get_name.return_value = ing_name
            ingredient.get_price.return_value = 50
            burger.add_ingredient(ingredient)
        
        receipt = burger.get_receipt()
        lines = receipt.split('\n')
        
        # Проверяем, что все ингредиенты присутствуют в правильном порядке
        for i, (ing_type, ing_name) in enumerate(ingredients_data):
            assert f"= {ing_type.lower()} {ing_name} =" in lines[i + 1]
        
        assert len(lines) == len(ingredients_data) + 4
    
    def test_get_receipt_preserves_ingredient_order(self, burger, mock_bun):
        """Тест: чек сохраняет порядок ингредиентов"""
        burger.set_buns(mock_bun)
        
        ingredients = []
        for i in range(3):
            ing = Mock(spec=Ingredient)
            ing.get_type.return_value = INGREDIENT_TYPE_SAUCE
            ing.get_name.return_value = f"ingredient_{i}"
            ing.get_price.return_value = 10
            ingredients.append(ing)
            burger.add_ingredient(ing)
        
        receipt = burger.get_receipt()
        lines = receipt.split('\n')
        
        # Проверяем порядок ингредиентов в чеке
        for i in range(3):
            assert f"= sauce ingredient_{i} =" in lines[i + 1]
    
    @pytest.mark.parametrize("bun_name, ingredients_data", [
        (
            "black bun",
            [("SAUCE", "hot sauce"), ("FILLING", "cutlet")],
        ),
        (
            "white bun",
            [("FILLING", "dinosaur")],
        ),
        (
            "red bun",
            [],
        ),
        (
            "special bun",
            [("SAUCE", "chili"), ("SAUCE", "sour cream"), ("FILLING", "sausage")],
        ),
        (
            "test bun",
            [("SAUCE", "sauce1"), ("SAUCE", "sauce2"), ("FILLING", "filling1"), ("FILLING", "filling2")],
        ),
    ])
    def test_get_receipt_parametrized(self, burger, bun_name, ingredients_data):
        """Параметризованный тест получения чека с разными данными"""
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)
        
        for ing_type, ing_name in ingredients_data:
            ingredient = Mock(spec=Ingredient)
            ingredient.get_type.return_value = ing_type
            ingredient.get_name.return_value = ing_name
            ingredient.get_price.return_value = 50
            burger.add_ingredient(ingredient)
        
        receipt = burger.get_receipt()
        receipt_lines = receipt.split('\n')
        
        # Проверяем, что булочка отображается дважды
        bun_line = f"(==== {bun_name} ====)"
        assert receipt_lines[0] == bun_line
        
        # Вторая булочка на позиции len(receipt_lines) - 3
        # Потому что последняя строка - цена, перед ней пустая строка
        assert receipt_lines[-3] == bun_line
        
        # Проверяем наличие всех ингредиентов
        for ing_type, ing_name in ingredients_data:
            assert f"= {ing_type.lower()} {ing_name} =" in receipt_lines
        
        # Проверяем, что цена присутствует
        assert "Price:" in receipt_lines[-1]
        
        # Проверяем, что перед ценой есть пустая строка
        assert receipt_lines[-2] == ""