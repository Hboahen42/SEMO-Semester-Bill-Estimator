import dearpygui.dearpygui as dpg

def calculate_bill():
    try:
        credit_hours = int(dpg.get_value("credit_hours"))
        cs_hours = int(dpg.get_value("cs_hours"))
        courses = int(dpg.get_value("num_courses"))
        scholarships = float(dpg.get_value("scholarships"))
        housing = float(dpg.get_value("housing_option"))
        meal = float(dpg.get_value("meal_option"))
        ipp_fee = 30.00 if dpg.get_value("use_ipp") else 0.00
        level = dpg.get_value("level_selector")

        if cs_hours > credit_hours:
            raise ValueError("CS/IS/CY credit hours cannot exceed total credit hours.")

        rates = {
            "Undergrad (Domestic)": (285.29, 44.80, 40.00),
            "Undergrad (Non-Domestic)": (526.79, 44.80, 40.00),
            "Grad (Domestic)": (382.94, 44.80, 0.00),
            "Grad (Non-Domestic)": (690.59, 44.80, 0.00)
        }

        tuition, general_fee, program_fee = rates[level]

        tuition_total = credit_hours * tuition
        fee_total = credit_hours * general_fee
        program_fee_total = cs_hours * program_fee
        textbook_total = courses * 36.49

        total_before = tuition_total + fee_total + program_fee_total + housing + meal + textbook_total + ipp_fee
        final_total = total_before - scholarships

        result = f"""
    Tuition: ${tuition_total:,.2f}
    General Fees: ${fee_total:,.2f}
    Program Fee ({cs_hours} hrs): ${program_fee_total:,.2f}
    Textbooks ({courses} courses): ${textbook_total:,.2f}
    IPP Fee: ${ipp_fee:,.2f}
    Housing: ${housing:,.2f}
    Meal Plan: ${meal:,.2f}

    ###############################
    Total Before Scholarships: ${total_before:,.2f}
    Scholarships: -${scholarships:,.2f}
    Final Bill: ${final_total:,.2f}
    ################################
"""
        dpg.set_value("result_output", result)

    except Exception as e:
        dpg.set_value("result_output", f"❌ Error: {str(e)}")

# Initialize DPG
dpg.create_context()

with dpg.theme(tag="dark_theme"):
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 25, 35), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (240, 240, 240), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 35, 50), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 100, 200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 130, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (40, 90, 190), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font("fonts\\SF-Pro-Display-Regular.otf", 20)

# Main layout
with dpg.window(label="SEMO Semester Bill Calculator", tag="main_window", width=700, height=750):
    dpg.bind_item_theme("main_window", "dark_theme")
    dpg.bind_font(default_font)

    with dpg.group():
        dpg.add_text("Student Level")
        dpg.add_combo(items=[
            "Undergrad (Domestic)",
            "Undergrad (Non-Domestic)",
            "Grad (Domestic)",
            "Grad (Non-Domestic)"
        ], default_value="Undergrad (Domestic)", tag="level_selector", width=368)

    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_text("Total Credit Hours")
            dpg.add_spacer(width=48)
            dpg.add_text("CS/IS/CY Credit Hours")
        with dpg.group(horizontal=True):
            dpg.add_input_int(tag="credit_hours", min_value=0, step=0, width=180)
            dpg.add_input_int(tag="cs_hours", min_value=0, step=0, width=180)

    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_text("Number of Courses")
            dpg.add_spacer(width=38)
            dpg.add_text("Scholarships ($)")
        with dpg.group(horizontal=True):
            dpg.add_input_int(tag="num_courses", min_value=0, step=0, width=180)
            dpg.add_input_float(tag="scholarships", min_value=0.0, format="%.2f", step=0, width=180)

    with dpg.group():
        with dpg.group(horizontal=True):
            dpg.add_text("Housing Option")
            dpg.add_spacer(width=65)
            dpg.add_text("Meal Plan Option")
        with dpg.group(horizontal=True):
            dpg.add_combo(items=["3925.00", "3100.00", "0.00"], default_value="3100.00", tag="housing_option", width=180)
            dpg.add_combo(items=["1650.00", "1850.00", "0.00"], default_value="1650.00", tag="meal_option", width=180)

    dpg.add_spacer(height=10)
    dpg.add_checkbox(label="Use Installment Payment Plan (IPP)", tag="use_ipp")
    dpg.add_spacer(height=10)
    dpg.add_button(label="Calculate Bill", callback=calculate_bill, width=368)
    dpg.add_spacer(height=10)
    dpg.add_input_text(tag="result_output", multiline=True, readonly=True, width=368, height=300)


# Final setup
dpg.create_viewport(title='SEMO Semester Bill Calculator', width=400, height=700, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()
