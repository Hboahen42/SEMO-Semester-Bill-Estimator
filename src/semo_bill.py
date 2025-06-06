# Import the Dear PyGui module using an alias
import dearpygui.dearpygui as dpg
import os

# Define the function that performs the semester bill calculation
def calculate_bill():
    try:
        # Collect and convert input values from UI widgets
        credit_hours = int(dpg.get_value("credit_hours"))              # Total credit hours
        cs_hours = int(dpg.get_value("cs_hours"))                      # Credit hours specific to CS/IS/CY
        classes = int(dpg.get_value("num_classes"))                    # Number of enrolled classes
        scholarships = float(dpg.get_value("scholarships"))           # Scholarship amount in dollars
        housing = float(dpg.get_value("housing_option"))              # Housing cost selected
        meal = float(dpg.get_value("meal_option"))                    # Meal plan cost selected
        ipp_fee = 30.00 if dpg.get_value("use_ipp") else 0.00         # Installment Payment Plan fee (optional)
        level = dpg.get_value("level_selector")                       # Student level (affects tuition rates)

        # Validate that CS credit hours do not exceed total credit hours
        if cs_hours > credit_hours:
            raise ValueError("CS/IS/CY credit hours cannot exceed total credit hours.")

        # Dictionary mapping each student level to their rates:
        # (tuition per credit hour, general fee per credit hour, CS/IS/CY program fee per credit hour)
        rates = {
            "Undergrad (Domestic)": (285.29, 44.80, 40.00),
            "Undergrad (Non-Domestic)": (526.79, 44.80, 40.00),
            "Grad (Domestic)": (382.94, 44.80, 0.00),
            "Grad (Non-Domestic)": (690.59, 44.80, 0.00)
        }

        # Extract relevant rate values based on selected student level
        tuition, general_fee, program_fee = rates[level]

        # Calculate cost breakdown
        tuition_total = credit_hours * tuition
        fee_total = credit_hours * general_fee
        program_fee_total = cs_hours * program_fee
        textbook_total = classes * 36.49                              # $36.49 per course for textbooks

        # Add all costs together (before subtracting scholarships)
        total_before = (
            tuition_total +
            fee_total +
            program_fee_total +
            housing +
            meal +
            textbook_total +
            ipp_fee
        )

        # Subtract scholarships to get the final bill amount
        final_total = total_before - scholarships

        # Format result string for display
        result = f"""
    Tuition: ${tuition_total:,.2f}
    General Fees: ${fee_total:,.2f}
    Program Fee ({cs_hours} hrs): ${program_fee_total:,.2f}
    Textbooks ({classes} classes): ${textbook_total:,.2f}
    IPP Fee: ${ipp_fee:,.2f}
    Housing: ${housing:,.2f}
    Meal Plan: ${meal:,.2f}

    ###############################
    Total Before Scholarships: ${total_before:,.2f}
    Scholarships: -${scholarships:,.2f}
    Final Bill: ${final_total:,.2f}
    ################################
"""
        # Output the result in the text field
        dpg.set_value("result_output", result)

    except Exception as e:
        # Display any errors that occur during processing
        dpg.set_value("result_output", f"❌ Error: {str(e)}")

# ----------- GUI Setup -----------

# Start Dear PyGui context
dpg.create_context()

# Custom dark theme for the app
with dpg.theme(tag="dark_theme"):
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 25, 35), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (240, 240, 240), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 35, 50), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 100, 200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 130, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (40, 90, 190), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

# Load and register custom font
with dpg.font_registry():
    font_path = os.path.join(os.path.dirname(__file__), "..", "fonts", "SF-Pro-Display-Regular.otf")
    default_font = dpg.add_font(font_path, 20)

# Main window layout and input fields
with dpg.window(label="SEMO Semester Bill Calculator", tag="main_window", width=700, height=750):
    dpg.bind_item_theme("main_window", "dark_theme")
    dpg.bind_font(default_font)

    # Student level selection
    with dpg.group():
        dpg.add_text("Student Level")
        dpg.add_combo(items=[
            "Undergrad (Domestic)",
            "Undergrad (Non-Domestic)",
            "Grad (Domestic)",
            "Grad (Non-Domestic)"
        ], default_value="Undergrad (Domestic)", tag="level_selector", width=368)

    # Credit hour inputs
    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_text("Total Credit Hours")
            dpg.add_spacer(width=48)
            dpg.add_text("CS/IS/CY Credit Hours")
        with dpg.group(horizontal=True):
            dpg.add_input_int(tag="credit_hours", min_value=0, step=0, width=180)
            dpg.add_input_int(tag="cs_hours", min_value=0, step=0, width=180)

    # Course count and scholarships
    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_text("Number of Classes")
            dpg.add_spacer(width=38)
            dpg.add_text("Scholarships ($)")
        with dpg.group(horizontal=True):
            dpg.add_input_int(tag="num_classes", min_value=0, step=0, width=180)
            dpg.add_input_float(tag="scholarships", min_value=0.0, format="%.2f", step=0, width=180)

    # Housing and meal plan options
    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_text("Housing Option")
            dpg.add_spacer(width=65)
            dpg.add_text("Meal Plan Option")
        with dpg.group(horizontal=True):
            dpg.add_combo(items=["3925.00", "3100.00", "0.00"], default_value="3100.00", tag="housing_option", width=180)
            dpg.add_combo(items=["1650.00", "1850.00", "0.00"], default_value="1650.00", tag="meal_option", width=180)

    # IPP option + Calculate button
    dpg.add_spacer(height=10)
    dpg.add_checkbox(label="Use Installment Payment Plan (IPP)", tag="use_ipp")
    dpg.add_spacer(height=10)
    dpg.add_button(label="Calculate Bill", callback=calculate_bill, width=368)

    # Result output field (read-only)
    dpg.add_spacer(height=10)
    dpg.add_input_text(tag="result_output", multiline=True, readonly=True, width=368, height=300)

# ----------- Launch the App -----------

dpg.create_viewport(title='SEMO Semester Bill Calculator', width=400, height=700, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()
