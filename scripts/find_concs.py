"""This code finds the concentration of every structure listed in
training_set_strucuters.dat and writes them to a file."""

# out_file_name = ""

# from os import system
# train_f = open("training_set_structures.dat","r").read().strip().split("\n")

# out_f = open(out_file_name,"w+")

# tt = 0
# for struct in train_f:
#     tt += 1
#     print(tt,struct.split()[1])
#     system("makestr.x struct_enum.out {}".format(struct.split()[1]))
#     system("mv vasp.* POSCAR")

#     with open("POSCAR","r") as pos_f:
#         count = 0
#         for line in pos_f:
#             count += 1
#             if count == 6:
#                 concs = [i for i in line.strip().split()]
#     system("rm POSCAR")
#     out_f.write("{}     {}\n".format(struct.split()[0],"".join(concs)))

# out_f.close()

# inf = open("data/energies_IID","r").read().split("\n")[:-1]
# outf = open("data/AlCuNi_IID.txt","w+")

# count = 0
# for line in inf:
#     count += 1
#     temp = line.split()[1:]
#     print("t",temp)

#     conc = [str(temp[0][2:-2]),str(temp[1][1:-2]),str(temp[2][1:-2])]
#     print(conc)

#     outf.write("{}     {}\n".format(count," ".join(conc)))

# outf.close()

inf = open("data/structures.in_AlCuNi","r").read().strip().split("\n")
outf = open("data/AlCuNi_500_IID_2.txt","w+")

next_conc = 8
loc = 0
count = 0
for line in inf:

    if loc == next_conc:

        count += 1
        conc = [int(i) for i in line.strip().split()]

        next_conc += (sum(conc)+9)
        outf.write("{}     {}\n".format(count," ".join([str(i) for i in conc])))

    loc += 1

outf.close()
