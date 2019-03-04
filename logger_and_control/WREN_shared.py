
'''Define variables used for management of phidget data'''
# Hub board
hub_vi = [178866]*8
# Thermocouple input
tc_i = [118257]
# DC motor 1 and 2
dcm1_vi = [146593]*2
dcm2_vi = [146812]*2
# Stepper motor controller
stm_di = [267223]*4
# Stepper serial
stp_serial = 267223
# weighpad
weigh = [999999]
# speed probe
revcount = [888888]
# Create full lists for logging (concatenate all previous lists, repeat those that have more than one kind of input)
ch_map = hub_vi*2 + tc_i + dcm1_vi*2 + dcm2_vi*2 + stm_di + weigh + revcount

ch_states = [False]*len(ch_map)
ch_data = [0.0]*len(ch_map)

states_spots_key = {
    "0": 1,
    "1": 2,
    "2": 3,
    "3": 4,
    "16": 5,
    "4": 6,
    "5": 7,
    "6": 8,
    "7": 9,
    "8": 10,
    "stp": "stp",
    "dc1": "dc1",
    "dc2": "dc2",
    "wfe": "wfe",
    "n" : "n"
}

''' Stepper states'''
stepper_position = 0.0
stepper_connected = False
stepper_moving = False

''' DC motor 1 states'''
DC1_pos_feedback = 0.0
DC1_pos_dem = 0.0

''' DC motor 2 states'''
DC2_pos_feedback = 0.0
DC2_pos_dem = 0.0

''' Logger data channels configuration 
    structure is [serial, channel, label] '''

logger_config = [[178866, 0, 'TAMB'],
                 [178866, 1, 'PAMB'],
                 [178866, 2, 'PTOT'],
                 [178866, 3, 'DP'],
                 [118257, 0, 'TTOT'],
                 [999999, 0, 'WFE'],
                 [888888, 0, 'N'],
                 [178866, 4, 'FN1'],
                 [178866, 5, 'FN2'],
                 [178866, 6, 'FN3'],
                 [178866, 7, 'FN4']]


ch_labels = ['TAMB', 'PAMB', 'PTOT', 'DP', 'TTOT','WFE', 'N', 'FN1', 'FN2', 'FN3', 'FN4']

mapped_channels = [178866, 178867, 178868, 178869, 118257, 'wfe','n', 178870, 178871, 178872, 178873]
mapped_ch_data = [0.0]*len(mapped_channels)

''' Postprocessing function definition'''

def applyLets(datain):
    dataout = [0.0]*len(datain)
    dataout[0] = (datain[0] * 5 * 44.444) - 61.111
    dataout[1] = (datain[1] * 250 + 10) * 0.145038
    dataout[2] = (datain[2] * 250 + 10) * 0.145038
    dataout[3] = (datain[3] * 5 * 1.61) - 4.0277
    dataout[4:] = datain[4:]
    return dataout

''' Weighpad connection flag'''
WFE_IsConnected = False

''' Revcount connection flag'''
N_IsConnected = False