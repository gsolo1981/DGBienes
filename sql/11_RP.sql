SELECT rd.AA_OCOMPRA , rd.N_OCOMPRA
, rd.N_ORDEN_REDET , rd.E_REDETERMINACION , rd.F_APLICACION , rd_ren.N_RENGLON_PLIEGO
, rd_ren.I_UNITARIO_ANT , rd_ren.N_PORC_REDET , rd_ren.I_UNITARIO_REDET , I_UNITARIO_REDET - nvl (rd_ren.i_unitario_ant,rd_ren.i_unitario_oc) Diferencia_Redet
,rd.FH_ALTA ,rd.FH_AUTORIZACION ,rd.O_REDETERMINACION 
FROM slu.tredeterminacion rd
JOIN slu.DREDETERMINACION_REN rd_ren ON rd.O_REDETERMINACION = rd_ren.O_REDETERMINACION 
where rd_ren.c_clase in (990010,560000,790000);