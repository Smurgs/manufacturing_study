import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def hist_plot(data, title, x_label, y_label):
    plt.hist(data, int(np.sqrt(len(data))))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


def chi_square_test(observed, expected, ddof, title):
    results = stats.chisquare(observed, expected, ddof)
    result = 'confirms' if results.pvalue > 0.05 else 'rejects'
    print('Conclusion: ' + title + ' ' + result + ' the null hypothesis with a p value of ' + str(results.pvalue))


if __name__ == '__main__':

    #Content load
    inspector1_1_data = np.loadtxt('servinsp1.txt')
    inspector2_2_data = np.loadtxt('servinsp22.txt')
    inspector2_3_data = np.loadtxt('servinsp23.txt')
    workstation1_data = np.loadtxt('ws1.txt')
    workstation2_data = np.loadtxt('ws2.txt')
    workstation3_data = np.loadtxt('ws3.txt')


    #Histogram plots
    hist_plot(inspector1_1_data, 'Inspector 1 Component 1 Observed Service Times', 'Service Time (min)', 'Frequency')
    hist_plot(inspector2_2_data, 'Inspector 2 Component 2 Observed Service Times', 'Service Time (min)', 'Frequency')
    hist_plot(inspector2_3_data, 'Inspector 2 Component 3 Observed Service Times', 'Service Time (min)', 'Frequency')
    hist_plot(workstation1_data, 'Workstation 1 Observed Service Times', 'Service Time (min)', 'Frequency')
    hist_plot(workstation2_data, 'Workstation 2 Observed Service Times', 'Service Time (min)', 'Frequency')
    hist_plot(workstation3_data, 'Workstation 3 Observed Service Times', 'Service Time (min)', 'Frequency')

    # Q-Q Test
    # a = stats.expon()
    # e = stats.expon.fit(inspector1_1_data)
    # print(e)
    # stats.probplot(inspector1_1_data, dist=stats.expon_gen(), plot=plt)
    # plt.show()

    #chi-square tests
    chi_square_test((np.histogram(inspector1_1_data))[1], (np.histogram(inspector1_1_data))[1], 0, 'Inspector 1 Service times')
    chi_square_test((np.histogram(inspector2_2_data))[1], (np.histogram(inspector2_2_data))[1], 0, 'Inspector 2 with Component 2 Service times')
    chi_square_test((np.histogram(inspector2_3_data))[1], (np.histogram(inspector2_3_data))[1], 0, 'Inspector 2 with Component 3 Service times')
    chi_square_test((np.histogram(workstation1_data))[1], (np.histogram(workstation1_data))[1], 0, 'Workstation 1 Service times')
    chi_square_test((np.histogram(workstation2_data))[1], (np.histogram(workstation2_data))[1], 0, 'Workstation 2 Service times')
    chi_square_test((np.histogram(workstation3_data))[1], (np.histogram(workstation3_data))[1], 0, 'Workstation 3 Service times')