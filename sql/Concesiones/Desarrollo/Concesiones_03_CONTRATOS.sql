SELECT 
    fade2.carpetacredito.id nro,
    fade2.carpetacredito.codexpediente expediente,
    TO_CHAR(fade2.carpetacredito.fechafirma, 'FMDD/FMMM/YYYY') fechafirma,
    fade2.tipo_contrato.descripcion tipo_contrato,
    fade2.tipo_calculo.descripcion tipo_calculo,
    fade2.tipo_direccion.descripcion tipo_unidad,
    fade2.carterainmobiliaria.identificacion,
    fade2.carteranucleo.descripcion,
    fade2.unidadfuncional.nrounidad,
    CASE WHEN current_date BETWEEN fade2.adjudicatario_vigencia.desde AND fade2.adjudicatario_vigencia.hasta 
         THEN 'S' ELSE 'N' END vigente,
    fade2.ente.nombre,
    fade2.ente.documento,
    TO_CHAR(fade2.adjudicatario_vigencia.desde, 'FMDD/FMMM/YYYY') desde,
    TO_CHAR(fade2.adjudicatario_vigencia.hasta, 'FMDD/FMMM/YYYY') hasta,
    fade2.adjudicatario.principal
FROM fade2.carpetacredito
JOIN fade2.planfinanciero ON fade2.planfinanciero.idcarpetacredito = fade2.carpetacredito.id
JOIN fade2.tipo_contrato ON fade2.tipo_contrato.id = fade2.carpetacredito.idtipocontrato
JOIN fade2.tipo_calculo ON fade2.tipo_calculo.id = fade2.carpetacredito.idtipocalculo
JOIN fade2.unidadfuncional ON fade2.unidadfuncional.id = fade2.planfinanciero.idunidadfuncional
JOIN fade2.tipo_direccion ON fade2.tipo_direccion.id = fade2.unidadfuncional.idtipodireccion
JOIN fade2.carteranucleo ON fade2.carteranucleo.id = fade2.unidadfuncional.idnucleo
JOIN fade2.carterainmobiliaria ON fade2.carterainmobiliaria.id = fade2.carteranucleo.idcarterainmobiliaria
JOIN fade2.adjudicatario ON fade2.adjudicatario.idplanfinanciero = fade2.planfinanciero.id
JOIN fade2.adjudicatario_vigencia ON fade2.adjudicatario_vigencia.idadjudicatario = fade2.adjudicatario.id
JOIN fade2.ente ON fade2.ente.id = fade2.adjudicatario.idente
ORDER BY fade2.carpetacredito.id, fade2.adjudicatario_vigencia.desde;
