SELECT
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
factitem.i_unitario,
pr.aa_rprovision,pr.t_rprovision , pr.n_rprovision

from slu.torden_compra OC
join slu.trecepcion_provision PR on pr.aa_ocompra= oc.aa_ocompra and pr.n_ocompra=oc.n_ocompra and pr.t_ocompra= oc.t_ocompra
join slu.dparte_recepcion_ren drr ON drr.AA_PRECEPCION = pr.AA_PRECEPCION AND drr.N_PRECEPCION = pr.n_precepcion AND drr.AA_RPROVISION = pr.AA_RPROVISION AND drr.N_RPROVISION = pr.N_RPROVISION
join slu.dfacgs_item factitem on factitem.AA_PRECEPCION = drr.AA_PRECEPCION AND factitem.N_PRECEPCION = drr.n_precepcion AND factitem.O_ITEM_PRD = drr.O_ITEM
join slu.tfactura_gs fact on fact.o_factura= factitem.o_factura and fact.aa_factura=factitem.aa_factura

where oc.t_ocompra='SPR' AND drr.c_clase in (990010,560000,790000);