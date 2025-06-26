-- Sin tabla adicional, 1 minuto con filtro
    
    select
    oc.aa_oca_original,
    oc.n_oca_original,
    oc.o_ente,
    oc.i_total_adjudicacion,
    pr.aa_precepcion,
    pr.t_precepcion,
    pr.n_precepcion,    
    pr.aa_rprovision,
    pr.t_rprovision,
    pr.n_rprovision,
    pr.t_precepcion,
    prd.e_formulario,
    pr.f_desde,
    pr.f_hasta,
    prd.c_unid_ejec, 
    renprd.n_renglon_pliego,
    renprd.k_rdefinitiva,
    renprd.i_unitario,
    renprd.k_rdefinitiva * renprd.i_unitario,
    prd.fh_alta,
    prd.fh_autorizacion,
    prd.fh_firma
from slu.torden_compra OC join slu.trecepcion_provision PR on pr.aa_ocompra= oc.aa_ocompra and pr.n_ocompra=oc.n_ocompra and pr.t_ocompra= oc.t_ocompra
join slu.tparte_recepcion prd on pr.n_precepcion = prd.n_precepcion and pr.aa_precepcion = prd.aa_precepcion 
join slu.dparte_recepcion_ren renprd on prd.n_precepcion = renprd.n_precepcion and prd.aa_precepcion = renprd.aa_precepcion 
where c_clase in (990010,560000,790000)  and oc.t_ocompra='SPR' --AND oc.aa_ocompra=2021 AND ROWNUM <= 2000
;
