select
    oc.t_ocompra,
    oc.aa_ocompra,
    oc.n_ocompra,
    prd.aa_precepcion, 
    prd.t_precepcion,
    prd.n_precepcion,   
    oc.o_ente,
    oc.c_unid_ejec,
    prd.fh_autorizacion,
    prd.fh_alta,
    oc.aa_ocompra_orig,
    oc.t_ocompra_orig,
    oc.n_ocompra_orig,
    prd.e_formulario   
from slu.torden_compra OC join slu.tparte_recepcion PRD on prd.aa_ocompra= oc.aa_ocompra and prd.n_ocompra=oc.n_ocompra and prd.t_ocompra= oc.t_ocompra
join slu.dorden_compra_ren ren on oc.aa_ocompra=ren.aa_ocompra and oc.t_ocompra= ren.t_ocompra and oc.n_ocompra=ren.n_ocompra
where oc.c_procedimiento=220
and ren.c_clase in (990010,560000,790000)
group by
   oc.t_ocompra,
    oc.aa_ocompra,
    oc.n_ocompra,
    prd.aa_precepcion, 
    prd.t_precepcion,
    prd.n_precepcion,   
    oc.o_ente,
    oc.c_unid_ejec,
    prd.fh_autorizacion,
    prd.fh_alta,
    oc.aa_ocompra_orig,
    oc.t_ocompra_orig,
    oc.n_ocompra_orig,
    prd.e_formulario  ;