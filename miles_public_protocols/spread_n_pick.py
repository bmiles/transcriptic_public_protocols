from autoprotocol.util import make_dottable_dict
import datetime
import provision_plate_util as ppu

def spread_n_pick(protocol,params):
    params = make_dottable_dict(params)
    today = datetime.date.today()
    liquid_culture_plate = protocol.ref("liquid_culture_plate_%s" % today, cont_type="96-deep", storage = "cold_4")
    solid_culture_plate = ppu.ref_kit_container(protocol, "colony_plate_%s" % today, "6-flat", ppu.return_agar_plates(6)["noAB"], store="warm_37")
    samples = sum([[s] * 1 for s in params.samples], [])
    solid_culture_plate_wells = solid_culture_plate.wells_from("A1", len(samples))
    antibiotic_id = params.antibiotic_id

    for innoculant, dest in zip(params.samples, solid_culture_plate_wells):
        protocol.spread(innoculant, dest, params.sample_volume)

    protocol.cover(solid_culture_plate)

    protocol.incubate(solid_culture_plate, "warm_37", params.plate_growth_time, shaking = False)

    protocol.dispense(liquid_culture_plate, params.media, [{'column': i, 'volume': params.media_volume} for i in xrange(len(samples))])

    if len(params.antibiotic_id) > 0:
        protocol.provision(antibiotic_id, liquid_culture_plate.wells_from(0, len(samples) * 8, columnwise = True), params.antibiotic_volume)
    if len(params.carbon_source) > 0:
        protocol.distribute(params.carbon_source.set_volume("1500:microliter"), liquid_culture_plate.wells_from(0, len(samples) * 8, columnwise = True), params.carbon_source_volume)

    protocol.uncover(solid_culture_plate)
    protocol.image_plate(solid_culture_plate, "top", dataref="culture_plate_image__%s" % today)

    count = 0
    while count < len(samples):
        protocol.autopick(solid_culture_plate.well(count), liquid_culture_plate.wells_from(count,8,columnwise = True), min_count = params.minimum_picked_colonies, dataref="autopick_%d" % count)
        count += 1

    protocol.cover(solid_culture_plate)
    protocol.cover(liquid_culture_plate)

    protocol.incubate(liquid_culture_plate,"warm_37", params.liq_growth_time, shaking=True)

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(spread_n_pick, 'SpreadNPick')
