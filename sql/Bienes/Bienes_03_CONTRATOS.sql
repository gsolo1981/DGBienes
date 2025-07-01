select bienes.carpetacredito.id nro,
bienes.carpetacredito.codexpediente expediente,
bienes.carpetacredito.fechafirma,
bienes.tipo_contrato.descripcion tipo_contrato,
bienes.tipo_calculo.descripcion tipo_calculo,
bienes.tipo_direccion.descripcion tipo_unidad,
bienes.carterainmobiliaria.identificacion,
bienes.carteranucleo.descripcion,
bienes.unidadfuncional.nrounidad,
case when current_date between bienes.adjudicatario_vigencia.desde and bienes.adjudicatario_vigencia.hasta then 'S' else 'N' end vigente,
bienes.ente.nombre,
bienes.ente.documento,
bienes.adjudicatario_vigencia.desde,
bienes.adjudicatario_vigencia.hasta,
bienes.adjudicatario.principal
from bienes.carpetacredito
join bienes.planfinanciero on bienes.planfinanciero.idcarpetacredito = bienes.carpetacredito.id
join bienes.tipo_contrato on bienes.tipo_contrato.id = bienes.carpetacredito.idtipocontrato
join bienes.tipo_calculo on bienes.tipo_calculo.id = bienes.carpetacredito.idtipocalculo
join bienes.unidadfuncional on bienes.unidadfuncional.id = bienes.planfinanciero.idunidadfuncional
join bienes.tipo_direccion on bienes.tipo_direccion.id = bienes.unidadfuncional.idtipodireccion
join bienes.carteranucleo on bienes.carteranucleo.id = bienes.unidadfuncional.idnucleo
join bienes.carterainmobiliaria on bienes.carterainmobiliaria.id = bienes.carteranucleo.idcarterainmobiliaria
join bienes.adjudicatario on bienes.adjudicatario.idplanfinanciero = bienes.planfinanciero.id
join bienes.adjudicatario_vigencia on bienes.adjudicatario_vigencia.idadjudicatario = bienes.adjudicatario.id
join bienes.ente on bienes.ente.id = bienes.adjudicatario.idente
order by bienes.carpetacredito.id, bienes.adjudicatario_vigencia.desde
