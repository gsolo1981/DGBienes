-- no agregue tabla de ren al script original    
    
select 
    oc.aa_oca_original,
    oc.n_oca_original,
    pr.aa_rprovision,
    pr.t_rprovision,
    pr.n_rprovision,
    pr.o_ente,
    pr.c_juris,
    pr.c_sjuris,
    pr.c_entidad,
    pr.c_unid_ejec,
    pr.f_desde,
    pr.f_hasta,
    pr.fh_autorizacion,
    ren.n_renglon_pliego,
    ren.k_rdefinitiva,
    ren.i_unitario,
    ren.k_rdefinitiva * ren.i_unitario  as "Total renglon",
    pr.e_rprovision
from slu.drecepcion_provision_ren REN 
join slu.trecepcion_provision PR on ren.aa_rprovision = pr.aa_rprovision and ren.t_rprovision=pr.t_rprovision and ren.n_rprovision = pr.n_rprovision
join slu.torden_compra OC on pr.aa_ocompra= oc.aa_ocompra and pr.t_ocompra = oc.t_ocompra and pr.n_ocompra= oc.n_ocompra
--where pr.aa_rprovision=2021 and pr.t_rprovision='RPR' and pr.n_rprovision='66630' AND c_clase in (990010,560000,790000)
WHERE  pr.t_rprovision='RPR' and  c_clase in (990010,560000,790000) --AND pr.aa_rprovision=2021 and ROWNUM <= 200
;
