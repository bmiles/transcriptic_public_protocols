from autoprotocol.util import make_dottable_dict
from autoprotocol import Unit

def serial_dilute_plus(protocol,params):
    params = make_dottable_dict(params)
    dilution_plate = protocol.ref("dilution plate", cont_type="96-flat", storage = params.storage_condition)
    # total_well_volume is 150 so that a factor of 2 dilution we don't exceed the well volume.
    total_well_volume = Unit(150,"microliter")
    num_of_dilutions = 8
    wells = dilution_plate.wells_from(0, num_of_dilutions * len(params.samples ), columnwise = True)

    protocol.dispense(dilution_plate, params.diluent, [{'column': i, 'volume': total_well_volume - (total_well_volume/params.samples[i]["dilution_factor"])} for i in xrange(0,len(params.samples))])
    for g in params["samples"]:
        protocol.transfer(g["sample"], dilution_plate.well(params.samples.index(g)), total_well_volume/g["dilution_factor"], mix_after = True)
        g["column"] = params.samples.index(g)

    for g in params["samples"]:
        well = g["column"] * 8
        while well < g["column"] * 8 + 7:
            protocol.transfer(wells[well], wells[well+1], total_well_volume/g["dilution_factor"], mix_after = True)
            well += 1

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(serial_dilute_plus, 'SerialDilutePlus')
