--30 segundos con filtros
    select
    oc.aa_oca_original,
    oc.n_oca_original,
    pr.t_precepcion,
    pr.n_precepcion,
    pr.aa_precepcion,
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
    factitem.i_unitario
    
from slu.torden_compra OC join slu.trecepcion_provision PR on pr.aa_ocompra= oc.aa_ocompra and pr.n_ocompra=oc.n_ocompra and pr.t_ocompra= oc.t_ocompra
join slu.dfacgs_ffi factdet on factdet.n_precepcion = pr.n_precepcion and factdet.aa_precepcion = pr.aa_precepcion 
join slu.tfactura_gs fact on fact.o_factura= factdet.o_factura and fact.aa_factura=factdet.aa_factura 
join slu.dfacgs_item factitem on factitem.o_factura= fact.o_factura and factitem.o_factura= fact.o_factura
where  oc.t_ocompra='SPR'
AND c_clase in (990010,560000,790000) --AND oc.aa_ocompra=2021 and oc.n_ocompra=48897  and ROWNUM <= 20000
GROUP BY oc.aa_oca_original,
    oc.n_oca_original,
    pr.t_precepcion,
    pr.n_precepcion,
    pr.aa_precepcion,
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
