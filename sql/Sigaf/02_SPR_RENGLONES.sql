select 
    oc.aa_oca_original,
    oc.n_oca_original,
    oc.o_ente,
    oc.aa_ocompra,
    oc.t_ocompra,
    oc.n_ocompra,
    oc.c_unid_ejec,
    oc.fh_estado,
    ren.n_renglon_pliego,
    ren.k_adjudicada,
    ren.i_unitario,
    ren.k_adjudicada * ren.i_unitario as "Total renglon",
    oc.e_ocompra,
    oc.fh_alta,
    oc.fh_autorizacion,
    ren.xl_descripcion
from slu.dorden_compra_ren REN join slu.torden_compra OC on ren.aa_ocompra= oc.aa_ocompra AND  ren.t_ocompra= oc.t_ocompra and ren.n_ocompra=oc.n_ocompra
and ren.n_ocompra=oc.n_ocompra and ren.t_ocompra= oc.t_ocompra
where c_clase in (990010,560000,790000)  --AND oc.aa_oca_original=2021
;
