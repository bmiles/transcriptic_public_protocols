from autoprotocol.util import make_dottable_dict
from autoprotocol import Unit

def glycerol_storage(protocol,params):
    params = make_dottable_dict(params)
    for g in params["samples"]:
        container = protocol.ref(g["label"], cont_type="micro-1.5", storage = "cold_80")
        protocol.provision("rs17rrhqpsxyh2", container.well(0), "500:microliter")
        protocol.transfer(g["sample"], container.well(0), "500:microliter", mix_after = True)

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(glycerol_storage, 'GlycerolStorage')
