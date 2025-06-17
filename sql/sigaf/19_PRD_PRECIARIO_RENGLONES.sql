select
    oc.aa_ocompra,
    oc.t_ocompra,
    oc.n_ocompra,
    prd.aa_precepcion, 
    prd.t_precepcion,
    prd.n_precepcion,   
    oc.o_ente,
    oc.aa_ocompra_orig,
    oc.t_ocompra_orig,
    oc.n_ocompra_orig,
    oc.c_unid_ejec,
    prd.fh_autorizacion,
    prd.f_desde,
    prd.f_hasta,
    ren.n_renglon_pliego,
    ren.xl_descripcion,
    ren.k_rdefinitiva,
    ren.i_unitario,
    ren.k_rdefinitiva*ren.i_unitario as "Total renglon",
    prd.e_formulario
from slu.torden_compra OC join slu.tparte_recepcion PRD on prd.aa_ocompra= oc.aa_ocompra and prd.n_ocompra=oc.n_ocompra and prd.t_ocompra= oc.t_ocompra
join slu.dparte_recepcion_ren ren on prd.aa_precepcion=ren.aa_precepcion and prd.n_precepcion= ren.n_precepcion
where oc.c_procedimiento=220
and ren.c_clase in (990010,560000,790000)
 --and  oc.aa_ocompra=2023
--and    oc.t_ocompra='OCC'
 --and    oc.n_ocompra=69538
 --and oc.aa_ocompra_orig=2021
--and oc.t_ocompra_orig='OCA'
 --and oc.n_ocompra_orig=65638
group by   
    oc.aa_ocompra,
    oc.t_ocompra,
    oc.n_ocompra,
    prd.aa_precepcion, 
    prd.t_precepcion,
    prd.n_precepcion,   
    oc.o_ente,
    oc.aa_ocompra_orig,
    oc.t_ocompra_orig,
    oc.n_ocompra_orig,
    oc.c_unid_ejec,
    prd.fh_autorizacion,
    prd.f_desde,
    prd.f_hasta,
    ren.n_renglon_pliego,
    ren.xl_descripcion,
    ren.k_rdefinitiva,
    ren.i_unitario,
    prd.e_formulario;
