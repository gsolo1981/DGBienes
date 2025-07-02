select
    oc.aa_oca_original,
    oc.n_oca_original,
    pr.aa_rprovision,
    pr.t_rprovision,
    pr.n_rprovision,
    oc.o_ente,
    oc.c_juris,
    oc.c_sjuris,
    oc.c_entidad,
    oc.c_unid_ejec,
    pr.f_desde,
    pr.f_hasta,
    pr.fh_autorizacion,
    pr.t_ocompra,
    pr.aa_ocompra,
    pr.n_ocompra,
    pr.t_precepcion,
    pr.aa_precepcion,
    pr.n_precepcion,
    pr.e_rprovision,
    pr.fh_alta
from slu.torden_compra OC 
INNER JOIN slu.dorden_compra_ren REN  on ren.aa_ocompra= oc.aa_ocompra AND  ren.t_ocompra= oc.t_ocompra and ren.n_ocompra=oc.n_ocompra
INNER join slu.trecepcion_provision PR on pr.aa_ocompra= oc.aa_ocompra and pr.n_ocompra=oc.n_ocompra and pr.t_ocompra= oc.t_ocompra
--where oc.aa_ocompra=2021 and oc.t_ocompra='SPR' and oc.n_ocompra=48897 
--where c_clase in (990010,560000,790000) AND oc.aa_ocompra=2021 and oc.t_ocompra='SPR' and oc.n_ocompra=48897
where c_clase in (990010,560000,790000)  and oc.t_ocompra='SPR' --AND oc.aa_ocompra=2021 AND ROWNUM <= 300000
GROUP BY
oc.aa_oca_original,
    oc.n_oca_original,
    pr.aa_rprovision,
    pr.t_rprovision,
    pr.n_rprovision,
    oc.o_ente,
    oc.c_juris,
    oc.c_sjuris,
    oc.c_entidad,
    oc.c_unid_ejec,
    pr.f_desde,
    pr.f_hasta,
    pr.fh_autorizacion,
    pr.t_ocompra,
    pr.aa_ocompra,
    pr.n_ocompra,
    pr.t_precepcion,
    pr.aa_precepcion,
    pr.n_precepcion,
    pr.e_rprovision,
    pr.fh_alta;
