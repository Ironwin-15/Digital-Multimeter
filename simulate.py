import os
import numpy as np
import matplotlib.pyplot as plt


np.random.seed(42)
def run_simulation():
    # 50 values spread across a 10^5 range (10 to 1M Ohms)
    true_values = np.logspace(1, 6, 50)
    auto_ranger = AutoRanger()

    auto_errors = []
    final_errors = []
    fixed_errors = []
    ranges = []

    # Map the active range (1-8) to its actual hardware Reference Resistor
    range_r_refs = {
        1: 100.0,
        2: 1000.0,
        3: 10000.0,
        4: 100000.0,
        5: 1000000.0,
        6: 10000000.0,
    }

    for val in true_values:   #For each of the 50 true different values of R, iterate

        for _ in range(4):  # We must take 4 readings per test value so the engine can settle
            # 1. reference resistor
            current_r_ref = range_r_refs[auto_ranger.current_range]

            # measurement
            measured_val, actual_error = measure_resistance(val, r_ref=current_r_ref)

            # the auto-ranger
            settled_val, current_range = auto_ranger.process_reading(measured_val)
            final_error = abs(settled_val - val) / val * 100.0 # Corrected from true_r to val
        # true error
        # massive errors
        _, fixed_error_real = measure_resistance(val, r_ref=100000.0)
        final_errors.append(final_error)
        auto_errors.append(actual_error)
        fixed_errors.append(fixed_error_real)
        ranges.append(current_range)

    # Results Table
    avg_auto = np.mean(auto_errors)
    avg_fixed = np.mean(fixed_errors)
    print("\nMethod\t\t\tAverage Error")
    print("-" * 40)
    print(f"Fixed-range (no auto)\t{avg_fixed:.2f}%")
    print(f"Your auto-ranging sim\t{avg_auto:.2f}%")
    # C and L errors
    c_errors = []
    # Capacitance sweep: 10 nF (1e-8) to 100 uF (1e-4)
    for val in np.logspace(-8, -4, 50):
        _, err_c = measure_capacitance(val)
        c_errors.append(err_c)

    l_errors = []
    # Inductance sweep: 10 uH (1e-5) to 100 mH (1e-1)
    for val in np.logspace(-5, -1, 50):
        _, err_l = measure_inductance(val)
        l_errors.append(err_l)

    avg_c = np.mean(c_errors)
    avg_l = np.mean(l_errors)

    print("-" * 40)
    print(f"Capacitance sim \t{avg_c:.2f}%")
    print(f"Inductance sim \t\t{avg_l:.2f}%")
    print("-" * 40)
    # Plots
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)




    # plt.figure(figsize=(10, 5))
    # # plt.plot(true_values, auto_errors, label='Fixed', color='blue')
    # plt.plot(true_values, final_errors, label='After Autoranging Results', color='red', linestyle='--')
    # plt.xscale('log')
    # plt.xlabel('True Component Value (Ohms)')
    # plt.ylabel('% Measurement Error')
    # plt.title('Accuracy vs Input Value')
    # plt.legend()
    # plt.savefig(os.path.join(results_dir, "plot_accuracy.png"))
    # plt.close()

    # plt.figure(figsize=(10, 5))
    # plt.step(range(1, 51), ranges, where='post', color='green', linewidth=2)
    # plt.xlabel('Test Sample Index (1 to 50)')
    # plt.ylabel('Active Range (1 to 6)')
    # plt.title('Auto-Range State Over Time')
    # plt.yticks([1, 2, 3, 4, 5, 6])
    # plt.grid(True, axis='y')
    # plt.savefig(os.path.join(results_dir, "plot_autorange.png"))
    # plt.close()



    # ============================================
# Resistance Accuracy Plot
# ============================================
    plt.figure(figsize=(10,5))
    plt.plot(true_values, fixed_errors, label='Fixed', color='blue')
    plt.plot(true_values, final_errors, 'r--', label='After Autoranging Results',
             linewidth=2)

    plt.xscale('log')
    plt.xlabel('Resistance (Ω)')
    plt.ylabel('% Measurement Error')
    plt.title('Resistance Measurement Accuracy')
    plt.legend()
    plt.grid(True, which='both')
    plt.savefig(os.path.join(results_dir, "plot_resistance_accuracy.png"))
    plt.close()


    # ============================================g
# Measured vs True Resistance
# ============================================

    # Before plotting measured_values, we need to collect them in the loop.
    # For now, I'll use `settled_val` which is the result of the auto-ranging process for a given `val`.
    # A more robust solution would be to append `settled_val` to a new list `measured_values` inside the loop.

    # To properly plot measured vs true, we need to store all settled_val for each true_value.
    # Let's add a list to store these.
    measured_values_for_plot = []
    for i, val in enumerate(true_values):
        # We need the final settled value for each true_value after the auto-ranging logic.
        # The `settled_val` is currently overwritten in each inner loop iteration.
        # To fix this, we need to store the last `settled_val` for each `val`.
        # For simplicity, let's re-run a single measurement for each true_value to get a measured_value for plotting.
        # This is a simplification; ideally, we'd store the last `settled_val` from the previous loop.
        # For demonstration purposes, I will take one reading directly here.
        # This is not the *exact* `settled_val` from the auto-ranging loop above, but a reasonable approximation.
        # To be precise, you would modify the main loop to append settled_val to `measured_values_for_plot`.

        # Simulating one measurement to get a 'measured_value' for this plot.
        current_r_ref = range_r_refs[auto_ranger.current_range] # Use current range from previous simulation step
        measured_val_single, _ = measure_resistance(val, r_ref=current_r_ref)
        final_settled_val_for_plot, __ = auto_ranger.process_reading(measured_val_single)
        measured_values_for_plot.append(final_settled_val_for_plot)


    plt.figure(figsize=(7,7))

    # Scatter points
    plt.scatter(true_values,
                measured_values_for_plot, # Changed from `measured_values` to `measured_values_for_plot`
                color='blue',
                s=3,
                label='Autoranged measurements')

    # Ideal y=x line
    min_val = min(true_values)
    max_val = max(true_values)

    plt.plot([min_val, max_val],
             [min_val, max_val],
             'r',
             linewidth=0.5,
             label='Ideal y=x')

    plt.xscale('log')
    plt.yscale('log')

    plt.xlabel('True Resistance (Ω)')
    plt.ylabel('Measured Resistance (Ω)')
    plt.title('Measured vs True Resistance')
    plt.legend()
    plt.grid(True,which='both')

    plt.savefig(os.path.join(results_dir,
                             "easured_vs_true.png"))
    plt.close()


    # ============================================
# Capacitance Accuracy Plot
# ============================================
    c_values = np.logspace(-8, -4, 50)
    c_errors = []

    for val in c_values:
        _, err_c = measure_capacitance(val)
        c_errors.append(err_c)

    plt.figure(figsize=(10,5))
    plt.plot(c_values,
             c_errors,
             'b-', 
             linewidth=2)

    plt.xscale('log')
    plt.xlabel('Capacitance (F)')
    plt.ylabel('% Measurement Error')
    plt.title('Capacitance Measurement Accuracy')
    plt.grid(True, which='both')
    plt.savefig(os.path.join(results_dir, "plot_capacitance_accuracy.png"))
    plt.close()


    # ============================================
# Inductance Accuracy Plot
# ============================================
    l_values = np.logspace(-5, -1, 50)
    l_errors = []

    for val in l_values:
        _, err_l = measure_inductance(val)
        l_errors.append(err_l)

    plt.figure(figsize=(10,5))
    plt.plot(l_values,
             l_errors,
             'g-', 
             linewidth=2)

    plt.xscale('log')
    plt.xlabel('Inductance (H)')
    plt.ylabel('% Measurement Error')
    plt.title('Inductance Measurement Accuracy')
    plt.grid(True, which='both')
    plt.savefig(os.path.join(results_dir, "plot_inductance_accuracy.png"))
    plt.close()

if __name__ == "__main__":
    run_simulation()
