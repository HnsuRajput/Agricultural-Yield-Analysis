print("Starting test...")
try:
    import numpy
    print(f"Numpy version: {numpy.__version__}")
except Exception as e:
    print(f"Error importing numpy: {e}")

try:
    import pandas
    print(f"Pandas version: {pandas.__version__}")
except Exception as e:
    print(f"Error importing pandas: {e}")

try:
    import sklearn
    print(f"Scikit-learn version: {sklearn.__version__}")
except Exception as e:
    print(f"Error importing sklearn: {e}")

print("Test completed.") 