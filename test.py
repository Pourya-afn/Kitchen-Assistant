import sys
import structure  # Bridge module to the backend/database layers


def test_structure_auth_and_session():
    print("\n--- Test Auth & Session (via structure) ---")
    print("1. Sign up (sign_up)")
    print("2. Login & auto-sync on user switch (login)")
    print("3. Get last user (get_last_user)")
    print("4. Set last user (set_last_user)")
    print("5. Check internet connection (check_internet_connection)")
    print("0. Back")

    sub_choice = input("Select an option: ").strip()

    match sub_choice:
        case "1":
            user = input("Username: ").strip()
            password = input("Password: ").strip()
            try:
                res = structure.sign_up(user, password)
                print("sign_up result:", res)
            except Exception as e:
                print("Sign up error:", e)

        case "2":
            user = input("Username: ").strip()
            password = input("Password: ").strip()
            try:
                res = structure.login(user, password)
                print("login result:", res)
                print("Current active user:", structure.get_last_user())
            except Exception as e:
                print("Login error:", e)

        case "3":
            print("Last recorded user:", structure.get_last_user())

        case "4":
            user = input("Username to record in session: ").strip()
            structure.set_last_user(user)
            print("Session file updated.")

        case "5":
            print("Internet connection status:", structure.check_internet_connection())

        case "0":
            return

        case _:
            print("Invalid option.")


def test_inventory_via_structure():
    print("\n--- Test User Inventory (via structure) ---")
    print("1. Add / increase ingredient quantity")
    print("2. Get user inventory")
    print("0. Back")

    sub_choice = input("Select an option: ").strip()

    match sub_choice:
        case "1":
            if not hasattr(structure, "add_item"):
                print("Function 'add_item' is not defined in 'structure' yet.")
                return
            username = input("Username: ").strip()
            ing_id = int(input("Ingredient ID (ing_id): ").strip())
            quantity = float(input("Quantity: ").strip())
            try:
                res = structure.add_item(username, ing_id, quantity)
                print("Add item result:", res)
            except Exception as e:
                print("Error adding item:", e)

        case "2":
            if not hasattr(structure, "get_inventory"):
                print("Function 'get_inventory' is not defined in 'structure' yet.")
                return
            username = input("Username: ").strip()
            try:
                items = structure.get_inventory(username)
                print("User inventory:", items)
            except Exception as e:
                print("Error reading inventory:", e)

        case "0":
            return

        case _:
            print("Invalid option.")


def main():
    while True:
        print("\n=== Backend Test Menu (structure layer) ===")
        print("1. Test Auth & Session")
        print("2. Test Inventory Operations")
        print("0. Exit")

        choice = input("Enter option number: ").strip()

        match choice:
            case "1":
                test_structure_auth_and_session()
            case "2":
                test_inventory_via_structure()
            case "0":
                print("Exiting test menu.")
                sys.exit(0)
            case _:
                print("Invalid option.")


if __name__ == "__main__":
    main()