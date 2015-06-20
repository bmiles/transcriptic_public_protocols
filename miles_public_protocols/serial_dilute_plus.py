from autoprotocol.util import make_dottable_dict
import math

def serial_dilute_plus(protocol,params):
    params = make_dottable_dict(params)

    dilution_plate = protocol.ref("dilution plate", cont_type="96-flat", storage = params.storage_condition)

    # total_well_volume is 150 so that a factor of 2 dilution we don't exceed the well volume.
    total_well_volume = "150:microliter"
    num_of_dilutions = params.num_of_dilutions
    dilution_factor = params.dilution_factor
    transfer_volume = "%d:microliter" % (150/dilution_factor)
    media_volume = "%d:microliter" % (150 - (150/dilution_factor))

    wells = dilution_plate.wells_from(0, num_of_dilutions, columnwise = True)

    protocol.dispense(dilution_plate, params.diluent, [{'column': i, 'volume': media_volume} for i in xrange(int(math.ceil(num_of_dilutions/8.0)))])

    protocol.transfer(params.sample, wells[0], transfer_volume, mix_after = True)

    count = 0
    while count < len(wells) -1 :
        protocol.transfer(wells[count], wells[count+1], transfer_volume, mix_after = True)
        count += 1

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(serial_dilute_plus, 'SerialDilutePlus')
