select fade2.carpetacredito.id nro,
fade2.carpetacredito.codexpediente expediente,
fade2.carpetacredito.fechafirma,
fade2.tipo_contrato.descripcion tipo_contrato,
fade2.tipo_calculo.descripcion tipo_calculo,
fade2.tipo_direccion.descripcion tipo_unidad,
fade2.carterainmobiliaria.identificacion,
fade2.carteranucleo.descripcion,
fade2.unidadfuncional.nrounidad,
case when current_date between fade2.adjudicatario_vigencia.desde and fade2.adjudicatario_vigencia.hasta then 'S' else 'N' end vigente,
fade2.ente.nombre,
fade2.ente.documento,
fade2.adjudicatario_vigencia.desde,
fade2.adjudicatario_vigencia.hasta,
fade2.adjudicatario.principal
from fade2.carpetacredito
join fade2.planfinanciero on fade2.planfinanciero.idcarpetacredito = fade2.carpetacredito.id
join fade2.tipo_contrato on fade2.tipo_contrato.id = fade2.carpetacredito.idtipocontrato
join fade2.tipo_calculo on fade2.tipo_calculo.id = fade2.carpetacredito.idtipocalculo
join fade2.unidadfuncional on fade2.unidadfuncional.id = fade2.planfinanciero.idunidadfuncional
join fade2.tipo_direccion on fade2.tipo_direccion.id = fade2.unidadfuncional.idtipodireccion
join fade2.carteranucleo on fade2.carteranucleo.id = fade2.unidadfuncional.idnucleo
join fade2.carterainmobiliaria on fade2.carterainmobiliaria.id = fade2.carteranucleo.idcarterainmobiliaria
join fade2.adjudicatario on fade2.adjudicatario.idplanfinanciero = fade2.planfinanciero.id
join fade2.adjudicatario_vigencia on fade2.adjudicatario_vigencia.idadjudicatario = fade2.adjudicatario.id
join fade2.ente on fade2.ente.id = fade2.adjudicatario.idente
order by fade2.carpetacredito.id, fade2.adjudicatario_vigencia.desde
