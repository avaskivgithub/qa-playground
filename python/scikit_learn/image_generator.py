import numpy as np
import matplotlib.pyplot as plt
import os

def generate_test_image(x = np.arange(-10, 11, 1),
                        f = lambda x: x**3 / np.exp(x), 
                        file_path = os.path.join(os.getcwd(), 'example_plot.png')):

    # Calculate y values
    y = f(x)

    # Add a few outliers
    outliers_x = np.array([-10, -5, 0, 5, 10])
    outliers_y = np.array([10, -10, 15, -15, 20])

    # Combine original points and outliers
    x_combined = np.concatenate((x, outliers_x))
    y_combined = np.concatenate((y, outliers_y))

    # Create the scatter plot
    plt.scatter(x_combined, y_combined, color='blue', label='Data Points')
    plt.scatter(outliers_x, outliers_y, color='red', label='Outliers')

    # Add labels and title
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Scatter plot with Outliers')
    plt.legend()

    # Show the plot
    # plt.show()
    print(file_path)
    plt.savefig(file_path, format='png')

if __name__ == '__main__':
    generate_test_image()