from gui.main_gui import run_main_gui
from utils.data_manager import ensure_user_data_exists

if __name__ == "__main__":
    ensure_user_data_exists()
    run_main_gui()
