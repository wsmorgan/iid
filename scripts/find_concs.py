"""This code finds the concentration of every structure listed in
training_set_strucuters.dat and writes them to a file."""

out_file_name = ""

from os import system
train_f = open("training_set_structures.dat","r").read().strip().split("\n")

out_f = open(out_file_name,"w+") 

tt = 0
for struct in train_f:
    tt += 1
    print(tt,struct.split()[1])
    system("makestr.x struct_enum.out {}".format(struct.split()[1]))
    system("mv vasp.* POSCAR")

    with open("POSCAR","r") as pos_f:
        count = 0
        for line in pos_f:
            count += 1
            if count == 6:
                concs = [int(i) for i in line.strip().split()]
    system("rm POSCAR")
    out_f.write("{} {}\n".format(struct.split()[0],concs))

out_f.close()
