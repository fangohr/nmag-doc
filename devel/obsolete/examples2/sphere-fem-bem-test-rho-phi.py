import nmag
from nmag import SI,mesh
import nmesh 
import os

H_x = SI(0.0e6, "A/m") 
H_y = SI(0.0e6, "A/m") 
H_z = SI(0.0e6, "A/m") 

intensive_param_by_name={"H_x":H_x, "H_y":H_y, "H_z":H_z}

mat_Py = nmag.MagMaterial(name="Py",
                          Ms=SI(1e6,"A/m"),
                          exchange_coupling=SI(13.0e-12, "J/m")
                          )

sim = nmag.Simulation("sphere", fem_only=False)
unit_length = SI(1e-9,"m")

meshfile = "central-sphere-fine.nmesh"
sim.load_mesh(meshfile, [("Py", mat_Py)], unit_length=unit_length)

def initial_magnetization((x, y, z), mag_type):
    return [1, 0, 0]

sim.set_magnetization(initial_magnetization)

sim.compute_H_fields()
sim.fun_update_energies([])

sim.save_field('m','m-sphere-fem-bem.nvf')
sim.save_data_table()

default_val = 1e-99

f = open("probe-sphere-fem-bem-test-rho-phi.dat", "w")
f.write("x_coords\tm_x\tm_y\tm_z\tm_x\th_demag_x\th_demag_y\th_demag_z\trho\tphi\n")

for p_x in range(-1000,1001):

    rho = sim._get_from_field(
        sim.fields['rho'],
        'rho',
        pos=[p_x*0.1,0.0,0.0],
        name='rho',
        units=SI(1,"A/m^2"),
        pos_units=unit_length,
        si_units=SI(1,"A/m^2"))

    if rho==None:
        rho = default_val
    
    phi = sim._get_from_field(
        sim.fields['phi'],
        'phi',
        pos=[p_x*0.1,0.0,0.0],
        name='phi',
        units=SI(1,"A"),
        pos_units=unit_length,
        si_units=SI(1,"A"))
    if phi==None:
        phi = default_val
        
    h_demag = sim.get_H_demag(pos=[p_x*0.1,0.0,0.0],pos_unit=unit_length)
    if h_demag == None:
        hx,hy,hz = 3*[default_val]
    else:
        hx,hy,hz = h_demag

    magnetization = sim.get_M([p_x*0.1,0.0,0.0],name="Py",pos_unit=unit_length)
    if magnetization == None:
        mx,my,mz = 3*[default_val]
    else: mx,my,mz = magnetization
    f.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (p_x*0.1, mx, my,mz, hx, hy, hz, rho, phi))
    
f.close()
sim.save_fields_vtk('sphere-fem-bem-test-rho-phi.vtk')

"""
-10.000000 0.000000 0.000000 0.000000 0.000000 0.000000 0.000000
-9.900000 1000000.000000 0.000000 0.000000 -332635.621585 -208.876110 54.546173
-9.800000 1000000.000000 0.000000 0.000000 -332632.132334 -204.532102 56.903911
-9.700000 1000000.000000 0.000000 0.000000 -332628.643083 -200.188094 59.261649
-9.600000 1000000.000000 0.000000 0.000000 -332625.153831 -195.844086 61.619387
-9.500000 1000000.000000 0.000000 0.000000 -332621.664580 -191.500078 63.977125
-9.400000 1000000.000000 0.000000 0.000000 -332618.175329 -187.156070 66.334862
-9.300000 1000000.000000 0.000000 0.000000 -332614.686078 -182.812061 68.692600
-9.200000 1000000.000000 0.000000 0.000000 -332611.196826 -178.468053 71.050338
-9.100000 1000000.000000 0.000000 0.000000 -332607.930518 -173.873492 73.607753
-9.000000 1000000.000000 0.000000 0.000000 -332597.706395 -169.995882 74.288301
-8.900000 1000000.000000 0.000000 0.000000 -332587.388004 -165.923317 74.801690
-8.800000 1000000.000000 0.000000 0.000000 -332577.069613 -161.850751 75.315079
-8.700000 1000000.000000 0.000000 0.000000 -332566.751222 -157.778185 75.828468
-8.600000 1000000.000000 0.000000 0.000000 -332556.432830 -153.705619 76.341857
-8.500000 1000000.000000 0.000000 0.000000 -332546.039025 -149.846149 76.669656
-8.400000 1000000.000000 0.000000 0.000000 -332535.338789 -146.852549 76.243347
-8.300000 1000000.000000 0.000000 0.000000 -332526.627051 -141.572259 75.555818
-8.200000 1000000.000000 0.000000 0.000000 -332518.564882 -135.544993 74.782959
-8.100000 1000000.000000 0.000000 0.000000 -332510.384833 -130.734947 73.802860
-8.000000 1000000.000000 0.000000 0.000000 -332502.473568 -127.131172 73.110034
-7.900000 1000000.000000 0.000000 0.000000 -332495.568237 -124.381107 73.662677
-7.800000 1000000.000000 0.000000 0.000000 -332488.662907 -121.631043 74.215320
-7.700000 1000000.000000 0.000000 0.000000 -332481.757576 -118.880979 74.767964
-7.600000 1000000.000000 0.000000 0.000000 -332475.062900 -116.098317 75.216829
-7.500000 1000000.000000 0.000000 0.000000 -332472.431903 -112.686840 73.663751
-7.400000 1000000.000000 0.000000 0.000000 -332469.800906 -109.275363 72.110674
-7.300000 1000000.000000 0.000000 0.000000 -332467.169909 -105.863886 70.557597
-7.200000 1000000.000000 0.000000 0.000000 -332464.538912 -102.452409 69.004519
-7.100000 1000000.000000 0.000000 0.000000 -332462.546796 -101.351657 67.028867
-7.000000 1000000.000000 0.000000 0.000000 -332461.301013 -98.439417 66.308886
-6.900000 1000000.000000 0.000000 0.000000 -332460.055230 -95.527176 65.588905
-6.800000 1000000.000000 0.000000 0.000000 -332458.809447 -92.614935 64.868924
-6.700000 1000000.000000 0.000000 0.000000 -332460.003789 -88.895824 64.427374
-6.600000 1000000.000000 0.000000 0.000000 -332461.430406 -85.099908 64.012326
-6.500000 1000000.000000 0.000000 0.000000 -332462.732553 -81.374546 63.408754
-6.400000 1000000.000000 0.000000 0.000000 -332463.112771 -77.211252 61.590050
-6.300000 1000000.000000 0.000000 0.000000 -332462.769380 -72.638917 58.829927
-6.200000 1000000.000000 0.000000 0.000000 -332462.316347 -68.221825 55.861291
-6.100000 1000000.000000 0.000000 0.000000 -332462.191748 -64.739955 53.092425
-6.000000 1000000.000000 0.000000 0.000000 -332462.544788 -62.291026 50.713339
-5.900000 1000000.000000 0.000000 0.000000 -332462.897828 -59.842096 48.334252
-5.800000 1000000.000000 0.000000 0.000000 -332463.874229 -55.757208 46.985464
-5.700000 1000000.000000 0.000000 0.000000 -332463.678793 -52.998655 45.316503
-5.600000 1000000.000000 0.000000 0.000000 -332464.260577 -51.045215 43.936064
-5.500000 1000000.000000 0.000000 0.000000 -332466.067702 -49.536436 42.690453
-5.400000 1000000.000000 0.000000 0.000000 -332468.487765 -47.873507 41.291672
-5.300000 1000000.000000 0.000000 0.000000 -332471.024031 -46.548761 39.898683
-5.200000 1000000.000000 0.000000 0.000000 -332473.778454 -45.858905 38.516566
-5.100000 1000000.000000 0.000000 0.000000 -332476.532876 -45.169049 37.134450
-5.000000 1000000.000000 0.000000 0.000000 -332479.499457 -44.166500 36.219728
-4.900000 1000000.000000 0.000000 0.000000 -332482.477967 -43.146368 35.331288
-4.800000 1000000.000000 0.000000 0.000000 -332485.357812 -42.204744 34.494638
-4.700000 1000000.000000 0.000000 0.000000 -332487.468434 -41.875183 34.061757
-4.600000 1000000.000000 0.000000 0.000000 -332490.339118 -41.147594 32.956886
-4.500000 1000000.000000 0.000000 0.000000 -332493.838271 -40.090891 31.296369
-4.400000 1000000.000000 0.000000 0.000000 -332497.446798 -39.097472 30.963714
-4.300000 1000000.000000 0.000000 0.000000 -332501.071090 -38.113175 30.822447
-4.200000 1000000.000000 0.000000 0.000000 -332504.695381 -37.128877 30.681180
-4.100000 1000000.000000 0.000000 0.000000 -332508.319673 -36.144580 30.539913
-4.000000 1000000.000000 0.000000 0.000000 -332511.936142 -35.163114 30.370129
-3.900000 1000000.000000 0.000000 0.000000 -332515.797376 -34.421607 30.018556
-3.800000 1000000.000000 0.000000 0.000000 -332520.127542 -34.036602 29.980128
-3.700000 1000000.000000 0.000000 0.000000 -332524.457910 -33.652069 29.942855
-3.600000 1000000.000000 0.000000 0.000000 -332528.788279 -33.267536 29.905582
-3.500000 1000000.000000 0.000000 0.000000 -332533.118647 -32.883004 29.868309
-3.400000 1000000.000000 0.000000 0.000000 -332537.111052 -32.669686 29.753184
-3.300000 1000000.000000 0.000000 0.000000 -332540.971929 -32.523001 29.607761
-3.200000 1000000.000000 0.000000 0.000000 -332544.520735 -32.376626 29.189730
-3.100000 1000000.000000 0.000000 0.000000 -332547.439588 -32.230873 28.221411
-3.000000 1000000.000000 0.000000 0.000000 -332550.358442 -32.085120 27.253091
-2.900000 1000000.000000 0.000000 0.000000 -332551.727487 -31.732185 27.599916
-2.800000 1000000.000000 0.000000 0.000000 -332552.959962 -31.360993 28.062632
-2.700000 1000000.000000 0.000000 0.000000 -332554.192438 -30.989802 28.525348
-2.600000 1000000.000000 0.000000 0.000000 -332556.280614 -30.269901 29.125140
-2.500000 1000000.000000 0.000000 0.000000 -332557.907993 -29.685158 29.479507
-2.400000 1000000.000000 0.000000 0.000000 -332558.153390 -29.510023 29.111686
-2.300000 1000000.000000 0.000000 0.000000 -332558.398787 -29.334887 28.743865
-2.200000 1000000.000000 0.000000 0.000000 -332558.644183 -29.159751 28.376045
-2.100000 1000000.000000 0.000000 0.000000 -332558.987516 -29.198194 27.641672
-2.000000 1000000.000000 0.000000 0.000000 -332559.376781 -29.336803 26.735388
-1.900000 1000000.000000 0.000000 0.000000 -332560.028872 -29.319357 25.972528
-1.800000 1000000.000000 0.000000 0.000000 -332559.865358 -28.885003 25.311726
-1.700000 1000000.000000 0.000000 0.000000 -332559.545660 -28.400585 24.652392
-1.600000 1000000.000000 0.000000 0.000000 -332558.354742 -28.631966 24.186538
-1.500000 1000000.000000 0.000000 0.000000 -332557.145588 -28.707201 23.443897
-1.400000 1000000.000000 0.000000 0.000000 -332555.936361 -28.773264 22.686117
-1.300000 1000000.000000 0.000000 0.000000 -332554.842193 -28.663517 21.982658
-1.200000 1000000.000000 0.000000 0.000000 -332553.971224 -28.212725 21.384571
-1.100000 1000000.000000 0.000000 0.000000 -332553.100255 -27.761933 20.786485
-1.000000 1000000.000000 0.000000 0.000000 -332552.229286 -27.311141 20.188399
-0.900000 1000000.000000 0.000000 0.000000 -332550.863616 -27.092614 19.667525
-0.800000 1000000.000000 0.000000 0.000000 -332549.381606 -26.928708 19.164810
-0.700000 1000000.000000 0.000000 0.000000 -332547.899595 -26.764803 18.662094
-0.600000 1000000.000000 0.000000 0.000000 -332546.500808 -26.732533 18.048610
-0.500000 1000000.000000 0.000000 0.000000 -332545.304914 -27.021184 17.165079
-0.400000 1000000.000000 0.000000 0.000000 -332544.075026 -27.277358 16.402341
-0.300000 1000000.000000 0.000000 0.000000 -332542.668912 -27.365180 16.265776
-0.200000 1000000.000000 0.000000 0.000000 -332541.469300 -27.502275 15.980540
-0.100000 1000000.000000 0.000000 0.000000 -332542.030328 -28.059484 14.427733
0.000000 1000000.000000 0.000000 0.000000 -332542.606083 -28.572331 12.614109
0.100000 1000000.000000 0.000000 0.000000 -332543.431202 -28.824779 11.249568
0.200000 1000000.000000 0.000000 0.000000 -332544.373403 -29.019082 10.386620
0.300000 1000000.000000 0.000000 0.000000 -332545.315604 -29.213384 9.523672
0.400000 1000000.000000 0.000000 0.000000 -332546.257805 -29.407686 8.660724
0.500000 1000000.000000 0.000000 0.000000 -332547.200005 -29.601988 7.797776
0.600000 1000000.000000 0.000000 0.000000 -332548.277781 -29.719914 6.835679
0.700000 1000000.000000 0.000000 0.000000 -332550.241317 -29.338837 5.225802
0.800000 1000000.000000 0.000000 0.000000 -332552.204853 -28.957760 3.615925
0.900000 1000000.000000 0.000000 0.000000 -332554.716146 -28.681783 1.973049
1.000000 1000000.000000 0.000000 0.000000 -332558.408979 -28.632513 0.258993
1.100000 1000000.000000 0.000000 0.000000 -332562.101812 -28.583243 -1.455064
1.200000 1000000.000000 0.000000 0.000000 -332565.794644 -28.533973 -3.169120
1.300000 1000000.000000 0.000000 0.000000 -332569.018172 -28.401354 -4.516505
1.400000 1000000.000000 0.000000 0.000000 -332570.812544 -27.532280 -5.296859
1.500000 1000000.000000 0.000000 0.000000 -332572.570521 -26.536506 -6.112722
1.600000 1000000.000000 0.000000 0.000000 -332574.328497 -25.540732 -6.928585
1.700000 1000000.000000 0.000000 0.000000 -332576.086473 -24.544959 -7.744447
1.800000 1000000.000000 0.000000 0.000000 -332577.772224 -23.619197 -8.578695
1.900000 1000000.000000 0.000000 0.000000 -332579.112720 -23.028110 -9.500827
2.000000 1000000.000000 0.000000 0.000000 -332580.453215 -22.437023 -10.422960
2.100000 1000000.000000 0.000000 0.000000 -332581.484771 -22.016441 -11.329161
2.200000 1000000.000000 0.000000 0.000000 -332582.442686 -21.588213 -12.201483
2.300000 1000000.000000 0.000000 0.000000 -332582.719373 -20.437220 -12.354204
2.400000 1000000.000000 0.000000 0.000000 -332582.996061 -19.286226 -12.506924
2.500000 1000000.000000 0.000000 0.000000 -332583.272748 -18.135233 -12.659644
2.600000 1000000.000000 0.000000 0.000000 -332583.549435 -16.984239 -12.812364
2.700000 1000000.000000 0.000000 0.000000 -332583.532694 -15.531974 -13.250621
2.800000 1000000.000000 0.000000 0.000000 -332582.960180 -14.406860 -13.454293
2.900000 1000000.000000 0.000000 0.000000 -332582.042208 -13.601491 -13.411623
3.000000 1000000.000000 0.000000 0.000000 -332581.124236 -12.796123 -13.368953
3.100000 1000000.000000 0.000000 0.000000 -332580.030696 -12.414774 -13.872685
3.200000 1000000.000000 0.000000 0.000000 -332578.904825 -12.111510 -14.477040
3.300000 1000000.000000 0.000000 0.000000 -332577.679540 -11.488054 -14.763900
3.400000 1000000.000000 0.000000 0.000000 -332576.372034 -10.599781 -14.788171
3.500000 1000000.000000 0.000000 0.000000 -332575.064528 -9.711508 -14.812443
3.600000 1000000.000000 0.000000 0.000000 -332573.654769 -8.629810 -15.344094
3.700000 1000000.000000 0.000000 0.000000 -332572.672132 -7.122295 -15.823984
3.800000 1000000.000000 0.000000 0.000000 -332571.764938 -5.558516 -16.262979
3.900000 1000000.000000 0.000000 0.000000 -332570.857744 -3.994736 -16.701975
4.000000 1000000.000000 0.000000 0.000000 -332570.034483 -2.205905 -16.999351
4.100000 1000000.000000 0.000000 0.000000 -332569.218522 -0.397499 -17.284410
4.200000 1000000.000000 0.000000 0.000000 -332569.382100 0.733096 -17.686165
4.300000 1000000.000000 0.000000 0.000000 -332569.959146 1.577585 -18.137178
4.400000 1000000.000000 0.000000 0.000000 -332570.589507 2.591292 -18.592705
4.500000 1000000.000000 0.000000 0.000000 -332571.321537 3.927694 -19.056841
4.600000 1000000.000000 0.000000 0.000000 -332572.053567 5.264095 -19.520977
4.700000 1000000.000000 0.000000 0.000000 -332572.785597 6.600496 -19.985113
4.800000 1000000.000000 0.000000 0.000000 -332573.517627 7.936898 -20.449249
4.900000 1000000.000000 0.000000 0.000000 -332574.534767 9.257605 -20.879211
5.000000 1000000.000000 0.000000 0.000000 -332576.493906 10.472974 -20.906927
5.100000 1000000.000000 0.000000 0.000000 -332578.473353 11.685260 -20.902409
5.200000 1000000.000000 0.000000 0.000000 -332580.452800 12.897546 -20.897891
5.300000 1000000.000000 0.000000 0.000000 -332582.432247 14.109832 -20.893373
5.400000 1000000.000000 0.000000 0.000000 -332584.411694 15.322118 -20.888855
5.500000 1000000.000000 0.000000 0.000000 -332586.391142 16.534404 -20.884336
5.600000 1000000.000000 0.000000 0.000000 -332588.676174 17.317627 -20.925422
5.700000 1000000.000000 0.000000 0.000000 -332591.122942 18.007364 -20.918691
5.800000 1000000.000000 0.000000 0.000000 -332593.657239 18.785987 -20.810962
5.900000 1000000.000000 0.000000 0.000000 -332596.191536 19.564610 -20.703233
6.000000 1000000.000000 0.000000 0.000000 -332598.725833 20.343233 -20.595504
6.100000 1000000.000000 0.000000 0.000000 -332601.260130 21.121856 -20.487776
6.200000 1000000.000000 0.000000 0.000000 -332603.794427 21.900479 -20.380047
6.300000 1000000.000000 0.000000 0.000000 -332606.328725 22.679102 -20.272318
6.400000 1000000.000000 0.000000 0.000000 -332608.863022 23.457725 -20.164589
6.500000 1000000.000000 0.000000 0.000000 -332611.375422 24.237386 -20.094436
6.600000 1000000.000000 0.000000 0.000000 -332614.215308 24.607503 -19.546428
6.700000 1000000.000000 0.000000 0.000000 -332617.119270 24.862340 -18.858418
6.800000 1000000.000000 0.000000 0.000000 -332620.023232 25.117176 -18.170408
6.900000 1000000.000000 0.000000 0.000000 -332622.927194 25.372012 -17.482398
7.000000 1000000.000000 0.000000 0.000000 -332625.831156 25.626848 -16.794388
7.100000 1000000.000000 0.000000 0.000000 -332628.735118 25.881684 -16.106378
7.200000 1000000.000000 0.000000 0.000000 -332631.639080 26.136520 -15.418369
7.300000 1000000.000000 0.000000 0.000000 -332634.543042 26.391357 -14.730359
7.400000 1000000.000000 0.000000 0.000000 -332637.447004 26.646193 -14.042349
7.500000 1000000.000000 0.000000 0.000000 -332640.350967 26.901029 -13.354339
7.600000 1000000.000000 0.000000 0.000000 -332643.296371 26.982433 -12.890604
7.700000 1000000.000000 0.000000 0.000000 -332646.534695 26.696499 -12.521713
7.800000 1000000.000000 0.000000 0.000000 -332649.773018 26.410566 -12.152822
7.900000 1000000.000000 0.000000 0.000000 -332653.011341 26.124632 -11.783931
8.000000 1000000.000000 0.000000 0.000000 -332656.324512 25.602712 -11.289946
8.100000 1000000.000000 0.000000 0.000000 -332659.771696 24.658265 -10.571986
8.200000 1000000.000000 0.000000 0.000000 -332663.218880 23.713817 -9.854025
8.300000 1000000.000000 0.000000 0.000000 -332666.627448 22.807481 -9.163539
8.400000 1000000.000000 0.000000 0.000000 -332669.892599 22.042694 -8.575096
8.500000 1000000.000000 0.000000 0.000000 -332673.157750 21.277907 -7.986653
8.600000 1000000.000000 0.000000 0.000000 -332676.422901 20.513120 -7.398210
8.700000 1000000.000000 0.000000 0.000000 -332679.688051 19.748332 -6.809767
8.800000 1000000.000000 0.000000 0.000000 -332682.985801 19.247475 -5.984602
8.900000 1000000.000000 0.000000 0.000000 -332685.907591 19.702873 -4.910404
9.000000 1000000.000000 0.000000 0.000000 -332688.716238 20.416943 -3.782937
9.100000 1000000.000000 0.000000 0.000000 -332691.524885 21.131013 -2.655470
9.200000 1000000.000000 0.000000 0.000000 -332693.395173 21.353945 -1.708490
9.300000 1000000.000000 0.000000 0.000000 -332695.091190 21.485664 -0.795030
9.400000 1000000.000000 0.000000 0.000000 -332696.787208 21.617383 0.118430
9.500000 1000000.000000 0.000000 0.000000 -332698.483226 21.749102 1.031890
9.600000 1000000.000000 0.000000 0.000000 -332700.179244 21.880821 1.945350
9.700000 1000000.000000 0.000000 0.000000 -332701.875261 22.012539 2.858810
9.800000 1000000.000000 0.000000 0.000000 -332703.571279 22.144258 3.772271
9.900000 1000000.000000 0.000000 0.000000 -332705.267297 22.275977 4.685731
10.000000 1000000.000000 0.000000 0.000000 -332706.963315 22.407696 5.599191
"""