import matplotlib.pyplot as plt
import numpy as np
import argparse, pathlib, sys
import pandas as pd

def show_plot(csv_file, plot_type):
    times, x_coords, y_coords = read_csv(csv_file)
    if plot_type == 'x':
        plot_generic(times, x_coords, 'Time (seconds)', 'X Coordinate', 
                     'X Coordinate vs Time')
    elif plot_type == 'y':
        plot_generic(times, y_coords, 'Time (seconds)', 'Y Coordinate', 
                     'Y Coordinate vs Time')
    elif plot_type == 'x_velocity':
        x_velocity, times = calculate_velocity(x_coords, times)
        plot_generic(times, x_velocity, 'Time (seconds)', 
                        'X Velocity (m/s)', 'X Velocity vs Time')
    elif plot_type == 'y_velocity':
        y_velocity, times = calculate_velocity(y_coords, times)
        plot_generic(times, y_velocity, 'Time (seconds)', 
                     'Y Velocity (m/s)', 'Y Velocity vs Time')
    elif plot_type == 'x_acceleration':
        x_acceleration, times = calculate_acceleration(x_coords, times)
        plot_generic(times, x_acceleration, 'Time (seconds)', 
                        'X Acceleration (m$^2$/s)', 'X Acceleration vs Time')
    elif plot_type == 'y_acceleration':
        y_acceleration, times = calculate_acceleration(y_coords, times)
        plot_generic(times, y_acceleration, 'Time (seconds)', 
                        'Y Velocity (m$^2$/s)', 'Y Acceleration vs Time')
    else:
        print(f"Invalid plot type")

def read_csv(csv_file):
    df = pd.read_csv(csv_file)
    print(df)
    return df['Time'].values, df['x'].values, df['y'].values

def plot_generic(x_data, y_data, x_label, y_label, title):
    plt.plot(x_data, y_data, 'o')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()

def calculate_velocity(coords, times):
    coord_series = pd.Series(coords)
    time_series = pd.Series(times)
    delta_coord = coord_series.diff().iloc[1:]
    delta_time = time_series.diff().iloc[1:]
    velocities = delta_coord / delta_time
    aligned_times = time_series.iloc[1:]
    return velocities.values, aligned_times.values

def calculate_acceleration(coords, times):
    coord_series = pd.Series(coords)
    time_series = pd.Series(times)
    velocity, time = calculate_velocity(coord_series, time_series)
    delta_velocity = pd.Series(velocity).diff().iloc[1:]
    delta_time = pd.Series(time).diff().iloc[1:]
    accelerations = delta_velocity / delta_time
    aligned_times = time_series.iloc[2:]
    return accelerations.values, aligned_times.values

def init_argparse() -> argparse.ArgumentParser:
    graph_choices = ["x", "y", "x_velocity", "y_velocity", "x_acceleration", "y_acceleration"]
    parser = argparse.ArgumentParser(prog=sys.argv[0],
    usage=f"%(prog)s [-h] [-v] -c CSV_FILE -t | --type {graph_choices}", 
    add_help=False, description="Generates a range of different graphs based on CSV file provided")

    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--infile", action="store", type=pathlib.Path,
                          required=True, help = "Full path to the input CSV file")
    required.add_argument("-t", "--type", type=str, choices=graph_choices, 
                          required=True, help = "Type of plot to generate")

    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("-h", "--help", action="help", 
                          help="show this help message and exit")
    optional.add_argument("-v", "--version", action="version", 
                        version=f"{parser.prog} version 1.0.0")
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    try:
        show_plot(args.infile, args.type)
        exit(0)
    except Exception as err:
        print(err, file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()