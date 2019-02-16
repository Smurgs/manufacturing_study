import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def hist_plot(data, filename):
    plt.hist(data, int(np.sqrt(len(data))))
    plt.xlabel('Service Time (min)')
    plt.ylabel('Frequency')
    plt.title(filename[:-4] + ' Frequency Distribution')
    plt.show()


def find_exp_params(data):
    loc, scale = stats.expon.fit(data)
    print('Loc: %.2f \tScale:%.2f' % (loc, scale))
    return loc, scale


def qqplot(data, dist, filename):
    stats.probplot(data, dist=dist, plot=plt)
    plt.title(filename[:-4] + ' Q-Q Plot')
    plt.show()


def chi_square_test(data, dist):
    # Get frequency and bin edges for observed data
    frequency, edges = np.histogram(data, int(np.sqrt(len(data))))

    # Determine expected frequency from exp distribution
    size = sum(frequency)
    expected_frequency = [(dist.cdf(edges[i + 1]) - dist.cdf(edges[i])) * size for i in range(len(edges)-1)]

    # Group bins together if observed or expected frequency < 5 to conform with chi-square requirements
    frequency = list(frequency)
    for i in reversed(range(len(frequency))):
        if expected_frequency[i] < 5 or frequency[i] < 5:
            expected_frequency[i - 1] += expected_frequency[i]
            expected_frequency.pop(i)
            frequency[i - 1] += frequency[i]
            frequency.pop(i)

    # Perform chi-square test and print results
    test_statistic, p_value = stats.chisquare(frequency, expected_frequency, ddof=2)
    print('Test statistic: %f \tP-value: %f' % (test_statistic, p_value))
    result = 'confirms' if p_value > 0.05 else 'rejects'
    print('Conclusion: ' + result + ' the null hypothesis with a p value of ' + str(p_value))


if __name__ == '__main__':

    input_files = ['servinsp1.txt', 'servinsp22.txt', 'servinsp23.txt', 'ws1.txt', 'ws2.txt', 'ws3.txt']
    for filename in input_files:

        # Load data
        print('\nLoading file: %s %s' % (filename, '-'*30))
        data = np.loadtxt(filename)

        # Plot histogram
        hist_plot(data, filename)

        # Fit exponential distribution to data to find parameters
        loc, scale = find_exp_params(data)

        # Print qqplot
        exp_dist = stats.expon(loc=loc, scale=scale)
        qqplot(data, exp_dist, filename)

        # Chi-square tests
        chi_square_test(data, exp_dist)
