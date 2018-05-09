import os, fnmatch, re
import graph_plotter as plotter

path = 'C:\\_src\\7196\\'
projects = ['BMesh', 'BRing', 'Equipment', 'utilities', 'XData', 'XMesh', 'XN', 'XORA', 'XRing', 'Xs']
pattern_cpp = "*.cpp"
pattern_h = "*.h"

result_matrix = {}


def print_info():
    for project,file_matrix in result_matrix.iteritems():
        print ("===================================================")
        print ("I                                                  ")
        print ("I PROJECT: \t" + project)
        print ("I___________________________________________________")
        for file,lines  in file_matrix.iteritems():
            print ("I")
            print ("I FILE: " + file)
            for line in lines:
                print ("I   " + line)
        print ("I                                                  ")
        print ("===================================================")

for prj in projects:
    p_path = path + prj + "\\"

    listOfFiles = os.listdir(p_path)

    file_matrix = {}
    for file_name in listOfFiles:
        if fnmatch.fnmatch(file_name, pattern_cpp) or fnmatch.fnmatch(file_name, pattern_h):
            inputfile = open(p_path + file_name)
            for line in inputfile:
                result = re.match('#include \"\../.{1,}\.h', line)
                if result:
                    if file_name not in file_matrix:
                        file_matrix[file_name] = [line.rstrip()]
                    else:
                        file_matrix[file_name].append(line.rstrip())
            inputfile.close()

    if len(file_matrix) != 0:
        result_matrix[prj] = file_matrix

#print_info()

plotter.init_graph(result_matrix)

