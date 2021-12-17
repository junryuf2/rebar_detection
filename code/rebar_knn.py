import matplotlib.pyplot as plt


# bins = [10,20,30,40]
values = [11,13,25,24,36,34,33,21,13,15,17]
# n, bin_returned, patches = plt.hist(values, 4, density=True, facecolor='g')
#
# print(n)
# print(bin_returned)
# print(patches)
#
# plt.show();

def find_peak(v, step):
    #initialize all parameters
    t = 0
    peaks_idx = []
    #check if the length of the step is correct
    if (step > len(v)/2):
        raise Exception("value must be less than half of the length of the inputted histogram")

    #loop through all the peak density values
    for i in range(step,len(v)-step):
        #using a helper function, to loop through the s amount of steps required for the condition of step inputted
        for s in range(1, step+1):
            t += peak_helper(v, i ,s)
        if (t == 0):
            peaks_idx.append(i)
        t = 0

    return peaks_idx

#helper function in finding the peak based on the step value
def peak_helper(v, i, s):
    if((v[i] > v[i-s]) and (v[i] > v[i+s])):
        return 0
    else:
        return 1

print("opening peak finder knn...")
