SELECT 
    fade.tipo_solicitud.descripcion tipo, 
    fade.solicitud.objetivo_prestacion, 
    fade.ente.nombre, 
    fade.ente.documento, 
    fade.ente.email, 
    fade.ente.emailadicional, 
    fade.tipo_persona.descripcion tipo_persona, 
    fade.direccion.calle, 
    fade.carpetacredito.id carpeta, 
    fade.carterainmobiliaria.identificacion, 
    fade.carteranucleo.descripcion sub_division, 
    fade.unidadfuncional.nrounidad, 
    fade.tipo_contrato.descripcion tipo_contrato, 
    fade.tipo_calculo.descripcion tipo_calculo, 
    fade.responsable_servicio.apellido_nombre resp_adjudicatatio, 
    fade.responsable_servicio.documento AS documento1, 
    TO_CHAR(fade.solicitud.fecha_creacion, 'FMDD/FMMM/YYYY') fecha_creacion, 
    fade.solicitud.nro_expediente, 
    fade.solicitud.exp_observaciones observaciones, 
    fade.bui.numero, 
    TO_CHAR(fade.bui.vencimiento, 'FMDD/FMMM/YYYY') vencimiento, 
    TO_CHAR(fade.bui.fechabui, 'DD/MM/YYYY HH24:MI:SS') fechabui, 
    fade.bui.total, 
    fade.bui.observacion, 
    fade.bui.estado, 
    TO_CHAR(fade.bui.fechapago, 'FMDD/FMMM/YYYY') fechapago, 
    fade.responsable_policia.apellido_nombre resp_cumplimiento, 
    fade.responsable_policia.cuil, 
    fade.responsable_policia.legajo 
FROM fade.solicitud 
JOIN fade.tipo_solicitud ON fade.tipo_solicitud.id = fade.solicitud.id_tipo_solicitud 
JOIN fade.ente ON fade.ente.id = fade.solicitud.id_ente 
JOIN fade.tipo_persona ON fade.tipo_persona.id = fade.ente.id_tipo_persona 
JOIN fade.direccion ON fade.direccion.id = fade.solicitud.id_direccion_prestacion 
JOIN fade.planfinanciero ON fade.planfinanciero.id = fade.solicitud.id_plan_financiero 
JOIN fade.carpetacredito ON fade.carpetacredito.id = fade.planfinanciero.idcarpetacredito 
JOIN fade.tipo_contrato ON fade.tipo_contrato.id = fade.carpetacredito.idtipocontrato 
JOIN fade.tipo_calculo ON fade.tipo_calculo.id = fade.carpetacredito.idtipocalculo 
JOIN fade.unidadfuncional ON fade.unidadfuncional.id = fade.planfinanciero.idunidadfuncional 
JOIN fade.tipo_direccion ON fade.tipo_direccion.id = fade.unidadfuncional.idtipodireccion 
JOIN fade.carteranucleo ON fade.carteranucleo.id = fade.unidadfuncional.idnucleo 
JOIN fade.carterainmobiliaria ON fade.carterainmobiliaria.id = fade.carteranucleo.idcarterainmobiliaria 
JOIN fade.responsable_servicio ON fade.responsable_servicio.id = fade.solicitud.id_responsable_servicio 
JOIN fade.responsable_policia ON fade.responsable_policia.id = fade.solicitud.id_responsable_policia 
LEFT JOIN fade.bui ON fade.bui.id_solicitud = fade.solicitud.id 
ORDER BY fade.carpetacredito.id, fade.bui.vencimiento;