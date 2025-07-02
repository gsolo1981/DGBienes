  -- REVISAR
SELECT
	pr.aa_ocompra,
	pr.t_ocompra,
	pr.n_ocompra,
	fg.aa_factura,
	fg.t_factura,
	fg.o_factura,
	pr.aa_precepcion,
	pr.t_precepcion,
	pr.n_precepcion,
	tf.aa_formulario,
	tf.t_formulario,
	tf.o_formulario,
	tf.f_emision,
	tf.f_autorizacion,
	tf.e_firma,
	tf.u_firma,
	tf.f_firma,
	tf.f_vencimiento_factura,
	tf.ia_devengado AS importe_op,
	tf.ia_pagado AS importe_pago,
	p.fh_pago,
	p.c_mediopago,
	p.e_pago,
	--SUM(drf.i_total) importe_prd,
	SUM(ffi.I_DEVENGADO) importe_factura,
	p.ia_pago AS neto
FROM
	SLU.TPARTE_RECEPCION pr,
	 SLU.TORDEN_COMPRA OC,
	SLU.DPARTE_RECEPCION_REN drr,
	SLU.DPARTE_RECEPCION_FFI drf,
	SLU.TFACTURA_GS fg,
	SLU.DFACGS_ITEM fdi,
	SLU.DFACGS_FFI ffi,
	SLU.TFORMULARIO tf,
	SLU.DFORM_ITEM df,
	SLU.TPAGO p,
	SLU.DPAGO dp
	--JOIN PRD CON ITEM E IMPUTACION
WHERE
pr.aa_ocompra = oc.aa_ocompra
  AND pr.t_ocompra =oc.t_ocompra
  AND pr.n_ocompra =oc.n_ocompra
	AND pr.aa_precepcion = drr.aa_precepcion
	AND pr.t_precepcion = drr.t_precepcion
	AND pr.n_precepcion = drr.n_precepcion
	AND pr.aa_precepcion = drf.aa_precepcion
	AND pr.t_precepcion = drf.t_precepcion
	AND pr.n_precepcion = drf.n_precepcion
	--JOIN FACTURA PRD X ITEM
	AND drr.aa_precepcion = fdi.aa_precepcion
	AND drr.t_precepcion = fdi.t_precepcion
	AND drr.n_precepcion = fdi.n_precepcion
	AND drr.O_ITEM = fdi.O_ITEM_PRD
	--join faturas
	AND fg.aa_factura = fdi.aa_factura
	AND fg.o_factura = fdi.o_factura
	AND fg.aa_factura = ffi.aa_factura
	AND fg.o_factura = ffi.o_factura
	--JOIN FACTURA OP
	AND ffi.aa_factura = df.aa_cpte_generador
	AND fg.t_factura = df.t_cpte_generador
	AND ffi.o_factura = df.n_cpte_generador
	AND ffi.O_FFI = df.O_IT_CPTE_GENERADOR
	--JOIN OP DETALLE-CABECERA
	AND tf.aa_formulario = df.aa_formulario
	AND tf.t_formulario = df.t_formulario
	AND tf.o_formulario = df.o_formulario
	--JOIN PAGO OP
	AND tf.aa_formulario = p.aa_op
	AND tf.t_formulario = p.t_op
	AND tf.o_formulario = p.o_op
	--JOIN pago con dpago
	AND p.aa_pago = dp.aa_pago
	AND p.o_pago = dp.o_pago
	--JOIN PAGO OP
	AND dp.o_item = df.O_ITEM
	AND dp.C_NUMCRED = df.C_NUMCRED
	--filtros
	AND NVL(drf.i_total,0)>0
	AND NVL(ffi.i_devengado,0)>0
  AND oc.c_procedimiento=220
	AND p.t_pago = 'B' --SOLO PAGOS A BENEFICIARIO
	AND pr.e_formulario = 'A' --FILTRO ESTADO PRD
	AND fg.e_factura = 'Y' --FILTRO ESTADO DE FACTGURA
	AND tf.e_formulario = 'C' --FILTRO ESTADO DE OP
	AND p.e_pago NOT IN ('X', 'I') --FILTRO ESTADO DE PAGO
	AND drr.c_clase IN (990010, 560000, 790000)--FILTRO BIENES
	--
GROUP BY
	pr.aa_ocompra,
	pr.t_ocompra,
	pr.n_ocompra,
	fg.aa_factura,
	fg.t_factura,
	fg.o_factura,
	pr.aa_precepcion,
	pr.t_precepcion,
	pr.n_precepcion,
	tf.aa_formulario,
	tf.t_formulario,
	tf.o_formulario,
	tf.f_emision,
	tf.f_autorizacion,
	tf.e_firma,
	tf.u_firma,
	tf.f_firma,
	tf.f_vencimiento_factura,
	tf.ia_devengado,
	tf.ia_pagado,
	p.ia_pago,
	p.fh_pago,
	p.c_mediopago,
	p.e_pago;