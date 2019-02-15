import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def hist_plot(data, title, x_label, y_label):
    plt.hist(data, int(np.sqrt(len(data))))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


if __name__ == '__main__':

    inspector1_1_data = np.loadtxt('servinsp1.txt')
    inspector2_2_data = np.loadtxt('servinsp22.txt')
    inspector2_3_data = np.loadtxt('servinsp23.txt')
    workstation1_data = np.loadtxt('ws1.txt')
    workstation2_data = np.loadtxt('ws2.txt')
    workstation3_data = np.loadtxt('ws3.txt')

    a = stats.expon()
    e = stats.expon.fit(inspector1_1_data)
    print(e)
    stats.probplot(inspector1_1_data, dist=stats.expon_gen(), plot=plt)
    plt.show()

    # hist_plot(inspector1_1_data, 'Inspector 1 Component 1 Observed Service Times', 'Service Time (min)', 'Frequency')
    # hist_plot(inspector2_2_data, 'Inspector 2 Component 2 Observed Service Times', 'Service Time (min)', 'Frequency')
    # hist_plot(inspector2_3_data, 'Inspector 2 Component 3 Observed Service Times', 'Service Time (min)', 'Frequency')
    # hist_plot(workstation1_data, 'Workstation 1 Observed Service Times', 'Service Time (min)', 'Frequency')
    # hist_plot(workstation2_data, 'Workstation 2 Observed Service Times', 'Service Time (min)', 'Frequency')
    # hist_plot(workstation3_data, 'Workstation 3 Observed Service Times', 'Service Time (min)', 'Frequency')

