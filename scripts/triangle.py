import ternary
import matplotlib.pyplot as plt

def _generate_heatmap_data(scale=5):
    from ternary.helpers import simplex_iterator
    d = dict()
    for (i, j, k) in simplex_iterator(scale):
        d[(i, j, k)] = _color_point(i, j, k, scale)
    return d

def _en_to_enth(energy,concs,A,B,C):
    enth = abs(energy - concs[0]*A -concs[1]*B -concs[2]*C)

    return enth

def _energy_to_enthalpy(energy):
    """Converts energy to enthalpy.
    
    This function take the energies stored in the energy array and
    converts them to formation enthalpy.

    Parameters
    ---------
    energy : list of lists of floats
    
    Returns
    -------
    enthalpy : list of lists containing the enthalpies.
    """
    
    pureA = [energy[0][1],energy[0][1]]
    pureB = [energy[1][1],energy[1][1]]
    pureC = [energy[2][1],energy[2][1]]
    # pureA = [energy[0][0],energy[0][1]]
    # pureB = [energy[1][0],energy[1][1]]
    # pureC = [energy[2][0],energy[2][1]]

    enthalpy = []
    for en in energy:
        c = en[2]
        conc = [float(i)/sum(c) for i in c]

        CE = _en_to_enth(en[0],conc,pureA[0],pureB[0],pureC[0])
        VASP = _en_to_enth(en[1],conc,pureA[1],pureB[1],pureC[1])

        enthalpy.append([CE,VASP,c])
        

    return enthalpy
    
def _find_error(vals):
    """Find the errors in the energy values.

    This function finds the errors in the enthalpys.

    Parameters
    ----------
    vals : list of lists of floats

    Returns
    -------
    err_vals : list of lists containing the errors.
    """

    err_vals = []
    for en in vals:
        c = en[2]
        conc = [float(i)/sum(c) for i in c]
        

        err = abs(en[0]-en[1])

        err_vals.append([conc,err])

    return err_vals

def _color_point(x,y,z,scale):
    r = x/float(scale)
    g = y/float(scale)
    b = z/float(scale)
    return (r, g, b)

def _read_data(fname):

    energy = []
    with open(fname,'r') as f:
        for line in f:
            CE = abs(float(line.strip().split()[0]))
            VASP = abs(float(line.strip().split()[1]))
            conc = [i for i in line.strip().split()[2:]]

            conc_f = []
            for c in conc:
                if '[' in c and ']' in c:
                    conc_f.append(int(c[1:-1]))
                elif '[' in c:
                    conc_f.append(int(c[1:-1]))
                elif ']' in c or ',' in c:
                    conc_f.append(int(c[:-1]))
                # elif ',' in c:
                #     conc_f.append(int(c[:-1]))                    
                else:
                    conc_f.append(int(c))
            energy.append([CE,VASP,conc_f])
    return energy

def _read_concs(fname):
    """Reads the concentrations from a file.

    Parameters
    ----------
    fname : str
        The input file name.
    
    Returns
    -------
    out : list of lists of floats
        The list of the concetrations and their weights.
    """

    concs = []
    out = []
    with open(fname,"r") as f:
        for line in f:
            conc = [i for i in line.strip().split()[2:]]

            conc_f = []
            for c in conc:
                if '[' in c and ']' in c:
                    conc_f.append(int(c[1:-1]))
                elif '[' in c:
                    conc_f.append(int(c[1:-1]))
                elif ']' in c or ',' in c:
                    conc_f.append(int(c[:-1]))
                else:
                    conc_f.append(int(c))

            conc_f = [float(j)/sum(conc_f) for j in conc_f]

            if conc_f in concs:
                loc = concs.index(conc_f)
                out[loc][1] += 1
            else:
                concs.append(conc_f)
                out.append([conc_f,1])
                
    return out
            
def enthalpy_plot(fname):
    """Plots the CE vs VASP enthalpies.

    Plots the CE data vs the VASP data to see if a linear relationship exists.

    Parameters
    ----------
    fname : string containing the file name.
    """

    energies = _read_data(fname)
    enthalpy = _energy_to_enthalpy(energies)
    CE = []
    VASP = []

    colors = []
    for en in enthalpy:
        x = en[2][0]
        y = en[2][1]
        z = en[2][2]
        colors.append(_color_point(x,y,z,float(sum(en[2]))))
        CE.append(en[0])#*1000.0)
        VASP.append(en[1])#*1000.0)


    plt.scatter(CE,VASP,facecolors=colors,edgecolor='none',cmap=plt.cm.brg)
    plt.plot([0,10000],[0,10000],linestyle='--',c='k')
    axis_lim = max([max(CE),max(VASP)])
    plt.xlim([0,axis_lim])
    plt.ylim([0,axis_lim])
    plt.title("Enthalpy of Lowest Energy Structures",fontsize=20)
    plt.xlabel('Cluster Expansion (eV/atom)',fontsize=16)
    plt.ylabel('DFT (eV/atom)',fontsize=16)
    plt.show()


def energy_plot(fname):
    """Plots the CE vs VASP energies.

    Plots the CE data vs the VASP data to see if a linear relationship exists.

    Parameters
    ----------
    fname : string containing the file name.
    """

    energies = _read_data(fname)
    CE = []
    VASP = []

    colors = []
    for en in energies:
        # colors.append((x[i]/100.0,y[i]/100.0,z[i]/100.0))
        x = en[2][0]
        y = en[2][1]
        z = en[2][2]
        colors.append(_color_point(x,y,z,float(sum(en[2]))))
        CE.append(en[0])#*1000.0)
        VASP.append(en[1])#*1000.0)


    plt.scatter(CE,VASP,facecolors=colors,edgecolor='none',cmap=plt.cm.brg)
    plt.plot([0,10000],[0,10000],linestyle='--',c='k')
    plt.xlim([3.5,6])
    plt.ylim([3.5,6])
    plt.title("Energy of Lowest Energy Structures",fontsize=20)
    plt.xlabel('Cluster Expansion (eV/atom)',fontsize=16)
    plt.ylabel('DFT (eV/atom)',fontsize=16)
    plt.show()

def make_ternary_legend(elements):
    """Makes the legend for concentraition plots."""

    scale = 100
    data = _generate_heatmap_data(scale)

    figure, tax = ternary.figure(scale=100, permutation="210")
    tax.heatmap(data, colormap=False)
    tax.boundary(linewidth = 0.0)
    tax.right_corner_label(elements[0], position=(0.95,0.1), fontsize=16)
    tax.top_corner_label(elements[1], position=(-0.075,1.15), fontsize=16)
    tax.left_corner_label(elements[2], position=(-0.05,0.1), fontsize=16)
    plt.axis("off")
    plt.show()

def _highest_error_only(errors):
    """Removes any duplicate concentrations that have lower errors.

    This script take a list of errors and concentrations and returns
    only the highest error for each concentration.

    Parameters
    ----------
    errors : list of lists of floats
        A list containing [errors,[concentrations]] in each list entry.

    Returns
    -------
    sorted_errors : list of list of floats
        The reduced list of errors.
    """

    sorted_errors = []
    concs = []
    for er in errors:
        c = er[0]

        if c not in concs:
            concs.append(c)
            sorted_errors.append([c,er[1]])
        else:
            loc = concs.index(c)
            # print("loc",loc)
            if sorted_errors[loc][1] < er[1]:
                sorted_errors[loc][1] = er[1]
                # print(er[1])

    return sorted_errors
  
def conc_err_plot(fname, elements=None, title=None, colormap=None, reduce=True, conc_line=None,
                  line_col=None, concs = False, plot_type="Scatter", dist=None, **kwargs):
    """Plots the error in the CE data.
    
    This plots the error in the CE predictions within a ternary concentration diagram.

    Parameters
    ----------
    fname : str
        The the input file name.
    elements : list of str, None
        A list containing the elemnt names in the same order as they appear in the VASP Poscars.
    title : str, None
        The name of the plot.
    colormap : str, None
        The name of the colormap for the plot.
    reduce : bool, True
        True if the input data is to be reduced by concentration.
    conc_line : list of int, None
        The value of the constant percentage line to be drawn.
    line_col : list of str, None
        A list of the colors to be used for each conc line.
    concs : bool, False
        True if the input file contains only structure number and concentration.
    plot_type : str, Scatter
        The type of plot to be used (Scatter or Contour).
    kwargs : 
        Any kwargs to pass through to matplotlib.
    """

    if concs:
        this_data = _read_concs(fname)
    else:
        energies = _read_data(fname)
        enthalpy = _energy_to_enthalpy(energies)
        temp_errors = _find_error(enthalpy)
        if reduce:
            this_data = _highest_error_only(temp_errors)
        else:
            this_data = temp_errors

    scale = 100
    figure, tax = ternary.figure(scale=scale)
    tax.boundary(linewidth = 1.0)
    # make the title
    if title != None:
        tax.set_title(title,fontsize=20,y=1.05)

    if "SCAT" in plot_type.upper():
        points = []
        colors = []
        total = 0
        for data in this_data:
            concs = data[0]
            points.append((concs[0]*100,concs[1]*100,concs[2]*100))
            colors.append(data[1])
            total += data[1]
        
        if colormap != None:
            colormap = plt.get_cmap(colormap)
            tax.scatter(points, vmin=0, vmax=max(colors), colormap=colormap, colorbar=True, c=colors, cmap=colormap, **kwargs)
        else:
            tax.scatter(points, **kwargs)
            
        tax.gridlines(multiple=10,color="blue")

    elif "CONT" in plot_type.upper():
        from itertools import combinations
        vals = range(0,scale+1)#*10+10,5)
        allowed = list(combinations(vals,3))

        points = {}
        for point in allowed:
            # points[(float(point[0])/10,float(point[1])/10,float(point[2])/10)] = 0
            points[(float(point[0]),float(point[1]),float(point[2]))] = 0

        total = 0
        for data in this_data:
            concs = data[0]
            points[(float(concs[0]*100),float(concs[1]*100),float(concs[2]*100))] = data[1]

        if colormap != None:
            colormap = plt.get_cmap(colormap)
            tax.heatmap(points,colormap=colormap, colorbar=True, cmap=colormap, dist=None,
                        **kwargs)
        else:
            tax.heatmap(points, scale, dist=dist, **kwargs)
            
    # draw any constant concentration lines
    if conc_line != None and line_col != None:
        if len(conc_line) != len(line_col) and len(line_col) != 1:
            print("WARNING. The number fo line colors does not match the number of conc_lines. "
                  "All lines will now be draw with the first supplied color.")
            for conc in conc_line:
                tax.horizontal_line(conc,color=line_col[0])
                tax.left_parallel_line(conc,color=line_col[0])
                tax.right_parallel_line(conc,color=line_col[0])
        elif len(line_col) == 1:
            for conc in conc_line:
                tax.horizontal_line(conc,color=line_col[0])
                tax.left_parallel_line(conc,color=line_col[0])
                tax.right_parallel_line(conc,color=line_col[0])
        else:
            for i in range(len(conc_line)):
                tax.horizontal_line(conc_line[i],color=line_col[i])
                tax.left_parallel_line(conc_line[i],color=line_col[i])
                tax.right_parallel_line(conc_line[i],color=line_col[i])
    elif conc_line != None:
        for conc in conc_line:
            tax.horizontal_line(conc)
            tax.left_parallel_line(conc)
            tax.right_parallel_line(conc)
                
    if elements != None:
        tax.right_corner_label(elements[0], position=(0.95,0.1), fontsize=16)
        tax.top_corner_label(elements[1], position=(-0.075,1.15), fontsize=16)
        tax.left_corner_label(elements[2], position=(-0.05,0.1), fontsize=16)

    # tax.ticks(multiple=10)
    tax.clear_matplotlib_ticks()
    plt.axis('off')
    plt.show()

# make_ternary_legend(["Al","Cu","Ni"])
conc_err_plot('energies_orig',elements=["Al","Cu","Ni"],
              title="AlCuNi Lowest Energy Errors",colormap="Greys",
              cbarlabel="Error in Formation Enthalpy (eV/atom)", plot_type="cont",dist=5)#, s=60)

# enthalpy_plot('energies_Al30')

# energy_plot('energies_Al30')
