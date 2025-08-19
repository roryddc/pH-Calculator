import tkinter as tk
import json
import math
from pathlib import Path

COMPOUNDS_FILE = Path("KaValues.json")
with open(COMPOUNDS_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)
    ACID = {el["name"]: {"type": el.get("type", ""), "Ka": el.get("Ka", [])}
            for el in data.get("acids", [])}
    ACID_NAMES = list(ACID.keys())

    BASE = {el["name"]: {"type": el.get("type", ""), "Kb": el.get("Kb", [])}
            for el in data.get("bases", [])}
    BASE_NAMES = list(BASE.keys())

class pHCalculator:
    def __init__(self, window):
        self.window = window
        self.variables()
        window.title("pH Calculator")
        window.configure(bg="black")
        window.geometry("810x500")

        self.intro_text()
        self.create_layout()

    def variables(self):
        self.selected_option = tk.StringVar()
        self.acid_type = tk.StringVar()
        self.ka_value_other = tk.StringVar()
        self.specific_acid_concentration = tk.StringVar()
        self.acid_concentration_other = tk.StringVar()
        self.specific_temperature_acid = tk.DoubleVar(value=25)
        self.specific_temperature_acid_other = tk.DoubleVar(value=25)

        self.base_type = tk.StringVar()
        self.kb_value_other = tk.StringVar()
        self.specific_base_concentration = tk.StringVar()
        self.base_concentration_other = tk.StringVar()
        self.specific_temperature_base = tk.DoubleVar(value=25)
        self.specific_temperature_base_other = tk.DoubleVar(value=25)

        self.acid_label = None
        self.acid_selection = None
        self.base_label = None
        self.base_selection = None
        self.get_concentration_acid = None
        self.concentration = None
        self.ka_other_acid_label = None
        self.ka_other_acid_entry = None
        self.get_concentration_base = None
        self.kb_other_base_label = None
        self.kb_other_base_entry = None
        self.get_concentration_acid_other = None
        self.get_concentration_base_other = None
        self.get_temperature_acid_other = None
        self.temperature = None
        self.calculate_button = None
        self.get_temperature_base_other = None
        self.error_label = None
        self.Kwtemperature = None
        self.print_pH = None
        self.print_hydrogen_ion = None
        self.print_pOH = None
        self.print_hydroxide_ion = None

    def intro_text(self):
        self.title = tk.Label(self.window, text="pH Calculator",
                         fg="white", bg="black", font=("Times New Roman", 30))
        self.title.grid(row=0, column=0, columnspan=3, pady=(20, 1), sticky="w", padx=20)

        self.description = tk.Label(self.window,
                               text="Calculate pH, pOH, and concentrations for acid/base solutions",
                               bg="black", fg="white", font=("Times New Roman", 20), justify="left")
        self.description.grid(row=1, column=0, columnspan=3, pady=(1, 15), sticky="w", padx=20)

    def create_layout(self):
        self.introduction = tk.Label(self.window, text="I want to calculate the pH from...",
                                fg="white", bg="black", font=("Times New Roman", 15, "bold"))
        self.introduction.grid(row=2, column=0, pady=(0, 1), padx=20, sticky="w")

        options = [
            "acid concentration",
            "base concentration"
        ]
        self.selected_option.set("Select a method")

        self.selection = tk.OptionMenu(self.window, self.selected_option,
                                  *options, command=self.show_selection)
        self.selection.config(font=("Times New Roman", 10), width=50)
        self.selection.grid(row=3, column=0, padx=20, pady=(1, 0), sticky="w")

    def reset_widgets_show_selection(self):
        for widget_name in ["acid_label", "acid_selection", "base_label", "base_selection"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def show_selection(self, method):
        self.reset_widgets_show_selection()

        method = self.selected_option.get()
        if method == "acid concentration":
            self.acid_label = tk.Label(self.window, text="What type of acid?",
                                  fg="white", bg="black", font=("Times New Roman", 15, "bold"))
            self.acid_label.grid(row=4, column=0, pady=(0, 1), padx=20, sticky="w")

            self.acid_type.set("Select an acid")
            self.acid_selection = tk.OptionMenu(self.window, self.acid_type, *ACID_NAMES, command=self.concentration_acid)
            self.acid_selection.config(font=("Times New Roman", 10), width=50)
            self.acid_selection.grid(row=5, column=0, padx=20, pady=(1, 0), sticky="w")

        elif method == "base concentration":
            self.base_label = tk.Label(self.window, text="What type of base?",
                                  fg="white", bg="black", font=("Times New Roman", 15, "bold"))
            self.base_label.grid(row=4, column=0, pady=(0, 1), padx=20, sticky="w")

            self.base_type.set("Select a base")
            self.base_selection = tk.OptionMenu(self.window, self.base_type, *BASE_NAMES, command=self.concentration_base)
            self.base_selection.config(font=("Times New Roman", 10), width=50)
            self.base_selection.grid(row=5, column=0, padx=20, pady=(1, 0), sticky="w")

    def reset_widgets_concentration(self):
        for widget_name in ["get_concentration_acid", "concentration", "ka_other_acid_label", "ka_other_acid_entry",
                            "get_concentration_base", "kb_other_base_label", "kb_other_base_entry"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def concentration_acid(self, acid_type):
        self.reset_widgets_concentration()

        acid = self.acid_type.get()
        if acid == "Other":
            self.ka_acid_other()
        else:
            self.get_concentration_acid = tk.Label(self.window, text="What is the concentration of the acid (M)?",
                                              fg="white", bg="black", font=("Times New Roman", 15, "bold"))
            self.get_concentration_acid.grid(row=6, column=0, padx=20, pady=(5, 0), sticky="w")

            self.concentration = tk.Entry(self.window, textvariable=self.specific_acid_concentration, width=57)
            self.concentration.grid(row=7, column=0, pady=(0, 0), padx=20, sticky="w")
            self.concentration.bind("<Return>", lambda event: self.validate_concentration_acid())

    def validate_concentration_acid(self):
        try:
            check = float(self.concentration.get())
            for widget_name in ["error_label"]:
                widget = getattr(self, widget_name, None)
                if widget is not None:
                    widget.destroy()
                    setattr(self, widget_name, None)
            self.temperature_acid()

        except ValueError:
            self.error_label = tk.Label(
                self.window,
                text="Please enter a valid numeric concentration.",
                fg="red", bg="black",
                font=("Times New Roman", 12, "italic")
            )
            self.error_label.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")

    def concentration_base(self, base_type):
        self.reset_widgets_concentration()

        base = self.base_type.get()
        if base == "Other":
            self.kb_base_other()
        else:
            self.get_concentration_base = tk.Label(self.window, text="What is the concentration of the base (M)?",
                                              fg="white", bg="black", font=("Times New Roman", 15, "bold"))
            self.get_concentration_base.grid(row=6, column=0, padx=20, pady=(5, 0), sticky="w")

            self.concentration = tk.Entry(self.window, textvariable=self.specific_base_concentration, width=57)
            self.concentration.grid(row=7, column=0, pady=(0, 0), padx=20, sticky="w")
            self.concentration.bind("<Return>", lambda event: self.validate_concentration_base())

    def validate_concentration_base(self):
        try:
            check = float(self.concentration.get())
            for widget_name in ["error_label"]:
                widget = getattr(self, widget_name, None)
                if widget is not None:
                    widget.destroy()
                    setattr(self, widget_name, None)
            self.temperature_base()

        except ValueError:
            self.error_label = tk.Label(
                self.window,
                text="Please enter a valid numeric concentration.",
                fg="red", bg="black",
                font=("Times New Roman", 12, "italic")
            )
            self.error_label.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")

    def reset_widgets_ka_kb_other_values(self):
        for widget_name in ["ka_other_acid_label", "ka_other_acid_entry", "kb_other_base_label", "kb_other_base_entry"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def ka_acid_other(self):
        self.reset_widgets_ka_kb_other_values()

        self.ka_other_acid_label = tk.Label(self.window, text="What is its Ka value (e.g. 3.2e-5)?",
                                      fg="white", bg="black", font=("Times New Roman", 15, "bold"))
        self.ka_other_acid_label.grid(row=6, column=0, pady=(0, 1), padx=20, sticky="w")

        self.ka_other_acid_entry = tk.Entry(self.window, textvariable=self.ka_value_other, width=57)
        self.ka_other_acid_entry.grid(row=7, column=0, pady=(0, 1), padx=20, sticky="w")
        self.ka_other_acid_entry.bind("<Return>", lambda event: self.validate_ka_acid_other())

    def validate_ka_acid_other(self):
        try:
            check = float(self.ka_other_acid_entry.get())
            for widget_name in ["error_label"]:
                widget = getattr(self, widget_name, None)
                if widget is not None:
                    widget.destroy()
                    setattr(self, widget_name, None)
            self.concentration_acid_other()

        except ValueError:
            self.error_label = tk.Label(
                self.window,
                text="Please enter a valid numeric Ka value.",
                fg="red", bg="black",
                font=("Times New Roman", 12, "italic")
            )
            self.error_label.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")

    def kb_base_other(self):
        self.reset_widgets_ka_kb_other_values()

        self.kb_other_base_label = tk.Label(self.window, text="What is its Kb value (e.g. 3.2e-5)?",
                                      fg="white", bg="black", font=("Times New Roman", 15, "bold"))
        self.kb_other_base_label.grid(row=6, column=0, pady=(0, 1), padx=20, sticky="w")

        self.kb_other_base_entry = tk.Entry(self.window, textvariable=self.kb_value_other, width=57)
        self.kb_other_base_entry.grid(row=7, column=0, pady=(0, 1), padx=20, sticky="w")
        self.kb_other_base_entry.bind("<Return>", lambda event: self.validate_kb_base_other())

    def validate_kb_base_other(self):
        try:
            check = float(self.kb_other_base_entry.get())
            for widget_name in ["error_label"]:
                widget = getattr(self, widget_name, None)
                if widget is not None:
                    widget.destroy()
                    setattr(self, widget_name, None)
            self.concentration_base_other()

        except ValueError:
            self.error_label = tk.Label(
                self.window,
                text="Please enter a valid numeric Kb value.",
                fg="red", bg="black",
                font=("Times New Roman", 12, "italic")
            )
            self.error_label.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")

    def reset_widgets_concentration_other(self):
        for widget_name in ["get_concentration_acid_other", "concentration", "get_concentration_base_other"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def concentration_acid_other(self):
        self.reset_widgets_concentration_other()

        self.get_concentration_acid_other = tk.Label(self.window, text="What is the concentration of the acid (M)?",
                                                fg="white", bg="black", font=("Times New Roman", 15, "bold"))
        self.get_concentration_acid_other.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")

        self.concentration = tk.Entry(self.window, textvariable=self.acid_concentration_other, width=57)
        self.concentration.grid(row=9, column=0, pady=(0, 0), padx=20, sticky="w")
        self.concentration.bind("<Return>", lambda event: self.validate_concentration_acid_other())

    def validate_concentration_acid_other(self):
        try:
            check = float(self.concentration.get())
            for widget_name in ["error_label"]:
                widget = getattr(self, widget_name, None)
                if widget is not None:
                    widget.destroy()
                    setattr(self, widget_name, None)
            self.temperature_acid()

        except ValueError:
            self.error_label = tk.Label(
                self.window,
                text="Please enter a valid numeric concentration.",
                fg="red", bg="black",
                font=("Times New Roman", 12, "italic")
            )
            self.error_label.grid(row=10, column=0, padx=20, pady=(5, 0), sticky="w")

    def concentration_base_other(self):
        self.reset_widgets_concentration_other()

        self.get_concentration_base_other = tk.Label(self.window, text="What is the concentration of the base (M)?",
                                                fg="white", bg="black", font=("Times New Roman", 15, "bold"))
        self.get_concentration_base_other.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")

        self.concentration = tk.Entry(self.window, textvariable=self.base_concentration_other, width=57)
        self.concentration.grid(row=9, column=0, pady=(0, 0), padx=20, sticky="w")
        self.concentration.bind("<Return>", lambda event: self.validate_concentration_base_other())

    def validate_concentration_base_other(self):
        try:
            check = float(self.concentration.get())
            for widget_name in ["error_label"]:
                widget = getattr(self, widget_name, None)
                if widget is not None:
                    widget.destroy()
                    setattr(self, widget_name, None)
            self.temperature_base()

        except ValueError:
            self.error_label = tk.Label(
                self.window,
                text="Please enter a valid numeric concentration.",
                fg="red", bg="black",
                font=("Times New Roman", 12, "italic")
            )
            self.error_label.grid(row=10, column=0, padx=20, pady=(5, 0), sticky="w")

    def reset_widgets_temperature(self):
        for widget_name in ["get_temperature_acid_other", "temperature", "calculate_button", "get_temperature_base_other"]:
            widget = getattr(self, widget_name, None)
            if widget is not None:
                widget.destroy()
                setattr(self, widget_name, None)

    def temperature_acid(self):
        self.reset_widgets_temperature()

        acid = self.acid_type.get()
        if acid == "Other":
            self.get_temperature_acid_other = tk.Label(self.window, text="At what temperature (°C)?",
                                                  fg="white", bg="black", font=("Times New Roman", 15, "bold"))
            self.get_temperature_acid_other.grid(row=10, column=0, padx=20, pady=(5, 0), sticky="w")

            self.temperature = tk.Spinbox(self.window, from_=1, to=100, textvariable=self.specific_temperature_acid_other,
                                     width=55)
            self.temperature.grid(row=11, column=0, padx=20, pady=(10, 0), sticky="w")

            self.calculate_button = tk.Button(self.window, text="Calculate!", command=self.pH_calculations_acid)
            self.calculate_button.config(font=("Times New Roman", 10))
            self.calculate_button.grid(row=12, column=0, padx=20, pady=(1, 0), sticky="w")

            self.reset_button = tk.Button(self.window, text="Reset", command=self.remove_widgets_all)
            self.reset_button.config(font=("Times New Roman", 10))
            self.reset_button.grid(row=12, column=0, padx=87, pady=(1, 0), sticky="w")

        else:
            self.get_temperature_acid_other = tk.Label(self.window, text="At what temperature (°C)?",
                                                  fg="white", bg="black", font=("Times New Roman", 15, "bold"))
            self.get_temperature_acid_other.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")

            self.temperature = tk.Spinbox(self.window, from_=1, to=100, textvariable=self.specific_temperature_acid,
                                     width=55)
            self.temperature.grid(row=9, column=0, padx=20, pady=(5, 0), sticky="w")

            self.calculate_button = tk.Button(self.window, text="Calculate!", command=self.pH_calculations_acid)
            self.calculate_button.config(font=("Times New Roman", 10))
            self.calculate_button.grid(row=10, column=0, padx=20, pady=(1, 0), sticky="w")

            self.reset_button = tk.Button(self.window, text="Reset", command=self.remove_widgets_all)
            self.reset_button.config(font=("Times New Roman", 10))
            self.reset_button.grid(row=10, column=0, padx=87, pady=(1, 0), sticky="w")

    def temperature_base(self):
        self.reset_widgets_temperature()

        base = self.base_type.get()
        if base == "Other":
            get_temperature_base_other = tk.Label(self.window, text="At what temperature (°C)?",
                                                  fg="white", bg="black", font=("Times New Roman", 15, "bold"))
            get_temperature_base_other.grid(row=10, column=0, padx=20, pady=(5, 0), sticky="w")

            temperature = tk.Spinbox(self.window, from_=1, to=100, textvariable=self.specific_temperature_base_other,
                                     width=55)
            temperature.grid(row=11, column=0, padx=20, pady=(5, 0), sticky="w")

            self.calculate_button = tk.Button(self.window, text="Calculate!", command=self.pOH_calculations_base)
            self.calculate_button.config(font=("Times New Roman", 10))
            self.calculate_button.grid(row=12, column=0, padx=20, pady=(1, 0), sticky="w")

            self.reset_button = tk.Button(self.window, text="Reset", command=self.remove_widgets_all)
            self.reset_button.config(font=("Times New Roman", 10))
            self.reset_button.grid(row=12, column=0, padx=87, pady=(1, 0), sticky="w")
        else:
            get_temperature_base_other = tk.Label(self.window, text="At what temperature (°C)?",
                                                  fg="white", bg="black", font=("Times New Roman", 15, "bold"))
            get_temperature_base_other.grid(row=8, column=0, padx=20, pady=(5, 0), sticky="w")

            temperature = tk.Spinbox(self.window, from_=1, to=100, textvariable=self.specific_temperature_base,
                                     width=55)
            temperature.grid(row=9, column=0, padx=20, pady=(5, 0), sticky="w")

            self.calculate_button = tk.Button(self.window, text="Calculate!", command=self.pOH_calculations_base)
            self.calculate_button.config(font=("Times New Roman", 10))
            self.calculate_button.grid(row=10, column=0, padx=20, pady=(10, 0), sticky="w")

            self.reset_button = tk.Button(self.window, text="Reset", command=self.remove_widgets_all)
            self.reset_button.config(font=("Times New Roman", 10))
            self.reset_button.grid(row=10, column=0, padx=87, pady=(10, 0), sticky="w")

    def pH_calculations_acid(self):
        acid = self.acid_type.get()
        acid_info = ACID.get(acid, {"type": "", "Ka": []})
        acid_type = acid_info.get("type", "").lower()
        Ka_values = acid_info.get("Ka", [])

        if acid == "Other":
            other_acid_ka_value = float(self.ka_value_other.get())
            other_acid_concentration = float(self.acid_concentration_other.get())
            temperature = float(self.specific_temperature_acid_other.get())

            if other_acid_ka_value > 1:
                hydrogen_ion_concentration = other_acid_concentration

            elif 0.1 <= other_acid_ka_value <= 1:
                hydrogen_ion_concentration = (-other_acid_ka_value + math.sqrt(other_acid_ka_value ** 2
                                                                               + 4 * other_acid_ka_value * other_acid_concentration)) / 2

            else:
                hydrogen_ion_concentration = math.sqrt(other_acid_ka_value * other_acid_concentration)

        else:
            acid_concentration = float(self.specific_acid_concentration.get())
            temperature = float(self.specific_temperature_acid.get())

            if "strong" in acid_type:
                hydrogen_ion_concentration = acid_concentration

            else:
                if "mono" in acid_type:
                    hydrogen_ion_concentration = math.sqrt(acid_concentration * Ka_values[0])

                elif "di" in acid_type:
                    hydrogen_ion_concentration = self.polyprotic_acid_calculations(acid_concentration, Ka_values)

                else:
                    hydrogen_ion_concentration = self.polyprotic_acid_calculations(acid_concentration, Ka_values)

        self.Kw = 1e-14 * 10 ** (0.033 * (temperature - 25))
        hydroxide_ion_concentration = self.Kw / hydrogen_ion_concentration
        pH = -math.log10(hydrogen_ion_concentration)
        pOH = -math.log10(hydroxide_ion_concentration)

        self.print_pH = pH
        self.print_hydrogen_ion = hydrogen_ion_concentration
        self.print_pOH = pOH
        self.print_hydroxide_ion = hydroxide_ion_concentration

        self.show_pH_pOH_results_values()

    def polyprotic_acid_calculations(self, acid_concentration, Ka_values):
        hydrogen_ions = 0.0
        Ka1 = Ka_values[0]

        if Ka1 > 1:
            hydrogen_ions += acid_concentration
            HA_concentration = 0

        else:
            hydrogen_ions = (-Ka1 + math.sqrt(Ka1 ** 2 + 4 * Ka1 * acid_concentration)) / 2
            HA_concentration = acid_concentration - hydrogen_ions

        if len(Ka_values) > 1:
            Ka2 = Ka_values[1]
            hydrogen_ions_2 = (Ka2 * HA_concentration) / (hydrogen_ions + Ka2)
            hydrogen_ions += hydrogen_ions_2
            acid_concentration_2 = HA_concentration - hydrogen_ions_2

        else:
            acid_concentration_2 = 0

        if len(Ka_values) > 2:
            Ka3 = Ka_values[2]
            hydrogen_ions_3 = (Ka3 * acid_concentration_2) / (hydrogen_ions + Ka3)
            hydrogen_ions += hydrogen_ions_3

        return hydrogen_ions

    def pOH_calculations_base(self):
        base = self.base_type.get()
        base_info = BASE.get(base, {"type": "", "Kb": []})
        base_type = base_info.get("type", "").lower()
        Kb_values = base_info.get("Kb", [])

        if base == "Other":
            other_base_kb_value = float(self.kb_value_other.get())
            other_base_concentration = float(self.base_concentration_other.get())
            temperature = float(self.specific_temperature_base_other.get())

            if other_base_kb_value > 1:
                hydroxide_ion_concentration = other_base_concentration

            elif 0.1 <= other_base_kb_value <= 1:
                hydroxide_ion_concentration = (-other_base_kb_value + math.sqrt(other_base_kb_value ** 2
                                                                               + 4 * other_base_kb_value * other_base_concentration)) / 2

            else:
                hydroxide_ion_concentration = math.sqrt(other_base_kb_value * other_base_concentration)

        else:
            base_concentration = float(self.specific_base_concentration.get())
            temperature = float(self.specific_temperature_base.get())

            if "very large" in Kb_values:
                hydroxide_ion_concentration = base_concentration

            else:
                if "mono" in base_type:
                    hydroxide_ion_concentration = math.sqrt(base_concentration * Kb_values[0])

                elif "di" in base_type:
                    hydroxide_ion_concentration = self.polyprotic_base_calculations(base_concentration, Kb_values)

                else:
                    hydroxide_ion_concentration = self.polyprotic_base_calculations(base_concentration, Kb_values)

        self.Kw = 1e-14 * 10 ** (0.033 * (temperature - 25))
        hydrogen_ion_concentration = self.Kw / hydroxide_ion_concentration
        pH = -math.log10(hydrogen_ion_concentration)
        pOH = -math.log10(hydroxide_ion_concentration)

        self.print_pH = pH
        self.print_hydrogen_ion = hydrogen_ion_concentration
        self.print_pOH = pOH
        self.print_hydroxide_ion = hydroxide_ion_concentration

        self.show_pH_pOH_results_values()

    def polyprotic_base_calculations(self, base_concentration, Kb_values):
        hydroxide_ions = 0.0
        Kb1 = Kb_values[0]

        if Kb1 > 1:
            hydroxide_ions += base_concentration
            B_concentration = 0

        else:
            hydroxide_ions = (-Kb1 + math.sqrt(Kb1 ** 2 + 4 * Kb1 * base_concentration)) / 2
            B_concentration = base_concentration - hydroxide_ions

        if len(Kb_values) > 1:
            Kb2 = Kb_values[1]
            hydroxide_ions_2 = (Kb2 * B_concentration) / (hydroxide_ions + Kb2)
            hydroxide_ions += hydroxide_ions_2
            base_concentration_2 = B_concentration - hydroxide_ions_2

        else:
            base_concentration_2 = 0

        if len(Kb_values) > 2:
            Kb3 = Kb_values[2]
            hydroxide_ions_3 = (Kb3 * base_concentration_2) / (hydroxide_ions + Kb3)
            hydroxide_ions += hydroxide_ions_3

        return hydroxide_ions

    def show_pH_pOH_results_values(self):
        solutions_label = tk.Label(self.window, text="Solution Properties",
                                   fg="white", bg="black", font=("Times New Roman", 12, "bold"))
        solutions_label.grid(row=2, column=1, pady=(0, 1), sticky="nw")

        pH_result_other = tk.Label(self.window, text=f"{self.print_pH:.2f}", fg="black", bg="white",
                                   font=("Times New Roman", 12, "bold"), justify="center", height=2, width=20)
        pH_result_other.grid(row=3, column=1, pady=(0, 1), sticky="nw")

        pH_result_label_other = tk.Label(self.window, text="pH value",
                                         fg="white", bg="black", font=("Times New Roman", 8, "bold"))
        pH_result_label_other.grid(row=4, column=1, pady=(0, 1), sticky="nw")

        hydrogen_concentration_result_other = tk.Label(self.window, text=f"{self.print_hydrogen_ion:.3e}",
                                                       fg="black", bg="white", font=("Times New Roman", 12, "bold"),
                                                       justify="center", height=2, width=20)
        hydrogen_concentration_result_other.grid(row=3, column=2, pady=(0, 1), padx=10, sticky="nw")
        hydrogen_concentration_result_label_other = tk.Label(self.window, text="hydrogen ion concentration (M)",
                                                             fg="white", bg="black",
                                                             font=("Times New Roman", 8, "bold"))
        hydrogen_concentration_result_label_other.grid(row=4, column=2, pady=(0, 1), sticky="nw")

        pOH_result_other = tk.Label(self.window, text=f"{self.print_pOH:.2f}", fg="black", bg="white",
                                    font=("Times New Roman", 12, "bold"), justify="center", height=2, width=20)
        pOH_result_other.grid(row=5, column=1, pady=(0, 1), sticky="nw")

        pOH_result_label_other = tk.Label(self.window, text="pOH value",
                                          fg="white", bg="black", font=("Times New Roman", 8, "bold"))
        pOH_result_label_other.grid(row=6, column=1, pady=(0, 1), sticky="nw")

        hydroxide_concentration_result_other = tk.Label(self.window, text=f"{self.print_hydroxide_ion:.3e}",
                                                        fg="black", bg="white", font=("Times New Roman", 12, "bold"),
                                                        justify="center", height=2, width=20)
        hydroxide_concentration_result_other.grid(row=5, column=2, pady=(0, 1), padx=10, sticky="nw")
        hydroxide_concentration_result_label_other = tk.Label(self.window, text="hydroxide ion concentration (M)",
                                                              fg="white", bg="black",
                                                              font=("Times New Roman", 8, "bold"))
        hydroxide_concentration_result_label_other.grid(row=6, column=2, pady=(0, 1), sticky="nw")

        self.show_pH_scale()

    def show_pH_scale(self):
        canvas_width = 380
        canvas_height = 28
        bar_width = 350
        bar_height = 6
        canvas_center = canvas_height // 2

        pH_scale = tk.Canvas(self.window, width=canvas_width, height=canvas_height, bg="white", highlightthickness=0)
        pH_scale.grid(row=7, column=1, columnspan=2)

        y1 = canvas_center - bar_height // 2
        y2 = canvas_center + bar_height // 2

        for i in range(bar_width):
            pH_value = i / bar_width * 14
            if pH_value < 7:
                frac = pH_value / 7
                r = 255
                g = int(255 * frac)
                b = 0
            else:
                frac = (pH_value - 7) / 7
                r = int(255 * (1 - frac))
                g = int(255 * (1 - 0.7 * frac))
                b = int(255 * frac)

            color = f"#{r:02x}{g:02x}{b:02x}"
            pH_scale.create_line(20 + i, y1, 20 + i, y2, fill=color)

        for i in range(15):
            x = 20 + (i / 14) * bar_width
            pH_scale.create_line(x, y1 - 3, x, y2 + 3, fill="black")
            pH_scale.create_text(x, y2 + 6, text=str(i), font=("Times New Roman", 6))

        pH = self.print_pH

        if pH < 0 or pH > 14:
            warning_label = tk.Label(self.window, text="pH out of range for display!", fg="red", bg="black")
            warning_label.grid(row=9, column=1, columnspan=2)
        elif pH < 0: pH = 0
        elif pH > 14: pH = 14
        x = 20 + (pH / 14) * bar_width
        pH_scale.create_polygon(x, 10, x - 5, 20, x + 5, 20, fill="black")

        self.show_strength_of_solution()

    def show_strength_of_solution(self):
        acid = self.acid_type.get()
        base = self.base_type.get()
        method = self.selected_option.get()

        if acid == "Other" or base == "Other":
            if method == "acid concentration":
                ka = float(self.ka_value_other.get())
                if ka > 0.1:
                    type_of_solution = tk.Label(self.window, text="Very Strong Acid",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                elif 1.0e-3 < ka <= 0.1:
                    type_of_solution = tk.Label(self.window, text="Moderately Strong Acid",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                elif 1.0e-5 < ka <= 1.0e-3:
                    type_of_solution = tk.Label(self.window, text="Weak Acid",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                elif 1.0e-15 < ka <= 1.0e-5:
                    type_of_solution = tk.Label(self.window, text="Very Weak Acid",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                else:
                    type_of_solution = tk.Label(self.window, text="Extremely Weak Acid",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
            elif method == "base concentration":
                kb = float(self.kb_value_other.get())
                if kb > 1:
                    type_of_solution = tk.Label(self.window, text="Very Strong Base",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                elif 1.0e-3 < kb <= 1:
                    type_of_solution = tk.Label(self.window, text="Strong Base",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                elif 1.0e-7 < kb <= 1.0e-3:
                    type_of_solution = tk.Label(self.window, text="Weak Base",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                else:
                    type_of_solution = tk.Label(self.window, text="Very Weak Base",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")

        else:
            if method == "acid concentration":
                acid_info = ACID.get(acid, {"type": "", "Ka": []})
                acid_type = acid_info.get("type", "").lower()
                Ka_values = acid_info.get("Ka", [])
                ka = Ka_values[0]

                if "strong" in acid_type:
                    type_of_solution = tk.Label(self.window, text="Very Strong Acid",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")

                else:
                    if ka > 0.1:
                        type_of_solution = tk.Label(self.window, text="Very Strong Acid",
                                                    fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                    justify="center")
                        type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                    elif 1.0e-3 < ka <= 0.1:
                        type_of_solution = tk.Label(self.window, text="Moderately Strong Acid",
                                                    fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                    justify="center")
                        type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                    elif 1.0e-5 < ka <= 1.0e-3:
                        type_of_solution = tk.Label(self.window, text="Weak Acid",
                                                    fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                    justify="center")
                        type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                    elif 1.0e-15 < ka <= 1.0e-5:
                        type_of_solution = tk.Label(self.window, text="Very Weak Acid",
                                                    fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                    justify="center")
                        type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                    else:
                        type_of_solution = tk.Label(self.window, text="Extremely Weak Acid",
                                                    fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                    justify="center")
                        type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")

                if "mono" in acid_type:
                    type_of_acid = tk.Label(self.window, text="Monoprotic Acid",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_acid.grid(row=8, column=2, pady=(0, 1), sticky="nw")

                elif "di" in acid_type:
                    type_of_acid = tk.Label(self.window, text="Diprotic Acid",
                                            fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                            justify="center")
                    type_of_acid.grid(row=8, column=2, pady=(0, 1), sticky="nw")

                else:
                    type_of_acid = tk.Label(self.window, text="Triprotic Acid",
                                            fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                            justify="center")
                    type_of_acid.grid(row=8, column=2, pady=(0, 1), sticky="nw")

            elif method == "base concentration":
                base_info = BASE.get(base, {"type": "", "Kb": []})
                base_type = base_info.get("type", "").lower()
                Kb_values = base_info.get("Kb", [])
                kb = Kb_values[0]

                if "strong" in base_type:
                    type_of_solution = tk.Label(self.window, text="Very Strong Acid",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")

                else:
                    if kb > 1:
                        type_of_solution = tk.Label(self.window, text="Very Strong Base",
                                                    fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                    justify="center")
                        type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                    elif 1.0e-3 < kb <= 1:
                        type_of_solution = tk.Label(self.window, text="Strong Base",
                                                    fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                    justify="center")
                        type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                    elif 1.0e-7 < kb <= 1.0e-3:
                        type_of_solution = tk.Label(self.window, text="Weak Base",
                                                    fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                    justify="center")
                        type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")
                    else:
                        type_of_solution = tk.Label(self.window, text="Very Weak Base",
                                                    fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                    justify="center")
                        type_of_solution.grid(row=8, column=1, columnspan=2, pady=(0, 1), sticky="nw")

                if "mono" in base_type:
                    type_of_acid = tk.Label(self.window, text="Monoprotic Base",
                                                fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                                justify="center")
                    type_of_acid.grid(row=8, column=2, pady=(0, 1), sticky="nw")

                elif "di" in base_type:
                    type_of_acid = tk.Label(self.window, text="Diprotic Base",
                                            fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                            justify="center")
                    type_of_acid.grid(row=8, column=2, pady=(0, 1), sticky="nw")

                else:
                    type_of_acid = tk.Label(self.window, text="Triprotic Base",
                                            fg="white", bg="black", font=("Times New Roman", 10, "bold"),
                                            justify="center")
                    type_of_acid.grid(row=8, column=2, pady=(0, 1), sticky="nw")

        self.calculation_information()

    def calculation_information(self):
        calculation = tk.Label(self.window, text="Key Formulas",
                                fg="white", bg="black", font=("Times New Roman", 14, "bold"),
                                justify="center")
        calculation.grid(row=9, column=1, columnspan=2, pady=(0, 1), sticky="nw")

        pH_calculation_description = tk.Label(self.window, text="pH = -log[H⁺]\n[H⁺] = 10⁻ᵖᴴ",
                                              fg="black", bg="white",
                                              font=("Times New Roman", 12),
                                              justify="center", width=20,
                                              relief="solid", bd=1)
        pH_calculation_description.grid(row=10, column=1, pady=(1, 0), sticky="w")

        pOH_calculation_description = tk.Label(self.window, text="pOH = -log[OH⁻]\npH + pOH = 14",
                                               fg="black", bg="white",
                                               font=("Times New Roman", 12),
                                               justify="center", width=20,
                                               relief="solid", bd=1)
        pOH_calculation_description.grid(row=10, column=2, padx=2, pady=(1, 0), sticky="w")

        self.show_Kw_information()
        kW_description = tk.Label(self.window, text=f"Kw = [H⁺][OH⁻] = {self.Kw:.3e} (at {self.Kwtemperature}°C)",
                                  fg="black", bg="white",
                                  font=("Times New Roman", 12),
                                  justify="center", width=41,
                                  relief="solid", bd=1)
        kW_description.grid(row=11, column=1, columnspan=2, pady=(0, 1), sticky="w")

    def show_Kw_information(self):
        method = self.selected_option.get()

        if method == "acid concentration":
            if self.acid_type.get() == "Other":
                self.Kwtemperature = float(self.specific_temperature_acid_other.get())
            else:
                self.Kwtemperature = float(self.specific_temperature_acid.get())
        if method == "base concentration":
            if self.base_type.get() == "Other":
                self.Kwtemperature = float(self.specific_temperature_base_other.get())
            else:
                self.Kwtemperature = float(self.specific_temperature_base.get())

    def remove_widgets_all(self):
        for widget in self.window.winfo_children():
            if widget not in (self.title, self.description, self.introduction, self.selection):
                widget.destroy()
                self.selected_option.set("Select a method")

if __name__ == "__main__":
    root = tk.Tk()
    app = pHCalculator(root)
    root.mainloop()
