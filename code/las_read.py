import matplotlib.pyplot as plt
from numpy.core.records import array

from rebar_knn import find_peak, peak_helper



##=================function declarations========================
#this function returns the 3D local coordinate of the point of a given line of data from the txt file extracted
def point(line):
    data = line.split(" ")
    coord = [float(data[0]),float(data[1]),float(data[2])]
    return coord

def print_hist_graph(x,y,z, bin):
    fig, (xplot, yplot, zplot) = plt.subplots(nrows=1, ncols=3)
    xplot.hist(x,bins=bin, density=True, facecolor='r')
    yplot.hist(y,bins=bin, density=True, facecolor='g')
    zplot.hist(z,bins=bin, density=True, facecolor='b')

    xptitle = "x projection with bin = "
    yptitle = "y projection with bin = "
    zptitle = "z projection with bin = "


    xplot.set_title(xptitle + str(bin))
    xplot.set_xlabel("arbitrary unit length")
    xplot.set_ylabel("frequency of points")

    yplot.set_title(yptitle + str(bin))
    yplot.set_xlabel("arbitrary unit length")
    yplot.set_ylabel("frequency of points")

    zplot.set_title(zptitle + str(bin))
    zplot.set_xlabel("arbitrary unit length")
    zplot.set_ylabel("frequency of points")
    plt.show()

def mean(array):
    sum = 0
    for i in array:
        sum += i

    return sum/(len(array))


def return_peaks_detected(n_axis, bin_axis, steps):
    print(len(n_axis))
    peak_index = find_peak(n_axis, steps)
    peak_coord = []
    print(peak_index)
    for i in peak_index:
        peak_coord.append(bin_axis[i])
        print(bin_axis[i])
    return peak_coord


def analyze_gap(peak_coordinates):
    gap = []
    for i in range(1,len(peak_coordinates)):
        gap.append(peak_coordinates[i] - peak_coordinates[i-1]);
        print(peak_coordinates[i] - peak_coordinates[i-1])
    return gap

def mark_peaks(peak_coordinates_x,peak_coordinates_y,peak_coordinates_z,file, original_file):
    #change access mode to 'a' to append the newest peak points
    new_txt_file = open(file, 'a')
    new_txt_file.truncate(0)
    #copy original las coordinates in to the new new_txt_file
    original = open(original_file, "r")
    read_rebars_data = original.read()
    each_line = read_rebars_data.split("\n")
    print("copying original file")
    for i in range(0,len(each_line)):
        new_txt_file.write(each_line[i])
        new_txt_file.write("\n")


    print("printing appending lines")
    #iterate over all of the peak coordinates at a given axis constraint
    for i in peak_coordinates_x:
        returning_line = ""
        returning_line += str(i)
        returning_line += " "
        returning_line += str(mean_y)
        returning_line += " "
        returning_line += str(mean_z)
        returning_line += " 255 0 0\n"

        new_txt_file.write(returning_line)

    for i in peak_coordinates_y:
        returning_line = ""
        returning_line += str(mean_x)
        returning_line += " "
        returning_line += str(i)
        returning_line += " "
        returning_line += str(mean_z)
        returning_line += " 0 255 0\n"

        new_txt_file.write(returning_line)

    for i in peak_coordinates_z:
        returning_line = ""
        returning_line += str(mean_x)
        returning_line += " "
        returning_line += str(mean_y)
        returning_line += " "
        returning_line += str(i)
        returning_line += " 0 0 255\n"

        new_txt_file.write(returning_line)


##peak coordinates are the detected peaks returned by the function "return_peaks_detected", input low and high constraint for gap
def graph_gap(peak_coordinates, low_constraint, high_constraint):
    default_coord = [0] * len(peak_coordinates)
    cumulative = 0
    annotation_coord = []
    annotation_y = []

    print("\nprinting graph gaps")
    gap = []

    for i in range(1,len(peak_coordinates)):
        g = peak_coordinates[i] - peak_coordinates[i-1]
        gap.append(g)
        if (peak_coordinates[i] < peak_coordinates[i-1]):
            annotation_coord.append(peak_coordinates[i] + abs(g)//4)
        else:
            annotation_coord.append(peak_coordinates[i-1] + abs(g)/4)

        annotation_y.append(0)


    
    #     cumulative += array_of_gaps[i]
    #     gap_coord.append(cumulative)
    #     print(gap_coord[i])
    
    # fig, (gapplot) = plt.subplots(nrows=1, ncols=1)
    # gapplot = plt.plot(annotation_coord, annotation_y, "o")

    fig = plt.subplots(nrows=1, ncols=1)
    gapplot = plt.plot(peak_coordinates, default_coord, "o:b")

    ##annotating the value of the gap in between rebar peaks detected
    for i in range(0, len(annotation_coord)):
        ##default annotation color is black
        c = 'black'
        if ((gap[i] < low_constraint) or (gap[i] > high_constraint)):
            c = 'red'
        plt.annotate(round(gap[i],3), (annotation_coord[i], annotation_y[i]),fontsize=5, color=c)

    # plt.annotate((-28,0),(-26,0),arrowprops={"arrowstyle":"<->"})
    # annot = plt.plot(annotation_coord, annotation_y, "o")


#============================command lines=================================

bins = int(input("PLEASE ENTER THE BIN NUMBER FOR THE HISTOGRAM: "))

##Extracting the file and saving to extracted_rebars_txt
input_file = str(input("INPUT THE FULL PATH OF YOUR FILE: "))
extracted_rebars_txt = open(input_file, "r")

read_rebars_data = extracted_rebars_txt.read()

each_line = read_rebars_data.split("\n")
count_statement = "the loaded amount of points are " + str(len(each_line))
print(count_statement)

xaxis = []
yaxis = []
zaxis = []

print("----------test printing some values----------")
print(type(point(each_line[2])[0]))
print(type(len(each_line)))

#appends all the data based on axis with fixed order
#appends everything from line 1 to the 2nd last line which has all the point cloud data
for i in range(1,len(each_line)-1):
    xaxis.append(point(each_line[i])[0])
    yaxis.append(point(each_line[i])[1])
    zaxis.append(point(each_line[i])[2])

# fig, ((xplot, yplot, zplot)) = plt.subplots(nrows=1, ncols=3)
# plt.show()

xplot = plt.hist(xaxis,bins, density=True, facecolor='r')
yplot = plt.hist(yaxis,bins, density=True, facecolor='g')
zplot = plt.hist(zaxis,bins, density=True, facecolor='b')

n_x, bin_returned_x, patches_x = xplot
n_y, bin_returned_y, patches_y = yplot
n_z, bin_returned_z, patches_z = zplot

mean_x = mean(bin_returned_x)
mean_y = mean(bin_returned_y)
mean_z = mean(bin_returned_z)



print(mean_x)
# Initialise the subplot function using number of rows and columns
# print("outputting values")
# print("returning the value of n")
# print(n_x)
#
# print("returning the bins created")
# print(bin_returned_x)

#print plots of histogram
print_hist_graph(xaxis,yaxis,zaxis,bins)

print("length of data with bin 200")
print(len(n_x))
print(len(n_y))
print(len(n_z))
print("----------------------------")


peaks_x = return_peaks_detected(n_x, bin_returned_x, 2)
peaks_y = return_peaks_detected(n_y, bin_returned_y, 2)
peaks_z = return_peaks_detected(n_z, bin_returned_z, 2)
print("the number of peaks (or rebars) detected are: ")
print(len(peaks_x))
print(len(peaks_y))
print(len(peaks_z))


mark_peaks(peaks_x, peaks_y, peaks_z,"annotated_las.txt", input_file)
# gaps_x = analyze_gap(peaks_x)

graph_gap(peaks_x, 2.0, 2.72)
graph_gap(peaks_y, 2.0, 2.72)
graph_gap(peaks_z, 2.0, 2.72)

plt.savefig('gap.png')
plt.show()

print("data created based on bin number " + str(bins))