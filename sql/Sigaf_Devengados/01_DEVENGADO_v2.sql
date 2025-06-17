SELECT t.o_ente
     , slu.spap_ente.numero_cuit(t.o_ente) n_cuit
     , slu.spap_ente.descripcion_completa(t.o_ente) xl_ente
     , t.aa_precepcion
     , t.t_precepcion
     , t.n_precepcion
     , t.c_juris
     , t.c_unid_ejec
     , t.fh_imputacion
     , TO_CHAR(drr.f_hasta,'MM/YYYY') AS periodo_dev
     , drr.n_renglon_pliego renglon
     , drr.i_unitario*drr.k_rdefinitiva total_dev 
     , c.c_programa
     , c.c_sprograma
     , c.c_proyecto
     , c.c_actividad
     , c.c_obra
     , c.c_fuefin
     , c.c_inciso||c.c_pprincipal||c.c_pparcial as o_gasto
     , d.i_total total_imp_presup
  FROM slu.tparte_recepcion t
     , slu.dparte_recepcion_ffi d
     , slu.timput_cred c
     , slu.dparte_recepcion_ren drr
 WHERE t.aa_precepcion = d.aa_precepcion
   AND t.t_precepcion  = d.t_precepcion
   AND t.n_precepcion  = d.n_precepcion
   AND drr.aa_precepcion = t.aa_precepcion
   AND drr.t_precepcion  = t.t_precepcion
   AND drr.n_precepcion  = t.n_precepcion
   AND d.aa_precepcion_ffi = c.aa_ejervg
   AND d.c_numcred = c.c_numcred
   AND t.aa_precepcion >= 2023
   AND t.e_formulario = 'A'
   AND t.t_ocompra = 'CON'
   AND c.c_juris = 50 
   AND c.c_inciso = 3
   AND c.c_pprincipal = 4
   AND c.c_pparcial = 7
   AND NVL(drr.k_rdefinitiva,0) > 0
   AND NVL(d.i_total,0) > 0
 ORDER BY t.aa_precepcion, t.n_precepcion, drr.n_renglon_pliego;
