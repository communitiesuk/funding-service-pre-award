import importlib
import os

from app import create_app


def load_all_fund_rounds() -> None:
    # Get a list of all Python files in the fund_round_loaders directory
    loader_module_names = [f for f in os.listdir("fund_store/scripts/fund_round_loaders") if f.endswith(".py")]
    for module_name in loader_module_names:
        # Remove the ".py" extension to get the module name
        module_name_without_extension = module_name[:-3]

        # Dynamically import the module
        loader_module = importlib.import_module(
            f"fund_store.scripts.fund_round_loaders.{module_name_without_extension}"
        )

        # Call the main function from the imported module
        if hasattr(loader_module, "main"):
            print(f"Calling main from {module_name_without_extension}")
            loader_module.main()


if __name__ == "__main__":
    with create_app().app_context():
        load_all_fund_rounds()
