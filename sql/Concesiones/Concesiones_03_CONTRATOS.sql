SELECT 
    fade.carpetacredito.id nro,
    fade.carpetacredito.codexpediente expediente,
    TO_CHAR(fade.carpetacredito.fechafirma, 'FMDD/FMMM/YYYY') fechafirma,
    fade.tipo_contrato.descripcion tipo_contrato,
    fade.tipo_calculo.descripcion tipo_calculo,
    fade.tipo_direccion.descripcion tipo_unidad,
    fade.carterainmobiliaria.identificacion,
    fade.carteranucleo.descripcion,
    fade.unidadfuncional.nrounidad,
    CASE WHEN current_date BETWEEN fade.adjudicatario_vigencia.desde AND fade.adjudicatario_vigencia.hasta 
         THEN 'S' ELSE 'N' END vigente,
    fade.ente.nombre,
    fade.ente.documento,
    TO_CHAR(fade.adjudicatario_vigencia.desde, 'FMDD/FMMM/YYYY') desde,
    TO_CHAR(fade.adjudicatario_vigencia.hasta, 'FMDD/FMMM/YYYY') hasta,
    fade.adjudicatario.principal
FROM fade.carpetacredito
JOIN fade.planfinanciero ON fade.planfinanciero.idcarpetacredito = fade.carpetacredito.id
JOIN fade.tipo_contrato ON fade.tipo_contrato.id = fade.carpetacredito.idtipocontrato
JOIN fade.tipo_calculo ON fade.tipo_calculo.id = fade.carpetacredito.idtipocalculo
JOIN fade.unidadfuncional ON fade.unidadfuncional.id = fade.planfinanciero.idunidadfuncional
JOIN fade.tipo_direccion ON fade.tipo_direccion.id = fade.unidadfuncional.idtipodireccion
JOIN fade.carteranucleo ON fade.carteranucleo.id = fade.unidadfuncional.idnucleo
JOIN fade.carterainmobiliaria ON fade.carterainmobiliaria.id = fade.carteranucleo.idcarterainmobiliaria
JOIN fade.adjudicatario ON fade.adjudicatario.idplanfinanciero = fade.planfinanciero.id
JOIN fade.adjudicatario_vigencia ON fade.adjudicatario_vigencia.idadjudicatario = fade.adjudicatario.id
JOIN fade.ente ON fade.ente.id = fade.adjudicatario.idente
ORDER BY fade.carpetacredito.id, fade.adjudicatario_vigencia.desde;
