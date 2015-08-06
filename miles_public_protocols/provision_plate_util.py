from autoprotocol.container import Container
from autoprotocol.protocol import Ref


def ref_kit_container(protocol, name, container, kit_id, discard=True, store=None):
    '''
        Still in use to allow booking of agar plates on the fly
    '''
    kit_item = Container(None, protocol.container_type(container))
    if store:
        protocol.refs[name] = Ref(name, {"reserve": kit_id, "store": {"where": store}}, kit_item)
    else:
        protocol.refs[name] = Ref(name, {"reserve": kit_id, "discard": discard}, kit_item)
    return(kit_item)


def return_agar_plates(wells):
    '''
        Dicts of all plates available that can be purchased.
    '''
    if wells == 6:
        plates = {"50_ug/ml_Kanamycin": "ki17rs7j799zc2",
                  "100_ug/ml_Ampicillin": "ki17sbb845ssx9",
                  "100_ug/mL_Spectinomycin": "ki17sbb9r7jf98",
                  "noAB": "ki17reefwqq3sq"}
    elif wells == 1:
        plates = {"50_ug/ml_Kanamycin": "ki17t8j7kkzc4g",
                  "100_ug/ml_Ampicillin": "ki17sbb845ssx9",
                  "100_ug/mL_Spectinomycin": "ki17t8jcebshtr",
                  "noAB": "ki17t8jejbea4z"}
    else:
        raise ValueError("Wells has to be an integer, either 1 or 6")
    return(plates)

# example call: myplate = protocol.ref_kit_container(protocol, 'my_agar_plate', 'flat-6', return_agar_plates(6)['50_ug/ml_Kanamycin'], store='warm_37')
