from platolocorestapi.src.wrapper.methods.cast import Cast
from platolocorestapi.src.wrapper.methods.seg import Seg
from platolocorestapi.src.wrapper.methods.flps import Flps
from platolocorestapi.src.wrapper.methods.simple import Simple
from platolocorestapi.src.wrapper.methods.gbsc import Gbsc


class MethodBuilder:
    def create(self, name, params):
        name = name.lower()
        print("name: {0}".format(name))
        print(params)
        if name == "cast":
            cast = Cast()
            cast.set_params(params)
            return cast
        elif name == "seg_strict":
            seg = Seg()
            seg.change_params_set("SEG_strict")
            return seg
        elif name == "seg_intermediate":
            seg = Seg()
            seg.change_params_set("SEG_intermediate")
            return seg
        elif name == "seg":
            seg = Seg()
            seg.set_params(params)
            return seg
        elif name == "flps":
            flps = Flps()
            flps.set_params(params)
            return flps
        elif name == "flps_strict":
            flps = Flps()
            flps.change_params_set("fLPS_strict")
            return flps
        elif name == "simple":
            simple = Simple()
            simple.set_params(params)
            return simple
        elif name == "gbsc":
            gbsc = Gbsc()
            gbsc.set_params(params)
            return gbsc
        else:
            raise NotImplementedError("method not found: {0}".format(name))

