ALTER TABLE DGBIDB.[dbo].[02_SPR_RENGLONES] ADD xl_descripcion VARCHAR(2000) NULL;
ALTER TABLE DGBIDB.[dbo].[05_RPR_RENGLONES] ADD xl_descripcion VARCHAR(2000) NULL;
ALTER TABLE DGBIDB.[dbo].[07_PRD_RENGLONES] ADD xl_descripcion VARCHAR(2000) NULL;
ALTER TABLE DGBIDB.[dbo].[12_DRP_RENGLONES] ADD xl_descripcion VARCHAR(2000) NULL;


ALTER VIEW VW_SPR_RENGLONES AS
SELECT aa_oca_original, n_oca_original, o_ente, aa_ocompra, t_ocompra, n_ocompra, c_unid_ejec, fh_estado, fh_alta, fh_autorizacion, n_renglon_pliego, k_adjudicada, i_unitario, total_renglon, e_ocompra,xl_descripcion
FROM DGBIDB.dbo.[02_SPR_RENGLONES];

ALTER VIEW VW_RPR_RENGLONESAS as
SELECT aa_oca_original, n_oca_original, aa_rprovision, t_rprovision, n_rprovision, o_ente, c_juris, c_sjuris, c_entidad, c_unid_ejec, f_desde, f_hasta, fh_autorizacion, n_renglon_pliego, k_rdefinitiva, i_unitario, total_renglon, e_rprovision,xl_descripcion
FROM DGBIDB.dbo.[05_RPR_RENGLONES];


ALTER VIEW VW_PRD_RENGLONES as
SELECT aa_oca_original, n_oca_original, o_ente, i_total_adjudicacion, aa_precepcion, t_precepcion, n_precepcion, aa_rprovision, t_rprovision, n_rprovision, e_formulario, f_desde, f_hasta, c_unid_ejec, n_renglon_pliego, k_rdefinitiva, i_unitario, total_renglon, fh_alta, fh_autorizacion, fh_firma,xl_descripcion
FROM DGBIDB.dbo.[07_PRD_RENGLONES];

ALTER VIEW VW_DRP_RENGLONES as
SELECT aa_ocompra, n_ocompra, aa_devengado, t_devengado, n_devengado, o_ente, t_rprovision, aa_rprovision, n_rprovision, n_orden_redet, o_redeterminacion, n_renglon_pliego, k_rdefinitiva, i_variacion, e_devengado, fh_alta, f_autorizacion, fh_firma, id, fecha_registro, row_hash,xl_descripcion
FROM DGBIDB.dbo.[12_DRP_RENGLONES];

delete from DGBIDB.dbo.[02_SPR_RENGLONES]
delete from DGBIDB.dbo.[05_RPR_RENGLONES]
delete from DGBIDB.dbo.[07_PRD_RENGLONES]
delete from DGBIDB.dbo.[12_DRP_RENGLONES]