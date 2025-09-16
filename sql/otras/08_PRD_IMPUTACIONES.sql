
select 
    oc.aa_oca_original,
    oc.n_oca_original,
    pr.aa_precepcion,
    pr.t_precepcion,
    pr.n_precepcion, 
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
from slu.torden_compra OC join slu.trecepcion_provision PR on pr.aa_ocompra= oc.aa_ocompra and pr.n_ocompra=oc.n_ocompra and pr.t_ocompra= oc.t_ocompra
join slu.tparte_recepcion prd on pr.n_precepcion = prd.n_precepcion and pr.aa_precepcion = prd.aa_precepcion 
join slu.dparte_recepcion_ffi ffi on prd.n_precepcion = ffi.n_precepcion and prd.aa_precepcion = ffi.aa_precepcion 
JOIN slu.dorden_compra_ren REN  on ren.aa_ocompra= oc.aa_ocompra AND  ren.t_ocompra= oc.t_ocompra and ren.n_ocompra=oc.n_ocompra
where c_clase in (990010,560000,790000)  and  oc.t_ocompra='SPR' -- AND oc.aa_ocompra=2021 AND ROWNUM <= 300000
-- where oc.aa_ocompra=2021 and oc.t_ocompra='SPR' and oc.n_ocompra=48897
GROUP BY  oc.aa_oca_original,
    oc.n_oca_original,
    pr.aa_precepcion,
    pr.t_precepcion,
    pr.n_precepcion, 
    ffi.c_numcred,
    ffi.c_juris,
    ffi.c_sjuris,
    ffi.c_entidad,
    ffi.c_inciso,
    ffi.c_pprincipal,
    ffi.c_pparcial,
    ffi.c_ubica_geo,
    ffi.i_total,
    prd.e_formulario; 