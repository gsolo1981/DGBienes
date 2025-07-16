SELECT DISTINCT 
f.AA_OCOMPRA , f.N_OCOMPRA
,f.AA_FACTURA ,f.T_FACTURA ,f.O_FACTURA ,f.E_FACTURA
,dv.AA_DEVENGADO ,dv.T_DEVENGADO ,dv.o_DEVENGADO ,dv.N_DEVENGADO 
,op.AA_FORMULARIO ,op.T_FORMULARIO ,op.O_FORMULARIO 
,op.FH_ALTA /* Fecha Ingreso*/ ,op.F_AUTORIZACION ,op.F_VENCIMIENTO_FACTURA /*Fecha Venc OP*/
,op.E_FIRMA ,op.U_FIRMA ,op.F_FIRMA 
, NULL importe_op  /*Importe OP*/
,op.IA_PAGADO  
,pg.C_MEDIOPAGO ,pg.FH_PAGO ,pg.E_PAGO 
, NULL importe_neto /*Importe Neto*/
FROM slu.TFACTURA_GS f,
slu.TDEVENGADO dv,
slu.DDEV_RPR_REDET_REN dv_rpr_rd,
slu.dform_item dop,
slu.TFORMULARIO op,
slu.tpago pg 
WHERE f.AA_CERTIFICADO = dv.AA_DEVENGADO AND f.T_FORM_MEDICION = dv.T_DEVENGADO AND f.O_CERTIFICADO = N_DEVENGADO 
AND dv_rpr_rd.O_DEVENGADO = dv.O_DEVENGADO
AND f.aa_factura = dop.aa_cpte_generador AND f.t_factura = dop.t_cpte_generador AND f.o_factura = dop.n_cpte_generador
AND op.AA_FORMULARIO = dop.AA_FORMULARIO AND op.T_FORMULARIO = dop.T_FORMULARIO AND op.O_FORMULARIO = dop.O_FORMULARIO 
AND  op.AA_FORMULARIO = pg.aa_op(+) AND op.t_FORMULARIO = pg.T_OP(+) AND op.O_FORMULARIO = pg.O_OP(+)
AND f.T_FACTURA = 'FRP' AND dv_rpr_rd.c_clase IN (990010,560000,790000);