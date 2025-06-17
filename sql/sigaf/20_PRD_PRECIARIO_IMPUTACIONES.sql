select 
    oc.aa_ocompra,
    oc.n_ocompra,
    prd.aa_precepcion,
    prd.t_precepcion,
    prd.n_precepcion, 
    oc.o_ente,
    oc.t_ocompra_orig,
    oc.aa_ocompra_orig,
    oc.n_ocompra_orig,
    prd.c_unid_ejec,    
    prd.fh_autorizacion,
    prd.f_desde,
    prd.f_hasta,
    ffi.c_numcred,
    ffi.c_juris,
    ffi.c_sjuris,
    ffi.c_entidad,
    ffi.c_inciso,
    ffi.c_pprincipal,
    ffi.c_pparcial,
    ffi.c_ubica_geo,
    ffi.i_total,
    prd.e_formulario   
from slu.torden_compra OC join slu.tparte_recepcion PRD on prd.aa_ocompra= oc.aa_ocompra and prd.n_ocompra=oc.n_ocompra and prd.t_ocompra= oc.t_ocompra
JOIN slu.dorden_compra_ren REN  on ren.aa_ocompra= oc.aa_ocompra AND  ren.t_ocompra= oc.t_ocompra and ren.n_ocompra=oc.n_ocompra

join slu.dparte_recepcion_ffi ffi on prd.n_precepcion = ffi.n_precepcion and prd.aa_precepcion = ffi.aa_precepcion 
where oc.c_procedimiento=220 and ren.c_clase in (990010,560000,790000)and oc.t_ocompra_orig='OCA'

group by
    oc.aa_ocompra,
    oc.n_ocompra,
    prd.aa_precepcion,
    prd.t_precepcion,
    prd.n_precepcion, 
    oc.o_ente,
    oc.t_ocompra_orig,
    oc.aa_ocompra_orig,
    oc.n_ocompra_orig,
    prd.c_unid_ejec,    
    prd.fh_autorizacion,
    prd.f_desde,
    prd.f_hasta,
    ffi.c_numcred,
    ffi.c_juris,
    ffi.c_sjuris,
    ffi.c_entidad,
    ffi.c_inciso,
    ffi.c_pprincipal,
    ffi.c_pparcial,
    ffi.c_ubica_geo,
    ffi.i_total,
    prd.e_formulario ;