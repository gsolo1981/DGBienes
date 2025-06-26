-- DROP SCHEMA dbo;

CREATE SCHEMA dbo;
-- DGBIDB.dbo.[01_RELACION_BAC_SIGAF] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[01_RELACION_BAC_SIGAF];

CREATE TABLE DGBIDB.dbo.[01_RELACION_BAC_SIGAF] (
	id_oc_bac varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL
);


-- DGBIDB.dbo.[02_SPR_RENGLONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[02_SPR_RENGLONES];

CREATE TABLE DGBIDB.dbo.[02_SPR_RENGLONES] (
	aa_oca_original varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_oca_original varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_estado datetime NOT NULL,
	fh_alta datetime NOT NULL,
	fh_autorizacion datetime NULL,
	n_renglon_pliego varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	k_adjudicada decimal(15,2) NOT NULL,
	i_unitario decimal(15,2) NOT NULL,
	total_renglon decimal(15,2) NULL,
	e_ocompra char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[Total renglon] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[03_SPR_IMPUTACIONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[03_SPR_IMPUTACIONES];

CREATE TABLE DGBIDB.dbo.[03_SPR_IMPUTACIONES] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	aa_oca_original varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	n_oca_original varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	fh_estado datetime NOT NULL,
	e_ocompra char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	c_numcred varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	c_juris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	c_sjuris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	c_entidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	c_inciso varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	c_pprincipal varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	c_pparcial varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	c_ubica_geo varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	i_total decimal(15,2) NOT NULL
);


-- DGBIDB.dbo.[04_RPR_SPR_PRD] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[04_RPR_SPR_PRD];

CREATE TABLE DGBIDB.dbo.[04_RPR_SPR_PRD] (
	aa_oca_original varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_oca_original varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_rprovision varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_rprovision varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_rprovision varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_juris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_sjuris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_entidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_desde date NULL,
	f_hasta date NULL,
	fh_autorizacion datetime NULL,
	fh_alta datetime NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_precepcion varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_precepcion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_rprovision char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[05_RPR_RENGLONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[05_RPR_RENGLONES];

CREATE TABLE DGBIDB.dbo.[05_RPR_RENGLONES] (
	aa_oca_original varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_oca_original varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_rprovision varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_rprovision varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_rprovision varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_juris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_sjuris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_entidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_desde date NULL,
	f_hasta date NULL,
	fh_autorizacion datetime NULL,
	n_renglon_pliego varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	k_rdefinitiva decimal(15,6) NULL,
	i_unitario decimal(15,2) NULL,
	total_renglon decimal(15,2) NULL,
	e_rprovision char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Total renglon] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[06_RPR_IMPUTACIONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[06_RPR_IMPUTACIONES];

CREATE TABLE DGBIDB.dbo.[06_RPR_IMPUTACIONES] (
	aa_oca_original varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_oca_original varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_rprovision varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_rprovision varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_rprovision varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_desde date NULL,
	f_hasta date NULL,
	fh_autorizacion datetime NULL,
	c_numcred varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_juris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_sjuris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_entidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_ubica_geo varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_inciso varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pprincipal varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pparcial varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	i_total decimal(15,2) NULL,
	e_rprovision char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[07_PRD_RENGLONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[07_PRD_RENGLONES];

CREATE TABLE DGBIDB.dbo.[07_PRD_RENGLONES] (
	aa_oca_original varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_oca_original varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	i_total_adjudicacion decimal(15,2) NULL,
	aa_precepcion varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_precepcion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_rprovision varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_rprovision varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_rprovision varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_formulario char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_desde varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_hasta varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_renglon_pliego varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	k_rdefinitiva decimal(15,6) NULL,
	i_unitario decimal(15,2) NULL,
	k_rdefinitiva_x_i_unitario decimal(15,2) NULL,
	fh_alta varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_autorizacion varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_firma varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion_1 varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[RENPRD.K_RDEFINITIVA*RENPRD.I_UNITARIO] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[08_PRD_IMPUTACIONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[08_PRD_IMPUTACIONES];

CREATE TABLE DGBIDB.dbo.[08_PRD_IMPUTACIONES] (
	aa_oca_original varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_oca_original varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_precepcion varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_precepcion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_numcred varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_juris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_sjuris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_entidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_inciso varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pprincipal varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pparcial varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_ubica_geo varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	i_total decimal(15,2) NULL,
	e_formulario char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[09_PRD_FACTURAS] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[09_PRD_FACTURAS];

CREATE TABLE DGBIDB.dbo.[09_PRD_FACTURAS] (
	aa_oca_original varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_oca_original varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_precepcion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_precepcion varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_factura varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_factura varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_factura_1 char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_factura_2 char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_fact_proveedor varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_suc_fact_proveedor varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_fact_proveedor varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_factura datetime NULL,
	fhu_actualiz datetime NULL,
	n_renglon_pliego varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	k_facturada decimal(15,6) NULL,
	i_unitario decimal(15,2) NULL,
	e_factura varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[10_FACTURAS_OP_PAGOS] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[10_FACTURAS_OP_PAGOS];

CREATE TABLE DGBIDB.dbo.[10_FACTURAS_OP_PAGOS] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_factura varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_factura varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_factura varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_precepcion varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_precepcion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_formulario varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_formulario varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_formulario varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_emision datetime NULL,
	f_autorizacion datetime NULL,
	f_vencimiento_factura datetime NULL,
	fh_pago datetime NULL,
	e_firma char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_firma varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_firma datetime NULL,
	importe_op decimal(15,2) NULL,
	importe_pago decimal(15,2) NULL,
	importe_factura decimal(15,2) NULL,
	neto decimal(15,2) NULL,
	c_mediopago varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_pago char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[11_RP] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[11_RP];

CREATE TABLE DGBIDB.dbo.[11_RP] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_orden_redet varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_redeterminacion char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_aplicacion varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_redeterminacion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_renglon_pliego varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	i_unitario_ant decimal(15,2) NULL,
	n_porc_redet decimal(8,2) NULL,
	i_unitario_redet decimal(15,2) NULL,
	diferencia_redet decimal(15,2) NULL,
	fh_alta varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_autorizacion varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[12_DRP_RENGLONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[12_DRP_RENGLONES];

CREATE TABLE DGBIDB.dbo.[12_DRP_RENGLONES] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_devengado varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_devengado varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_devengado varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_rprovision varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_rprovision varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_rprovision varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_orden_redet varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_redeterminacion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_renglon_pliego varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	k_rdefinitiva decimal(15,6) NULL,
	i_variacion decimal(15,6) NULL,
	e_devengado char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_alta varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_autorizacion varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_firma varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[13_DRP_IMPUTACIONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[13_DRP_IMPUTACIONES];

CREATE TABLE DGBIDB.dbo.[13_DRP_IMPUTACIONES] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_devengado varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_devengado varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_devengado varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_numcred varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_juris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_sjuris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_entidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_programa varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_inciso varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pprincipal varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pparcial varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_psparcial varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_ubica_geo varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	i_devengado decimal(15,2) NULL,
	e_devengado char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[14_DRP_FACTURAS] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[14_DRP_FACTURAS];

CREATE TABLE DGBIDB.dbo.[14_DRP_FACTURAS] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_certificado varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_form_medicion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_certificado varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_factura varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_factura varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_factura varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_factura char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_fact_proveedor varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_suc_fact_proveedor varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_fact_proveedor varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_factura datetime NULL,
	fh_alta datetime NULL,
	f_autorizacion datetime NULL,
	c_numcred varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_juris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_sjuris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_entidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_programa varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_inciso varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pprincipal varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pparcial varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_psparcial varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_ubica_geo varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	i_devengado decimal(15,2) NULL,
	i_pagado decimal(15,2) NULL
);


-- DGBIDB.dbo.[15_DRP_FACTURAS_PAGOS] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[15_DRP_FACTURAS_PAGOS];

CREATE TABLE DGBIDB.dbo.[15_DRP_FACTURAS_PAGOS] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_factura varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_factura varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_factura varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_factura char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_devengado varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_devengado varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_devengado varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_devengado varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_formulario varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_formulario varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_formulario varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_alta datetime NULL,
	f_autorizacion datetime NULL,
	f_vencimiento_factura datetime NULL,
	f_firma datetime NULL,
	fh_pago datetime NULL,
	e_firma char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_firma varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	importe_op decimal(15,2) NULL,
	ia_pagado decimal(15,2) NULL,
	importe_neto decimal(15,2) NULL,
	c_mediopago varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_pago char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[16_PRECIARIO] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[16_PRECIARIO];

CREATE TABLE DGBIDB.dbo.[16_PRECIARIO] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_ocompra char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_estado datetime NULL,
	aa_ocompra_orig varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra_orig varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra_orig varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_procedimiento varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_renglon_pliego varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	xl_descripcion varchar(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	k_adjudicada decimal(15,6) NULL,
	i_unitario decimal(15,2) NULL,
	total_renglon decimal(15,2) NULL,
	fh_alta datetime NULL,
	fh_autorizacion datetime NULL,
	[Total renglon] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[17_PRECIARIO_IMPUTACIONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[17_PRECIARIO_IMPUTACIONES];

CREATE TABLE DGBIDB.dbo.[17_PRECIARIO_IMPUTACIONES] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_ocompra char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_estado datetime NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_ocompra_orig varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra_orig varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra_orig varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_procedimiento varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_numcred varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_juris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_sjuris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_entidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_inciso varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pprincipal varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pparcial varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_ubica_geo varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	i_total decimal(15,2) NULL
);


-- DGBIDB.dbo.[18_PRD_PRECIARIO] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[18_PRD_PRECIARIO];

CREATE TABLE DGBIDB.dbo.[18_PRD_PRECIARIO] (
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_precepcion varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_precepcion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_autorizacion datetime NULL,
	fh_alta datetime NULL,
	aa_ocompra_orig varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra_orig varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra_orig varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_formulario char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[19_PRD_PRECIARIO_RENGLONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[19_PRD_PRECIARIO_RENGLONES];

CREATE TABLE DGBIDB.dbo.[19_PRD_PRECIARIO_RENGLONES] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_precepcion varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_precepcion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_ocompra_orig varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra_orig varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra_orig varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_autorizacion datetime NULL,
	f_desde datetime NULL,
	f_hasta datetime NULL,
	n_renglon_pliego varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	xl_descripcion varchar(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	k_rdefinitiva decimal(15,6) NULL,
	i_unitario decimal(15,2) NULL,
	total_renglon decimal(15,2) NULL,
	e_formulario char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Total renglon] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[20_PRD_PRECIARIO_IMPUTACIONES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[20_PRD_PRECIARIO_IMPUTACIONES];

CREATE TABLE DGBIDB.dbo.[20_PRD_PRECIARIO_IMPUTACIONES] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_precepcion varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_precepcion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_ocompra_orig varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra_orig varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra_orig varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_autorizacion datetime NULL,
	f_desde datetime NULL,
	f_hasta datetime NULL,
	c_numcred varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_juris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_sjuris varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_entidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_inciso varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pprincipal varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_pparcial varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_ubica_geo varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	i_total decimal(15,2) NULL,
	e_formulario char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_ente int NULL
);


-- DGBIDB.dbo.[21_PRD_PRECIARIO_FACTURAS] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[21_PRD_PRECIARIO_FACTURAS];

CREATE TABLE DGBIDB.dbo.[21_PRD_PRECIARIO_FACTURAS] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_precepcion varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_precepcion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_factura varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_factura varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_factura varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_ocompra_orig varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra_orig varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra_orig varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fh_autorizacion datetime NULL,
	f_desde datetime NULL,
	f_hasta datetime NULL,
	n_renglon_pliego varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	xl_descripcion varchar(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	k_facturada decimal(15,6) NULL,
	i_unitario decimal(15,2) NULL,
	total_renglon decimal(15,2) NULL,
	t_fact_proveedor varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_suc_fact_proveedor varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_fact_proveedor varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_factura datetime NULL,
	e_formulario char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_factura varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fhu_actualiz varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Total renglon] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[22_PAGOS_PRECIARIO] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[22_PAGOS_PRECIARIO];

CREATE TABLE DGBIDB.dbo.[22_PAGOS_PRECIARIO] (
	aa_ocompra varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_ocompra varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_ocompra varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_factura varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_factura varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_factura varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_precepcion varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_precepcion varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	n_precepcion varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	aa_formulario varchar(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	t_formulario varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	o_formulario varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	f_emision datetime NULL,
	f_autorizacion datetime NULL,
	f_firma datetime NULL,
	f_vencimiento_factura datetime NULL,
	fh_pago datetime NULL,
	e_firma char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_firma varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	importe_op decimal(15,2) NULL,
	importe_pago decimal(15,2) NULL,
	importe_factura decimal(15,2) NULL,
	neto decimal(15,2) NULL,
	c_mediopago varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	e_pago char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[23_UNIDADES_EJECUTORAS] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[23_UNIDADES_EJECUTORAS];

CREATE TABLE DGBIDB.dbo.[23_UNIDADES_EJECUTORAS] (
	c_unid_ejec varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	xl_unid_ejec varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.[24_PERIODOS_FISCALES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[24_PERIODOS_FISCALES];

CREATE TABLE DGBIDB.dbo.[24_PERIODOS_FISCALES] (
	año int NOT NULL
);


-- DGBIDB.dbo.[25_ENTES] definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.[25_ENTES];

CREATE TABLE DGBIDB.dbo.[25_ENTES] (
	o_ente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	denom_ente varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nro_oc_sigaf varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.Bienes_01_BENEFICIARIOS definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.Bienes_01_BENEFICIARIOS;

CREATE TABLE DGBIDB.dbo.Bienes_01_BENEFICIARIOS (
	documento_tipo varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	documento varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	nombre varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	email varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	emailadicional varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	telefono varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_persona varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	fechanacimiento datetime NULL,
	sexo char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	activo char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	tipo_domicilio varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	calle varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	piso varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dpto varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	localidad varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	codigo_postal varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL
);


-- DGBIDB.dbo.Bienes_02_CARTERAS definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.Bienes_02_CARTERAS;

CREATE TABLE DGBIDB.dbo.Bienes_02_CARTERAS (
	barrio varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	ley int NULL,
	identificacion varchar(64) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	circunscripcion int NULL,
	seccion int NULL,
	manzana int NULL,
	parcela int NULL,
	division varchar(64) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_unidad varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nrounidad int NULL,
	piso varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	depto varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	telefono varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	partidaunidad varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	digitoverificador varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipoplano varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	valuacionfiscal varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nueva varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	mtstotales varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	mtscubiertos varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	habilitado varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.Bienes_03_CONTRATOS definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.Bienes_03_CONTRATOS;

CREATE TABLE DGBIDB.dbo.Bienes_03_CONTRATOS (
	nro int NOT NULL,
	expediente varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fechafirma datetime NOT NULL,
	tipo_contrato varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	tipo_calculo varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	tipo_unidad varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	identificacion varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	descripcion varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	nrounidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	vigente char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	nombre varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	documento varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	desde datetime NOT NULL,
	hasta datetime NOT NULL,
	principal char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL
);


-- DGBIDB.dbo.Bienes_04_PLAN_DE_PAGOS definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.Bienes_04_PLAN_DE_PAGOS;

CREATE TABLE DGBIDB.dbo.Bienes_04_PLAN_DE_PAGOS (
	tipo varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	objetivo_prestacion varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	nombre varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	documento varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	email varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	emailadicional varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_persona varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	calle varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	carpeta varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	identificacion varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	sub_division varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	nrounidad varchar(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	tipo_contrato varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	tipo_calculo varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	resp_adjudicatatio varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	documento1 varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	fecha_creacion datetime NOT NULL,
	nro_expediente varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	observaciones varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	numero varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	vencimiento datetime NULL,
	fechabui datetime NULL,
	total decimal(12,2) NULL,
	observacion varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	estado varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fechapago datetime NULL,
	resp_cumplimiento varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	cuil varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	legajo varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL
);


-- DGBIDB.dbo.Concesiones_01_BENEFICIARIOS definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.Concesiones_01_BENEFICIARIOS;

CREATE TABLE DGBIDB.dbo.Concesiones_01_BENEFICIARIOS (
	documento_tipo varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	documento varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nombre varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	email varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	emailadicional varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_persona varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fechanacimiento varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sexo char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	telefono varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	activo char(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_domicilio varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	calle varchar(300) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	piso varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dpto varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	localidad varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	codigo_postal varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.Concesiones_02_CARTERAS definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.Concesiones_02_CARTERAS;

CREATE TABLE DGBIDB.dbo.Concesiones_02_CARTERAS (
	barrio varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	ley varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	identificacion varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	circunscripcion varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	seccion varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	manzana varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	parcela varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	division varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_unidad varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nrounidad varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	partidaunidad varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	digitoverificador varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipoplano varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	valuacionfiscal varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nueva varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	mtstotales varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	mtscubiertos varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	habilitado varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.Concesiones_03_CONTRATOS definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.Concesiones_03_CONTRATOS;

CREATE TABLE DGBIDB.dbo.Concesiones_03_CONTRATOS (
	nro varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	expediente varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fechafirma varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_contrato varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_calculo varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_unidad varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	identificacion varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	descripcion varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nrounidad varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	vigente varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nombre varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	documento varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	desde varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	hasta varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	principal varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- DGBIDB.dbo.Concesiones_04_PLAN_DE_PAGOS definition

-- Drop table

-- DROP TABLE DGBIDB.dbo.Concesiones_04_PLAN_DE_PAGOS;

CREATE TABLE DGBIDB.dbo.Concesiones_04_PLAN_DE_PAGOS (
	tipo varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	objetivo_prestacion varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nombre varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	documento varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	email varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	emailadicional varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_persona varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	calle varchar(300) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	carpeta varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	identificacion varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sub_division varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nrounidad varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_contrato varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	tipo_calculo varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	resp_adjudicatatio varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	documento1 varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fecha_creacion varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	nro_expediente varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	observaciones varchar(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	numero varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	vencimiento varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fechabui varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	total varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	observacion varchar(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	estado varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fechapago varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	resp_cumplimiento varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	cuil varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	legajo varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);


-- dbo.VW_Bienes_Beneficiarios source

ALTER VIEW VW_Bienes_Beneficiarios AS
select * from DGBIDB.dbo.Bienes_01_BENEFICIARIOS;


-- dbo.VW_Bienes_Carteras source

ALTER VIEW VW_Bienes_Carteras AS
select * from DGBIDB.dbo.Bienes_02_CARTERAS;


-- dbo.VW_Bienes_Contratos source

ALTER VIEW VW_Bienes_Contratos AS
select * from DGBIDB.dbo.Bienes_03_CONTRATOS ;


-- dbo.VW_Bienes_Plan_de_pagos source

ALTER VIEW VW_Bienes_Plan_de_pagos AS
select * from DGBIDB.dbo.Bienes_04_PLAN_DE_PAGOS ;


-- dbo.VW_Concesiones_Beneficiarios source

ALTER VIEW VW_Concesiones_Beneficiarios as
select * from DGBIDB.dbo.Concesiones_01_BENEFICIARIOS;


-- dbo.VW_Concesiones_Carteras source

ALTER VIEW VW_Concesiones_Carteras as
select * from DGBIDB.dbo.Concesiones_02_CARTERAS;


-- dbo.VW_Concesiones_Contratos source

ALTER VIEW VW_Concesiones_Contratos as
select * from DGBIDB.dbo.Concesiones_03_CONTRATOS;


-- dbo.VW_Concesiones_Plan_de_pagos source

ALTER VIEW VW_Concesiones_Plan_de_pagos as
select * from DGBIDB.dbo.Concesiones_04_PLAN_DE_PAGOS;


-- dbo.VW_DRP_FACTURAS source

ALTER VIEW VW_DRP_FACTURAS as
select * from DGBIDB.dbo.[14_DRP_FACTURAS];


-- dbo.VW_DRP_FACTURAS_PAGOS source

ALTER VIEW VW_DRP_FACTURAS_PAGOS as
select * from DGBIDB.dbo.[15_DRP_FACTURAS_PAGOS];


-- dbo.VW_DRP_IMPUTACIONES source

ALTER VIEW VW_DRP_IMPUTACIONES as
select * from DGBIDB.dbo.[13_DRP_IMPUTACIONES];


-- dbo.VW_DRP_RENGLONES source

ALTER VIEW VW_DRP_RENGLONES as
select * from DGBIDB.dbo.[12_DRP_RENGLONES];


-- dbo.VW_FACTURAS_OP_PAGOS source

ALTER VIEW VW_FACTURAS_OP_PAGOS as
select * from DGBIDB.dbo.[10_FACTURAS_OP_PAGOS];


-- dbo.VW_PAGOS_PRECIARIO source

ALTER VIEW VW_PAGOS_PRECIARIO as
select * from DGBIDB.dbo.[22_PAGOS_PRECIARIO];


-- dbo.VW_PERIODOS_FISCALES source

ALTER VIEW VW_PERIODOS_FISCALES as
select * from DGBIDB.dbo.[24_PERIODOS_FISCALES];


-- dbo.VW_PRD_FACTURAS source

ALTER VIEW VW_PRD_FACTURAS as
select * from DGBIDB.dbo.[09_PRD_FACTURAS];


-- dbo.VW_PRD_IMPUTACIONES source

ALTER VIEW VW_PRD_IMPUTACIONES as
select * from DGBIDB.dbo.[08_PRD_IMPUTACIONES];


-- dbo.VW_PRD_PRECIARIO source

ALTER VIEW VW_PRD_PRECIARIO as
select * from DGBIDB.dbo.[18_PRD_PRECIARIO];


-- dbo.VW_PRD_PRECIARIO_FACTURAS source

ALTER VIEW VW_PRD_PRECIARIO_FACTURAS as
select * from DGBIDB.dbo.[21_PRD_PRECIARIO_FACTURAS];


-- dbo.VW_PRD_PRECIARIO_IMPUTACIONES source

ALTER VIEW VW_PRD_PRECIARIO_IMPUTACIONES as
select * from DGBIDB.dbo.[20_PRD_PRECIARIO_IMPUTACIONES];


-- dbo.VW_PRD_PRECIARIO_RENGLONES source

ALTER VIEW VW_PRD_PRECIARIO_RENGLONES as
select * from DGBIDB.dbo.[19_PRD_PRECIARIO_RENGLONES];


-- dbo.VW_PRD_RENGLONES source

ALTER VIEW VW_PRD_RENGLONES as
select * from DGBIDB.dbo.[07_PRD_RENGLONES];


-- dbo.VW_PRECIARIO source

ALTER VIEW VW_PRECIARIO as
select * from DGBIDB.dbo.[16_PRECIARIO];


-- dbo.VW_PRECIARIO_IMPUTACIONES source

ALTER VIEW VW_PRECIARIO_IMPUTACIONES as
select * from DGBIDB.dbo.[17_PRECIARIO_IMPUTACIONES];


-- dbo.VW_RELACION_BAC_SIGAF source

ALTER VIEW VW_RELACION_BAC_SIGAF AS
select * from DGBIDB.dbo.[01_RELACION_BAC_SIGAF] ;


-- dbo.VW_RP source

ALTER VIEW VW_RP as
select * from DGBIDB.dbo.[11_RP];


-- dbo.VW_RPR_IMPUTACIONES source

ALTER VIEW VW_RPR_IMPUTACIONES as
select * from DGBIDB.dbo.[06_RPR_IMPUTACIONES] ;


-- dbo.VW_RPR_RENGLONESAS source

ALTER VIEW VW_RPR_RENGLONESAS as
select * from DGBIDB.dbo.[05_RPR_RENGLONES];


-- dbo.VW_RPR_SPR_PRD source

ALTER VIEW VW_RPR_SPR_PRD AS
select * from DGBIDB.dbo.[04_RPR_SPR_PRD] ;


-- dbo.VW_SPR_IMPUTACIONES source

ALTER VIEW VW_SPR_IMPUTACIONES AS
select * from DGBIDB.dbo.[03_SPR_IMPUTACIONES] ;


-- dbo.VW_SPR_RENGLONES source

ALTER VIEW VW_SPR_RENGLONES AS
select * from DGBIDB.dbo.[02_SPR_RENGLONES] ;


-- dbo.VW_UNIDADES_EJECUTORAS source

ALTER VIEW VW_UNIDADES_EJECUTORAS as
select * from DGBIDB.dbo.[23_UNIDADES_EJECUTORAS];


-- dbo.vw_entes source

ALTER VIEW vw_entes AS
SELECT o_ente, denom_ente, nro_oc_sigaf FROM DGBIDB.dbo.[25_ENTES];