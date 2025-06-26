select 
    oc.aa_oca_original,
    oc.n_oca_original,
    pr.aa_rprovision,
    pr.t_rprovision,
    pr.n_rprovision,
    pr.c_unid_ejec,
    pr.f_desde,
    pr.f_hasta,
    pr.fh_autorizacion,
    ffi.c_numcred,
    ffi.c_juris,
    ffi.c_sjuris,
    ffi.c_entidad,
    ffi.c_ubica_geo,
    ffi.i_total,
    pr.e_rprovision,
    ffi.c_inciso,
    ffi.c_pprincipal,
    ffi.c_pparcial  
from slu.drecepcion_provision_ffi ffi join slu.trecepcion_provision PR on ffi.aa_rprovision = pr.aa_rprovision and ffi.t_rprovision=pr.t_rprovision and ffi.n_rprovision = pr.n_rprovision
INNER join slu.torden_compra OC on pr.aa_ocompra= oc.aa_ocompra and pr.t_ocompra = oc.t_ocompra and pr.n_ocompra= oc.n_ocompra
INNER JOIN slu.dorden_compra_ren REN  on ren.aa_ocompra= oc.aa_ocompra AND  ren.t_ocompra= oc.t_ocompra and ren.n_ocompra=oc.n_ocompra
--where oc.aa_oca_original = 2021 and oc.n_oca_original=65638 AND c_clase in (990010,560000,790000)
WHERE  c_clase in (990010,560000,790000)  --AND oc.aa_oca_original = 2021 and ROWNUM <= 200000
GROUP BY     oc.aa_oca_original,
    oc.n_oca_original,
    pr.aa_rprovision,
    pr.t_rprovision,
    pr.n_rprovision,
    pr.c_unid_ejec,
    pr.f_desde,
    pr.f_hasta,
    pr.fh_autorizacion,
    ffi.c_numcred,
    ffi.c_juris,
    ffi.c_sjuris,
    ffi.c_entidad,
    ffi.c_ubica_geo,
    ffi.i_total,
    pr.e_rprovision,
    ffi.c_inciso,
    ffi.c_pprincipal,
    ffi.c_pparcial;
