from autoprotocol.util import make_dottable_dict

def spread_n_pick(protocol,params):
    params = make_dottable_dict(params)

    liquid_culture_plate = protocol.ref("liquid_culture_plate", cont_type="96-deep", storage = "cold_4")
    solid_culture_plate = params.solid_culture_plate

    samples = sum([[s] * 1 for s in params.samples], [])

    solid_culture_plate_wells = solid_culture_plate.wells_from("A1", len(samples))

    for innoculant, dest in zip(params.samples, solid_culture_plate_wells):
        protocol.spread(innoculant, dest, params.sample_volume)

    protocol.cover(solid_culture_plate)

    protocol.incubate(solid_culture_plate, "warm_37", params.plate_growth_time, shaking = False)

    protocol.dispense(liquid_culture_plate, params.media, [{'column': i, 'volume': params.media_volume} for i in xrange(len(samples))])

    if len(params.antibiotic) > 0:
        protocol.distribute(params.antibiotic.set_volume("1500:microliter"), liquid_culture_plate.wells_from(0, len(samples) * 8, columnwise = True), params.antibiotic_volume)

    protocol.uncover(solid_culture_plate)
    protocol.image_plate(solid_culture_plate, "top", dataref="culture_plate_image_01")

    count = 0
    while count < len(samples):
        protocol.autopick(solid_culture_plate.well(count), liquid_culture_plate.wells_from(count,8,columnwise = True), min_count = params.minimum_picked_colonies)
        count += 1

    protocol.cover(solid_culture_plate)
    protocol.cover(liquid_culture_plate)

    protocol.incubate(liquid_culture_plate,"warm_37", params.liq_growth_time, shaking=True)

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(spread_n_pick, 'SpreadNPick')
