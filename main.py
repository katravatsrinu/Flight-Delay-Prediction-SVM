import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

# Load your modified synthetic flight delay dataset without 'FlightDelay' column
def load_data():
    try:
        if os.path.exists('flight_delay_dataset.csv'):
            data = pd.read_csv('flight_delay_dataset.csv')  # Replace with your modified dataset file path
            return data
        else:
            messagebox.showerror("File Not Found", "The dataset file 'flight_delay_dataset.csv' is missing.")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the dataset: {str(e)}")
        return None

data = load_data()

if data is None:
    exit()

# Split the dataset into features (X) and labels (y)
X = data[['DepTime', 'ArrTime', 'Airline', 'Distance', 'WeatherConditions', 'PreviousFlightDelay']]
y = data['PreviousFlightDelay']  # Use 'PreviousFlightDelay' as the target variable

# Encode categorical variables using Label Encoding
label_encoders = {}
categorical_columns = ['Airline', 'WeatherConditions']

for col in categorical_columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Split the dataset into a training set and a testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train your Support Vector Machine classifier
model = SVC(kernel='linear', random_state=42)
model.fit(X_train, y_train)

# Function to handle model prediction
def predict_delay():
    try:
        # Get input values from the user
        dep_time = int(dep_time_entry.get())
        arr_time = int(arr_time_entry.get())
        airline = airline_var.get()
        airline_encoded = label_encoders['Airline'].transform([airline])[0]
        distance = int(distance_entry.get())
        weather_conditions = weather_var.get()
        weather_encoded = label_encoders['WeatherConditions'].transform([weather_conditions])[0]
        
        # Validate Previous Flight Delay input (0 or 1)
        previous_flight_delay = previous_delay_var.get()
        if previous_flight_delay not in ['0', '1']:
            messagebox.showerror("Invalid Input", "Previous Flight Delay should be either 0 or 1.")
            return
        previous_flight_delay = int(previous_flight_delay)

        # Create an input data array
        input_data = [dep_time, arr_time, airline_encoded, distance, weather_encoded, previous_flight_delay]

        # Make a prediction using the trained model
        prediction = model.predict([input_data])

        # Show the prediction result
        if prediction[0] == 0:
            result_label.config(text="No Previous Delay", foreground="black")
        else:
            result_label.config(text="Previous Delay", foreground="black")
    except ValueError as e:
        # Handle input validation errors
        messagebox.showerror("Invalid Input", f"Error: {e}")
    except Exception as e:
        # Catch any other errors
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

# Create a GUI window
root = tk.Tk()
root.title("Previous Flight Delay Prediction")

# Configure the background color
root.configure(bg='skyblue')

# Set the size of the interface
root.geometry("700x500")  # Increased width to 700

# Custom font
custom_font = ("Imprint MT Shadow", 12, 'bold')

# Create a frame to center labels and input fields
frame = ttk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Create labels and entry widgets with custom font using the grid geometry manager
tk.Label(frame, text="Departure Time (HHMM):", font=custom_font).grid(row=0, column=0, pady=10, sticky='e')  # Increased pady
dep_time_entry = ttk.Entry(frame, font=("Imprint MT Shadow", 12))
dep_time_entry.grid(row=0, column=1, padx=10, pady=10)  # Increased pady

tk.Label(frame, text="Arrival Time (HHMM):", font=custom_font).grid(row=1, column=0, pady=10, sticky='e')  # Increased pady
arr_time_entry = ttk.Entry(frame, font=("Imprint MT Shadow", 12))
arr_time_entry.grid(row=1, column=1, padx=10, pady=10)  # Increased pady

# Create a custom style for the dropdown options
dropdown_style = ttk.Style()
dropdown_style.configure("Custom.TMenubutton", font=("Imprint MT Shadow", 12))

tk.Label(frame, text="Airline:", font=custom_font).grid(row=2, column=0, pady=10, sticky='e')  # Increased pady
airline_var = tk.StringVar()
airline_var.set('Delta')  # Default value
airline_dropdown = ttk.OptionMenu(frame, airline_var, 'Delta', 'United', 'American', 'JetBlue', 'Southwest', style="Custom.TMenubutton")
airline_dropdown.grid(row=2, column=1, padx=10, pady=10)  # Increased pady

tk.Label(frame, text="Distance (miles):", font=custom_font).grid(row=3, column=0, pady=10, sticky='e')  # Increased pady
distance_entry = ttk.Entry(frame, font=("Imprint MT Shadow", 12))
distance_entry.grid(row=3, column=1, padx=10, pady=10)  # Increased pady

tk.Label(frame, text="Weather Conditions:", font=custom_font).grid(row=4, column=0, pady=10, sticky='e')  # Increased pady
weather_var = tk.StringVar()
weather_var.set('Clear')  # Default value
weather_dropdown = ttk.OptionMenu(frame, weather_var, 'Clear', 'Cloudy', 'Rainy', 'Snowy', style="Custom.TMenubutton")
weather_dropdown.grid(row=4, column=1, padx=10, pady=10)  # Increased pady

tk.Label(frame, text="Previous Flight Delay (0 or 1):", font=custom_font).grid(row=5, column=0, pady=10, sticky='e')  # Increased pady
previous_delay_var = ttk.Entry(frame, font=("Imprint MT Shadow", 12))
previous_delay_var.grid(row=5, column=1, padx=10, pady=10)  # Increased pady

# Button to trigger prediction with font color, background color, and font text
style = ttk.Style()
style.configure('Custom.TButton', font=("Imprint MT Shadow", 12), background='skyblue')
predict_button = ttk.Button(frame, text="Predict Previous Delay", command=predict_delay, style='Custom.TButton')
predict_button.grid(row=6, column=0, columnspan=2, pady=20)  # Increased pady

# Label to display prediction result with black color, bold text, and increased font size
result_label = ttk.Label(frame, text="", font=("Imprint MT Shadow", 18, "bold"), foreground="black")
result_label.grid(row=7, column=0, columnspan=2, pady=10)

# Run the GUI application
root.mainloop()
