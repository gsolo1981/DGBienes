select 
    oc.aa_ocompra,
    oc.t_ocompra,
    oc.n_ocompra,
    oc.e_ocompra,
    oc.fh_estado,
    oc.o_ente,
    oc.aa_ocompra_orig,
    oc.t_ocompra_orig,
    oc.n_ocompra_orig,
    oc.c_procedimiento,
    ffi.c_numcred,
    ffi.c_juris,
    ffi.c_sjuris,
    ffi.c_entidad,
    ffi.c_inciso,
    ffi.c_pprincipal,
    ffi.c_pparcial,
    ffi.c_ubica_geo,
    ffi.i_total
from slu.torden_compra oc join slu.dorden_compra_ren ren on oc.aa_ocompra=ren.aa_ocompra and oc.t_ocompra= ren.t_ocompra and oc.n_ocompra=ren.n_ocompra
join slu.dorden_compra_ffi ffi on oc.aa_ocompra=ffi.aa_ocompra and oc.t_ocompra= ffi.t_ocompra and oc.n_ocompra=ffi.n_ocompra
where oc.c_procedimiento=220
and ren.c_clase in (990010,560000,790000)
and oc.c_procedimiento=220
group by  
oc.aa_ocompra,
    oc.t_ocompra,
    oc.n_ocompra,
    oc.e_ocompra,
    oc.fh_estado,
    oc.o_ente,
    oc.aa_ocompra_orig,
    oc.t_ocompra_orig,
    oc.n_ocompra_orig,
    oc.c_procedimiento,
    ffi.c_numcred,
    ffi.c_juris,
    ffi.c_sjuris,
    ffi.c_entidad,
    ffi.c_inciso,
    ffi.c_pprincipal,
    ffi.c_pparcial,
    ffi.c_ubica_geo,
    ffi.i_total;