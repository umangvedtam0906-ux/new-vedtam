import sys
import update_cert_data

# Redirect stdout to a file internally
with open("python_debug_log.txt", "w", encoding="utf-8") as f:
    original_stdout = sys.stdout
    sys.stdout = f
    try:
        update_cert_data.main()
    except Exception as e:
        print(f"Exception caught: {e}")
    finally:
        sys.stdout = original_stdout
