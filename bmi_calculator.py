import tkinter as tk
import customtkinter as ctk
import numpy as np

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")
class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.geometry("690x400")
		self.title("BMI Calculator")
		self.grid_columnconfigure((0, 1), weight=1)
		self.modes = {
						"Metric":{
								"event":self.calculate_metric,
								"height":"centimeters",
								"weight":"kilograms"
								},		
						"Imperial":{
								"event":self.calculate_imperial,
								"height":"inches",
								"weight":"pounds"
								}
						}
		# inputs and calculate button
		self.frame = ctk.CTkFrame(self)
		self.frame.grid(row=0, column=0, sticky="nsew", padx=(20, 0), pady=(30,0))
		self.enter_weight = ctk.CTkEntry(self.frame, width=250)
		self.enter_weight.pack(anchor=tk.CENTER, pady=(20, 0), padx=(30, 30))
		self.enter_height = ctk.CTkEntry(self.frame, width=250)
		self.enter_height.pack(anchor=tk.CENTER, pady=10, padx=(30, 30))
		self.calculate_button = ctk.CTkButton(self.frame, text="Caluclate")
		self.calculate_button.pack(anchor=tk.CENTER, pady=15)
		
		# optionmenu and clear button
		self.frame_2 = ctk.CTkFrame(self)
		self.frame_2.grid(row=0, column=1, sticky="nsew", padx=(5, 20), pady=(30,0))
		self.select_mode_menu = ctk.CTkOptionMenu(self.frame_2, values=["Metric", "Imperial"], command=self.select_mode)
		self.select_mode_menu.pack(padx=30, expand=True)
		self.clear_button = ctk.CTkButton(self.frame_2, text="Clear", command=self.clear_button_event)
		self.clear_button.pack(pady=(10, 30), padx=30)
		
		# outputs
		self.frame_3 = ctk.CTkFrame(self)
		self.frame_3.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(20, 20), pady=(5, 30))
		self.output_display = ctk.CTkEntry(self.frame_3, height=55, placeholder_text="BMI and comment")
		self.output_display.pack(pady=(15, 15), padx=(30, 30), fill=tk.BOTH)
		self.output_display.configure(state="disabled")
		
		# default
		self.select_mode_menu.set("Select mode")
		
	# functions
	def get_comment(self, bmi: float):
		underweight_range = [round(val, 1) for val in np.arange(0, 18.5, 0.1)]
		healthy_range = [round(val, 1) for val in np.arange(18.5, 25.1, 0.1)]
		if bmi in underweight_range:
			comment = ". You are underweight."
		elif bmi in healthy_range:
			comment = ". You have an healthy weight."
		else:
			comment = ". You are overweight."
		return comment
	
	def update_output_display(self, msg):
		self.output_display.configure(state="normal")
		self.output_display.configure(placeholder_text=msg)
		self.output_display.configure(state="disabled")
	
	def calculate_metric(self):
		height: float = float(self.enter_height.get())
		weight: float = float(self.enter_weight.get())
		_ = weight / (height/100)**2
		bmi = round(_, 1)
		msg = f"Your BMI is {bmi}"
		msg += self.get_comment(bmi)
		self.update_output_display(msg)
		
	def calculate_imperial(self):
		height: float = float(self.enter_height.get())
		weight: float = float(self.enter_weight.get())
		_ = (weight/(height**2)) * 703
		bmi = round(_, 1)
		msg = f"Your BMI is {bmi}"
		msg += self.get_comment(bmi)
		self.update_output_display(msg)
		
	def clear_button_event(self):
		weight_unit = self.modes.get(self.mode).get("weight")
		height_unit = self.modes.get(self.mode).get("height")
		self.enter_weight.delete(0, tk.END)
		self.enter_weight.configure(placeholder_text=f"Your weight in {weight_unit}")
		self.enter_height.delete(0, tk.END)
		self.enter_height.configure(placeholder_text=f"Your height in {height_unit}")
		output_display_msg = "BMI and comment"
		self.update_output_display(output_display_msg)
		
	def select_mode(self, mode: str):
		self.mode = mode
		button_mode = self.modes.get(mode).get("event")
		self.calculate_button.configure(command=button_mode)
		self.clear_button.invoke()
		

if __name__ == "__main__":
	app = App()
	app.mainloop()