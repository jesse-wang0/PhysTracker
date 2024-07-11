import matplotlib.pyplot as plt
import numpy as np
import csv, argparse, pathlib, sys

def read_csv(csv_file, times, x_coords, y_coords):
    with open(csv_file, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            times.append(float(row[0]))
            x_coords.append(float(row[1]))
            y_coords.append(float(row[2]))

def show_plot(csv_file, plot_type):
    x_coords = []
    y_coords = []
    times = []
    read_csv(csv_file, times, x_coords, y_coords)
    np_x_coords = np.array(x_coords)
    np_y_coords = np.array(y_coords)
    np_times = np.array(times)
    if plot_type == 'x':
        plot_generic(np_times, np_x_coords, 'Time (seconds)', 'X Coordinate', 
                     'X Coordinate vs Time')
    elif plot_type == 'y':
        plot_generic(np_times, np_y_coords, 'Time (seconds)', 'Y Coordinate', 
                     'Y Coordinate vs Time')
    elif plot_type == 'x_velocity':
        x_velocity = calculate_velocity(x_coords, times)
        plot_generic(np_times[1:], x_velocity, 'Time (seconds)', 
                        'X Velocity (m/s)', 'X Velocity vs Time')
    elif plot_type == 'y_velocity':
        y_velocity = calculate_velocity(y_coords, times)
        plot_generic(np_times[1:], y_velocity, 'Time (seconds)', 
                        'Y Velocity (m/s)', 'Y Velocity vs Time')
    elif plot_type == 'x_acceleration':
        x_acceleration = calculate_acceleration(x_coords, times[1:])
        plot_generic(np_times[2:], x_acceleration, 'Time (seconds)', 
                        'X Acceleration (m$^2$/s)', 'X Acceleration vs Time')
    elif plot_type == 'y_acceleration':
        y_acceleration = calculate_acceleration(y_coords, times[1:])
        plot_generic(np_times[2:], y_acceleration, 'Time (seconds)', 
                        'Y Velocity (m$^2$/s)', 'Y Acceleration vs Time')
    else:
        print(f"Invalid plot type")
    

def plot_generic(x_data, y_data, x_label, y_label, title):
    plt.plot(x_data, y_data, 'o')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()

def calculate_velocity(coord_list, time_list):
    velocities = np.zeros(len(coord_list) - 1)
    frame_duration = time_list[1] - time_list[0]
    for i in range(len(coord_list) - 1):
        velocity = (coord_list[i+1] - coord_list[i]) / frame_duration 
        velocities[i] = velocity
    return velocities

def calculate_acceleration(coord_list, time_list):
    velocity = calculate_velocity(coord_list, time_list)
    times = np.array(time_list)
    delta_v = np.diff(velocity)
    delta_t = np.diff(times)
    return delta_v / delta_t

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