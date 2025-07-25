SELECT
	dv.AA_OCOMPRA,
	dv.N_OCOMPRA,
	dv.AA_DEVENGADO,
	dv.T_DEVENGADO,
	dv.N_DEVENGADO,
	imp.C_NUMCRED,
	dv.C_JURIS ,
	dv.C_SJURIS ,
	dv.C_ENTIDAD,
	imp.C_PROGRAMA,
	imp.C_INCISO,
	imp.C_PPRINCIPAL,
	imp.C_PPARCIAL,
	imp.C_PSPARCIAL,
	imp.C_UBICA_GEO,
	dv_ffi.I_DEVENGADO,
	dv.E_DEVENGADO
FROM slu.DDEVENGADO_FFI dv_ffi,
slu.TDEVENGADO dv,
slu.timput_cred imp,
slu.DDEV_RPR_REDET_REN dv_rpr_rd
WHERE	dv.T_DEVENGADO = 'DRP'
AND dv_ffi.O_DEVENGADO = dv.O_DEVENGADO
AND imp.AA_EJERVG = dv_ffi.AA_EJERVG
AND imp.C_NUMCRED = dv_ffi.C_NUMCRED
AND dv.O_DEVENGADO = dv_rpr_rd.O_DEVENGADO
AND dv_rpr_rd.c_clase IN (990010, 560000, 790000)
GROUP BY dv.AA_OCOMPRA,dv.N_OCOMPRA,dv.AA_DEVENGADO,dv.T_DEVENGADO,dv.N_DEVENGADO,imp.C_NUMCRED,
	dv.C_JURIS,dv.C_SJURIS,dv.C_ENTIDAD,imp.C_PROGRAMA,imp.C_INCISO,imp.C_PPRINCIPAL,imp.C_PPARCIAL,
	imp.C_PSPARCIAL,imp.C_UBICA_GEO,dv_ffi.I_DEVENGADO,dv.E_DEVENGADO;