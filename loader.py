import joblib
import traceback

def load_data(file_path):
    try:
        data = joblib.load(file_path)
        print("Data loaded successfully.")
        print("Loaded data: ", data)
    except Exception as e:
        print("An error occurred while loading the data.")
        print("Error message: ", str(e))
        print("Detailed traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    file_path = "14file/2023-03-20 14:03:29.387629-gain=2.1-film_thickness=1.081e-05/dynamic_simulation_data "
    load_data(file_path)
