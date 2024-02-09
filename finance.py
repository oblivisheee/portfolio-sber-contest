from decimal import Decimal
from enum import Enum
import os
import json

class AssetPrice(Enum):
    LKOH = Decimal(5896)
    SBER = Decimal(250)

class Portfolio:
    def __init__(self):
        self.assets = {}
        self.load_portfolio()

    def buy_asset(self, asset, quantity):
        self.assets[asset] = self.assets.get(asset, Decimal(0)) + quantity
        self.save_portfolio()

    def sell_asset(self, asset, quantity):
        if asset in self.assets:
            if self.assets[asset] >= quantity:
                self.assets[asset] -= quantity
            else:
                print(f"Not enough {asset.name} to sell.")
        else:
            print(f"You don't have {asset.name} assets in the portfolio.")
        self.save_portfolio()

    def calculate_portfolio_value(self):
        total_value = sum(asset.value * quantity for asset, quantity in self.assets.items())
        return total_value

    def save_portfolio(self):
        asset_dict = {asset.name: str(quantity) for asset, quantity in self.assets.items()}
        with open('portfolio.json', 'w') as file:
            json.dump(asset_dict, file)

    def load_portfolio(self):
        try:
            with open('portfolio.json', 'r') as file:
                asset_dict = json.load(file)
                self.assets = {AssetPrice[asset_name]: Decimal(value) for asset_name, value in asset_dict.items() if asset_name in AssetPrice.__members__}
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.assets = {}

class ChooseFunc:
    @staticmethod
    def buy_asset_func():
        os.system('clear')
        print('Assets to buy: LKOH, SBER')
        asset_str = input("Enter asset: ").upper()
        asset = AssetPrice[asset_str] if asset_str in AssetPrice.__members__ else None
        if not asset:
            print(f"{asset_str} is not a valid asset.")
            print("You will return to the main menu.")
            input("Press Enter to continue...")
            os.system('clear')
            return
        current_quantity = portfolio.assets.get(asset, Decimal(0))
        print(f"Your current quantity of {asset.name}: {current_quantity}")
        print(f"In Rubles: {asset.value * current_quantity}")
        print("Write quantity not in Rubles.\n")
        quantity = Decimal(input("Enter quantity to buy: "))
        portfolio.buy_asset(asset, quantity)
        os.system('clear')

    @staticmethod
    def sell_asset_func():
        os.system('clear')
        print('Assets to sell: LKOH, SBER')
        asset_str = input("Enter asset: ").upper()
        asset = AssetPrice[asset_str] if asset_str in AssetPrice.__members__ else None
        if not asset:
            print(f"{asset_str} is not a valid asset.")
            print("You will return to the main menu.")
            input("Press Enter to continue...")
            os.system('clear')
            return
        current_quantity = portfolio.assets.get(asset, Decimal(0))
        print(f"Your current quantity of {asset.name}: {current_quantity}")
        print(f"In Rubles: {asset.value * current_quantity}")
        print("Write quantity not in Rubles.\n")
        quantity = Decimal(input("Enter quantity to sell: "))
        portfolio.sell_asset(asset, quantity)
        os.system('clear')

    @staticmethod
    def main_menu():
        os.system('clear')
        while True:
            print("Welcome to the portfolio manager!")
            portfolio_value = portfolio.calculate_portfolio_value()
            print(f"Your current portfolio value: {portfolio_value}")
            if os.path.exists('portfolio.json') and os.path.getsize('portfolio.json') > 0:
                print("\n----------------------------------------------------\n")
                for asset, quantity in portfolio.assets.items():
                    print(f"Your current quantity of {asset.name}: {quantity}.", f"In Rubles: {asset.value * quantity}")
                print("\n----------------------------------------------------\n")
            print("1. Buy asset")
            print("2. Sell asset")
            print("3. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
                os.system('clear')
                ChooseFunc.buy_asset_func()
            elif choice == '2':
                os.system('clear')
                ChooseFunc.sell_asset_func()
            elif choice == '3':
                os.system('clear')
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    portfolio = Portfolio()
    ChooseFunc.main_menu()
