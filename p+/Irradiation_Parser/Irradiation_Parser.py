
import re
import os
from LayerSpecification import LayerSpecification, LayerSpec
from MapRecord import MapRecord, MapRec
import numpy as np
import pylab

directory = 'J:\\180398\\logs\\irradiation\\'

def padded_layer_number(layer):
    padded_string = format(layer,'04')
    return padded_string

def file_walker(directory):
    """ Walk a directory and yield all files in the directory. """
    for dirName, subdirList, file_list in os.walk(directory):
        for file_name in file_list:
            yield os.path.join(dirName, file_name)

def find_record_files(directory):
    """ Find all log files for the treatments in the system. """
    normal_record = re.compile('map_record_\d{4}.csv$')
    resume_record = re.compile('map_record_\d{4}_resume_\d{2}.csv$')
    tuning_record = re.compile('map_record_\d{4}_tuning_\d{2}.csv$')
    file_walk = file_walker(directory)
    for file in file_walk:
        if re.search(normal_record, file) is not None:
            yield file
        elif re.search(resume_record, file) is not None:
            yield file
        elif re.search(tuning_record, file) is not None:
            yield file

def find_specification(record_file_name):
    directory = os.path.dirname(record_file_name)
    name = record_file_name.replace('record','specif')
    if os.path.exists(name):
        return name

def sum_charge_on_column(data, column):
    last_element = -1
    total_charge = 0.0
    items = []
    for item in data:
        if item[1] == last_element:
            items.append(item)
            total_charge += item[column]
            last_element = item[1]            
            continue
        else:
            if len(items) > 0:
                for item in items:
                    item[column] = total_charge
            items.clear()
            total_charge = 0.0

        last_element = item[1]
    return data

def create_beam_current_graph(spec, record, file_record):
    
    # Create arrays for graphing elements versus expected.
    data = []
    count = 0
    for element in record:
        spot_number = int(element[0]) - 1
        line = list()
        line.append(count)
        line.append(spec[spot_number][LayerSpec.MIN_BEAM_CURRENT_FB])
        line.append(spec[spot_number][LayerSpec.MAX_BEAM_CURRENT_FB])
        line.append(record[count][MapRec.BEAMCURRENT])
        count += 1
        data.append(line)
    
    data_array = np.array(data,dtype=np.float64)
    # Look for the maximum and minimum values
    data_max = np.amax(data_array, axis=0)
    data_min = np.amin(data_array, axis=0)
    max = np.amax(data_max[1:]) + 1
    min = np.amin(data_min[1:]) - 1
   
    fig, ax = pylab.subplots()
    pylab.ylim([min,max])
    ax.set_autoscaley_on(False)
    ax.plot(data_array[:,0], data_array[:,1], 'b', label="Beam Minimum")
    ax.plot(data_array[:,0], data_array[:,2], 'r',  label="Beam Maximum")
    ax.plot(data_array[:,0], data_array[:,3], 'g', label="Beam Feedback ")
    ax.set_xlabel('Timeslice (250 microseconds)')
    ax.set_ylabel('Beam Current V(IC Cyclo)')
    ax.legend()
    name = file_record +  '_beam_current.png'
    pylab.savefig(name)
    pylab.close()

def create_dose_graphs(spec, record, file_record):
    
    # Create arrays for graphing elements versus expected.
    count = 0
    data = []
    for element in record:
        spot_number = int(element[0]) - 1
        line = list()
        line.append(count)
        line.append(spot_number)
        line.append(spec[spot_number][LayerSpec.MIN_CHARGE_PRIM])
        line.append(spec[spot_number][LayerSpec.MAX_CHARGE_PRIM])
        line.append(spec[spot_number][LayerSpec.MIN_CHARGE_SEC])
        line.append(spec[spot_number][LayerSpec.MAX_CHARGE_SEC])
        line.append(record[count][MapRec.DOSE_PRIM])
        line.append(record[count][MapRec.DOSE_SEC])
        count+=1
        data.append(line)
    
    data_array = np.array(data,dtype=np.float64)
    # Look for the maximum and minimum values
    temp_data = sum_charge_on_column(data_array, 6)
    charged_data = sum_charge_on_column(temp_data, 7)
    data_max = np.amax(charged_data, axis=0)
    data_min = np.amin(charged_data, axis=0)
    max = np.amax(data_max[2:]) 
    min = np.amin(data_min[2:]) 
   
    fig, ax = pylab.subplots()
    pylab.ylim([min,max])
    ax.set_autoscaley_on(False)
    ax.plot(charged_data[:,0], charged_data[:,2], label="Min Charge Primary (C)")
    ax.plot(charged_data[:,0], charged_data[:,3], label="Max Charge Primary (C)")
    ax.plot(charged_data[:,0], charged_data[:,6], label="Charge Primary (C)")
    ax.set_xlabel('Timeslice (250 microseconds)')
    ax.set_ylabel('Dose Primary (Coloumbs)')
    ax.legend()
    name = file_record +  '_dose_primary.png'
    pylab.savefig(name)
    pylab.close()


    fig, ax = pylab.subplots()
    pylab.ylim([min,max])
    ax.set_autoscaley_on(False)
    ax.plot(charged_data[:,0], charged_data[:,4], label="Min Charge Secondary (C)")
    ax.plot(charged_data[:,0], charged_data[:,5], label="Max Charge Secondary (C)")
    ax.plot(charged_data[:,0], charged_data[:,7], label="Charge Secondary (C)")
    ax.set_xlabel('Timeslice (250 microseconds)')
    ax.set_ylabel('Dose Secondary (Coloumbs)')
    ax.legend()
    name = file_record +  '_dose_secondary.png'
    pylab.savefig(name)
    pylab.close()

def create_position_graphs(spec, record, file_record):
    
    # Create arrays for grpahing elements versus expected.
    count = 0
    data = []
    for element in record:
        spot_number = int(element[0]) - 1
        line = list()
        line.append(count)
        line.append(spec[spot_number][LayerSpec.X_POS_LOW])
        line.append(spec[spot_number][LayerSpec.X_POS_HIGH])
        line.append(spec[spot_number][LayerSpec.Y_POS_LOW])
        line.append(spec[spot_number][LayerSpec.Y_POS_HIGH])
        line.append(record[count][MapRec.X_POSITION])
        line.append(record[count][MapRec.Y_POSITION])
        count+=1
        data.append(line)
    
    data_array = np.array(data,dtype=np.float64)
    # Look for the maximum and minimum values
    data_max = np.amax(data_array, axis=0)
    data_min = np.amin(data_array, axis=0)
    max = np.amax(data_max[1:]) 
    min = np.amin(data_min[1:]) 
   
    fig, ax = pylab.subplots()
    pylab.ylim([-45,45])
    ax.set_autoscaley_on(False)
    ax.scatter(data_array[:,0], data_array[:,1], label="X Pos Min",marker='^', alpha=0.3)
    ax.scatter(data_array[:,0], data_array[:,2], label="X Pos Max",marker='v', alpha=0.3)
    ax.scatter(data_array[:,0], data_array[:,5], label="X Pos",marker='.', alpha=0.3)
    ax.set_xlabel('Timeslice (250 microseconds)')
    ax.set_ylabel('X Position (mm)')
    ax.legend()
    name = file_record +  '_x_position.png'
    pylab.savefig(name)
    pylab.close()

    fig, ax = pylab.subplots()
    pylab.ylim([-45,45])
    ax.set_autoscaley_on(False)
    ax.scatter(data_array[:,0], data_array[:,3], label="Y Pos Min", marker='^', alpha=0.3)
    ax.scatter(data_array[:,0], data_array[:,4], label="Y Pos Max", marker='v', alpha=0.3)
    ax.scatter(data_array[:,0], data_array[:,6], label="Y Pos", marker='.', alpha=0.3)
    ax.set_xlabel('Timeslice (250 microseconds)')
    ax.set_ylabel('Y Pos (mm)')
    ax.legend()
    name = file_record +  '_y_position.png'
    pylab.savefig(name)
    pylab.close()

def create_layer_reconstruction(record, file_record):
    
    # Create arrays for grpahing elements versus expected.
    count = 0

    data = []
    for element in record:
        spot_number = int(element[0]) - 1
        line = list()
        line.append(count)
        line.append(record[count][MapRec.Y_POSITION])
        line.append(record[count][MapRec.X_POSITION])
        line.append(record[count][MapRec.DOSE_PRIM])
        count+=1
        data.append(line)
    
    data_array = np.array(data,dtype=np.float64)
    # Look for the maximum and minimum values
    temp_data = sum_charge_on_column(data_array, 3)
    for item in temp_data:
        if ((item[0] == -10000) or (item[1] == -10000)):
            item[3] = 0
    temp_data[temp_data < -9000] = 0.0

    fig, ax = pylab.subplots()
    pylab.xlim([-200,200])
    pylab.ylim([-150, 150])
    ax.set_autoscalex_on(False)
    ax.set_autoscaley_on(False)
    colors = data_array[:,3] / np.linalg.norm(data_array[:,3])
    colors *= 100
    sc = ax.scatter(data_array[:,1], data_array[:,2], cmap='jet', c=colors, s=colors, alpha=0.4)
    fig.colorbar(sc)
    ax.set_ylabel('Y Position (mm)')
    ax.set_xlabel('X Position (mm)')
    name = file_record +  '_scatter.png'
    pylab.savefig(name)
    pylab.close()

for file in find_record_files(directory):
    try:
        record = MapRecord()    
        specification = LayerSpecification()
        record.parse_record(file)
        specification.parse_specification(find_specification(file))
        specification_array = np.array(specification.get_layers())
        specification = None
        record_array = np.array(record.get_layers())
        record = None
 
        if (file.find('_tuning_') == -1):
            create_beam_current_graph(specification_array,record_array, file)
            create_dose_graphs(specification_array,record_array, file)
            create_position_graphs(specification_array,record_array, file)
            create_layer_reconstruction(record_array, file)
        else:
            create_beam_current_graph(specification_array,record_array, file)
            create_dose_graphs(specification_array,record_array, file)
    except IndexError as e:
            print('File: {}, Error {}'.format(file,e))


