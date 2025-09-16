select 
    oc.aa_ocompra,
    oc.t_ocompra,
    oc.n_ocompra,
    oc.e_ocompra,
    oc.o_ente,
    oc.fh_estado,
    --o_ente_1,
    oc.aa_ocompra_orig,
    oc.t_ocompra_orig,
    oc.n_ocompra_orig,
    oc.c_procedimiento,
    ren.n_renglon_pliego,
    ren.xl_descripcion,
    ren.k_adjudicada,
    ren.i_unitario,
    ren.k_adjudicada * ren.i_unitario as "Total renglon",
    oc.fh_alta,
    oc.fh_autorizacion
from slu.torden_compra oc join slu.dorden_compra_ren ren on oc.aa_ocompra=ren.aa_ocompra and oc.t_ocompra= ren.t_ocompra and oc.n_ocompra=ren.n_ocompra
where oc.c_procedimiento=220 AND
 oc.t_ocompra = 'OCC' AND ren.c_clase in (990010,560000,790000)  ;