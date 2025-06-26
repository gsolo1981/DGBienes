SELECT 
    fade2.tipo_solicitud.descripcion tipo, 
    fade2.solicitud.objetivo_prestacion, 
    fade2.ente.nombre, 
    fade2.ente.documento, 
    fade2.ente.email, 
    fade2.ente.emailadicional, 
    fade2.tipo_persona.descripcion tipo_persona, 
    fade2.direccion.calle, 
    fade2.carpetacredito.id carpeta, 
    fade2.carterainmobiliaria.identificacion, 
    fade2.carteranucleo.descripcion sub_division, 
    fade2.unidadfuncional.nrounidad, 
    fade2.tipo_contrato.descripcion tipo_contrato, 
    fade2.tipo_calculo.descripcion tipo_calculo, 
    fade2.responsable_servicio.apellido_nombre resp_adjudicatatio, 
    fade2.responsable_servicio.documento AS documento1, 
    TO_CHAR(fade2.solicitud.fecha_creacion, 'FMDD/FMMM/YYYY') fecha_creacion, 
    fade2.solicitud.nro_expediente, 
    fade2.solicitud.exp_observaciones observaciones, 
    fade2.bui.numero, 
    TO_CHAR(fade2.bui.vencimiento, 'FMDD/FMMM/YYYY') vencimiento, 
    TO_CHAR(fade2.bui.fechabui, 'DD/MM/YYYY HH24:MI:SS') fechabui, 
    fade2.bui.total, 
    fade2.bui.observacion, 
    fade2.bui.estado, 
    TO_CHAR(fade2.bui.fechapago, 'FMDD/FMMM/YYYY') fechapago, 
    fade2.responsable_policia.apellido_nombre resp_cumplimiento, 
    fade2.responsable_policia.cuil, 
    fade2.responsable_policia.legajo 
FROM fade2.solicitud 
JOIN fade2.tipo_solicitud ON fade2.tipo_solicitud.id = fade2.solicitud.id_tipo_solicitud 
JOIN fade2.ente ON fade2.ente.id = fade2.solicitud.id_ente 
JOIN fade2.tipo_persona ON fade2.tipo_persona.id = fade2.ente.id_tipo_persona 
JOIN fade2.direccion ON fade2.direccion.id = fade2.solicitud.id_direccion_prestacion 
JOIN fade2.planfinanciero ON fade2.planfinanciero.id = fade2.solicitud.id_plan_financiero 
JOIN fade2.carpetacredito ON fade2.carpetacredito.id = fade2.planfinanciero.idcarpetacredito 
JOIN fade2.tipo_contrato ON fade2.tipo_contrato.id = fade2.carpetacredito.idtipocontrato 
JOIN fade2.tipo_calculo ON fade2.tipo_calculo.id = fade2.carpetacredito.idtipocalculo 
JOIN fade2.unidadfuncional ON fade2.unidadfuncional.id = fade2.planfinanciero.idunidadfuncional 
JOIN fade2.tipo_direccion ON fade2.tipo_direccion.id = fade2.unidadfuncional.idtipodireccion 
JOIN fade2.carteranucleo ON fade2.carteranucleo.id = fade2.unidadfuncional.idnucleo 
JOIN fade2.carterainmobiliaria ON fade2.carterainmobiliaria.id = fade2.carteranucleo.idcarterainmobiliaria 
JOIN fade2.responsable_servicio ON fade2.responsable_servicio.id = fade2.solicitud.id_responsable_servicio 
JOIN fade2.responsable_policia ON fade2.responsable_policia.id = fade2.solicitud.id_responsable_policia 
LEFT JOIN fade2.bui ON fade2.bui.id_solicitud = fade2.solicitud.id 
ORDER BY fade2.carpetacredito.id, fade2.bui.vencimiento;