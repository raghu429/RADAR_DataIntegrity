import numpy as np

pc_input = np.array([ 40.30910863,   8.56577551,  54.46320516,  60.39623699,
         7.25475803,   4.65158945,  24.0168705 ,  68.55214697,
        69.95924573,  15.59284008,  17.31696879,  22.58139698,
        37.97602155,  23.98546057,  15.84086424,  64.47562428,
        64.68739303,  25.09177234,  68.35058661,  20.31693454,
        31.41407668,   7.74210555,   9.88657606,  13.63142911,
        49.15850831,  30.58308429,  28.70665896,  31.94941439,
         8.84467812,  55.1633896 ,  58.55935082,   0.37767247,
        19.88306825,  39.77105362,  66.51084712,  66.87295357,
        62.33949719,  47.45150092,  26.96712105,  46.75531802,
        29.20449607,  17.91013346,  13.92973487,  42.06037351,
         2.83635417,  58.57577831,  24.29099014,  21.64608291,
        38.06935796,  37.76095876,  60.17714093,  67.97861171,
        64.5394034 ,  14.40865039,  42.46893421,   9.8684628 ,
        32.20983921,   7.14781606,   9.81968821,   7.74585164]).astype(np.float64)
        
#global variables.. 
# ***************
# modify this value for changing the delta
DELTA_VAR = 50.0

DELTA = DELTA_VAR/100.0
HALFDELTA = DELTA/2.0
NUMBITS = 2

def getPointCloud_from_quantizedValues(pc_encoded, resolution_in  = HALFDELTA):
    pc_value = (pc_encoded *resolution_in) #+ np.array([x_in[0],y_in[0],z_in[0]])
    return(pc_value)

def getQuantizedValues_from_pointCloud(pc, resolution_in = DELTA):
    pc_quant_value = np.around((pc) / resolution_in).astype(np.int32)
    # pc_quant_value = ((pc - np.array([x_in[0],y_in[0],z_in[0]]))/resolution_in).astype(np.int32)
    return(pc_quant_value)

#checks if the quantized value is even or odd
def get_oddflag(pc_row):
    o_flag = [] 
    # print('pc input', pc_row)
    for i in range(len(pc_row)):
        number_dec = int(pc_row[i])
        # print('num dec', number_dec)
        if (number_dec % 2 == 0): #even
            o_flag.append(0)
        else:
            o_flag.append(1) #odd 
    return o_flag

def qim_dummy_encoded_pc(length_in):
    pc_row_count = 0
    cbook = []
    message_count = 0
    while pc_row_count < length_in:    
        encode_message = '{0:02b}'.format(message_count%4)
        encode_message = np.array(list(encode_message), dtype= int)
        cbook.append(encode_message)
        # this variable gives some flexibility on starting the encoding at different number other than 0        
        message_count += 1 
        pc_row_count += 1
    return np.array(cbook)

def qim_decode(pc, resolution = HALFDELTA, numbits=NUMBITS):
    # We can check if each coordinate is even or odd.. while encoding 
    final_code = []
    cloud_row_read = []
    cloud_row_read = getQuantizedValues_from_pointCloud(pc, resolution)

    for j in range (cloud_row_read.shape[0]):
        row_odd_flags = []       
        row_odd_flags = get_oddflag(cloud_row_read[j])
        final_code.append(row_odd_flags[:numbits])
    # print('******decoded quantized values', cloud_row_read.shape, cloud_row_read)
    
    return final_code, cloud_row_read
    
def qim_quantize_twobit(pc_in, message_in):
    
    #converts the input message to embed into list of bits
    encode_message = '{0:02b}'.format(message_in)
    encode_message = np.array(list(encode_message), dtype= int)
    
    #while pc_row_count < len(pc_in):
    cloud_to_compare = np.array([])
    cloud_row_halfdelta = []
    changed_indices = np.array([])
    # cloud_row_clean = ((pc - np.array([x[0],y[0],z[0]])) / resolution).astype(np.int32)
    quantized_values_row = getQuantizedValues_from_pointCloud(pc_in)
    # print('clean', cloud_row_clean)
    cloud_row_halfdelta =  2*quantized_values_row
    # print('input cloud- Half Delta', cloud_row_halfdelta)
    cloud_to_compare = np.array(get_oddflag(cloud_row_halfdelta))
    # print('input oddflag', cloud_to_compare)
    changed_indices = np.where(cloud_to_compare[:2] != encode_message[:2])

    if(len(changed_indices)):
        for i in range(len(changed_indices[0])):
                cloud_row_halfdelta[changed_indices[0][i]] = cloud_row_halfdelta[changed_indices[0][i]] + 1
    
    return cloud_row_halfdelta
    
def get_tamperedindices_twobits(decoded_codebook, encoded_codebook):
    error_counter = 0
    suspect_indices = []
    #length of the encoded and decoded code books should be equal
    for index in range(len(decoded_codebook)):
        #changed_indices = np.array([])
        changed_indices = np.where(decoded_codebook[index] != decoded_codebook[index])
        if(changed_indices[0].shape[0]):
            suspect_indices.append(index)    
            for i in range(len(changed_indices[0])):
                # increment the error counter
                error_counter += 1
                
    suspect_indices = np.array(suspect_indices)
    error_rate =  error_counter/(2.0*len(decoded_codebook))
    return suspect_indices, error_rate
    
def qim_quantize_twobits(pc_message_in):
    
    pc_row_count = 0
    message = 0
    quant_encoded = []
    while pc_row_count < len(pc_message_in):
        pc_in_row = pc_message_in[pc_row_count, :]
        # the quantize funciton takes two arguments:
        #1. the data elements to encode as two element array        
        #2. message to be encoded in the form of a number(then converts into bit stream)
        quant_two_bit_value = qim_quantize_twobit(pc_in_row, message)
        quant_encoded.append(quant_two_bit_value)
        message += 1
        message %= 4          
        # print('row# and code book', pc_row_count, code_book)
        pc_row_count +=  1
    if(pc_row_count > len(pc_message_in)):
        print('something wrong.. exceeded length of pc')
    return  quant_encoded

def QIM_encode_twobit(sensor_data, message):
  modified_x, modified_y = 0,0
  quant_two_bit_value = qim_quantize_twobit(sensor_data, message)
#   print('embedded quantized value x={},y={}'. format(quant_two_bit_value[0], quant_two_bit_value[1]) )
  qim_encoded_pointcloud = getPointCloud_from_quantizedValues( quant_two_bit_value)
  modified_x, modified_y = qim_encoded_pointcloud[0],qim_encoded_pointcloud[1]
  return (modified_x, modified_y)

if __name__ == '__main__':

#    resolution_delta = 5.0/100.0 
#    resolution_halfdelta = resolution_delta/2.0
    
    voxel_halfdelta = qim_quantize_twobits( np.copy(pc_input.reshape(-1,2)))
    
    voxel_halfdelta_npy = np.array([voxel_halfdelta]).reshape(-1,2)
    print('quant encoded shape', voxel_halfdelta_npy.shape, voxel_halfdelta_npy)
    
    qim_encoded_pointcloud = getPointCloud_from_quantizedValues(  np.copy(voxel_halfdelta_npy))        
    
    decoded_CB, decoded_quantized_values = qim_decode( np.copy(qim_encoded_pointcloud))
    
    print('decoded codebook', decoded_CB)
    decoded_codebook = np.array([decoded_CB]).reshape(-1,NUMBITS)
    
    encoded_cb = qim_dummy_encoded_pc(len(pc_input.reshape(-1,NUMBITS)))
    print('encoded cb', encoded_cb)
    # uncomment below to test if the tamper index finder is working
    #encoded_cb[2] = [1,1]
    #encoded_cb[4] = [0,1]
    
    tampered_indices, b_errorRate = get_tamperedindices_twobits(decoded_codebook, encoded_cb)
    print('tampered indices', tampered_indices)