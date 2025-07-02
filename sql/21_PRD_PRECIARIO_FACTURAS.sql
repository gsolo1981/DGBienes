  -- REVISAR
  select
    oc.aa_ocompra,
    oc.n_ocompra,
    prd.t_precepcion,
    prd.n_precepcion,
    prd.aa_precepcion,
    fact.aa_factura,
    fact.o_factura,
    fact.e_factura,
    fact.t_fact_proveedor,
    fact.n_suc_fact_proveedor,
    fact.n_fact_proveedor,
    fact.f_factura,
    fact.fhu_actualiz,
    factitem.n_renglon_pliego,
    factitem.k_facturada,
    factitem.i_unitario ,
    factitem.k_facturada*factitem.i_unitario as "Total renglon"   
from slu.torden_compra OC join slu.tparte_recepcion PRD on prd.aa_ocompra= oc.aa_ocompra and prd.n_ocompra=oc.n_ocompra and prd.t_ocompra= oc.t_ocompra
join slu.dparte_recepcion_ren ren on prd.aa_precepcion=ren.aa_precepcion and prd.n_precepcion= ren.n_precepcion
join slu.dfacgs_ffi factdet on factdet.n_precepcion = prd.n_precepcion and factdet.aa_precepcion = prd.aa_precepcion 
join slu.tfactura_gs fact on fact.o_factura= factdet.o_factura and fact.aa_factura=factdet.aa_factura 
join slu.dfacgs_item factitem on factitem.o_factura= fact.o_factura and factitem.o_factura= fact.o_factura
where oc.c_procedimiento=220
and ren.c_clase in (990010,560000,790000)
group by
  oc.aa_ocompra,
    oc.n_ocompra,
    prd.t_precepcion,
    prd.n_precepcion,
    prd.aa_precepcion,
    fact.aa_factura,
    fact.o_factura,
    fact.e_factura,
    fact.t_fact_proveedor,
    fact.n_suc_fact_proveedor,
    fact.n_fact_proveedor,
    fact.f_factura,
    fact.fhu_actualiz,
    factitem.n_renglon_pliego,
    factitem.k_facturada,
    factitem.i_unitario;