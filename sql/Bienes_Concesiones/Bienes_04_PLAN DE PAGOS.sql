select bienes.tipo_solicitud.descripcion tipo,
bienes.solicitud.objetivo_prestacion,
bienes.ente.nombre,
bienes.ente.documento,
bienes.ente.email,
bienes.ente.emailadicional,
bienes.tipo_persona.descripcion tipo_persona,
bienes.direccion.calle,
bienes.carpetacredito.id carpeta,
bienes.carterainmobiliaria.identificacion,
bienes.carteranucleo.descripcion sub_division,
bienes.unidadfuncional.nrounidad,
bienes.tipo_contrato.descripcion tipo_contrato,
bienes.tipo_calculo.descripcion tipo_calculo,
bienes.responsable_servicio.apellido_nombre resp_adjudicatatio,
bienes.responsable_servicio.documento as documento1,
bienes.solicitud.fecha_creacion,
bienes.solicitud.nro_expediente,
bienes.solicitud.exp_observaciones observaciones,
bienes.bui.numero,
bienes.bui.vencimiento,
bienes.bui.fechabui,
bienes.bui.total,
bienes.bui.observacion,
bienes.bui.estado,
bienes.bui.fechapago,
bienes.responsable_policia.apellido_nombre resp_cumplimiento,
bienes.responsable_policia.cuil,
bienes.responsable_policia.legajo
from bienes.solicitud
join bienes.tipo_solicitud on bienes.tipo_solicitud.id = bienes.solicitud.id_tipo_solicitud
join bienes.ente on bienes.ente.id = bienes.solicitud.id_ente
join bienes.tipo_persona on bienes.tipo_persona.id = bienes.ente.id_tipo_persona
join bienes.direccion on bienes.direccion.id = bienes.solicitud.id_direccion_prestacion
join bienes.planfinanciero on bienes.planfinanciero.id = bienes.solicitud.id_plan_financiero
join bienes.carpetacredito on bienes.carpetacredito.id = bienes.planfinanciero.idcarpetacredito
join bienes.tipo_contrato on bienes.tipo_contrato.id = bienes.carpetacredito.idtipocontrato
join bienes.tipo_calculo on bienes.tipo_calculo.id = bienes.carpetacredito.idtipocalculo
join bienes.unidadfuncional on bienes.unidadfuncional.id = bienes.planfinanciero.idunidadfuncional
join bienes.tipo_direccion on bienes.tipo_direccion.id = bienes.unidadfuncional.idtipodireccion
join bienes.carteranucleo on bienes.carteranucleo.id = bienes.unidadfuncional.idnucleo
join bienes.carterainmobiliaria on bienes.carterainmobiliaria.id = bienes.carteranucleo.idcarterainmobiliaria
join bienes.responsable_servicio on bienes.responsable_servicio.id = bienes.solicitud.id_responsable_servicio
join bienes.responsable_policia on bienes.responsable_policia.id = bienes.solicitud.id_responsable_policia
left join bienes.bui on bienes.bui.id_solicitud = bienes.solicitud.id
order by bienes.carpetacredito.id, bienes.bui.vencimiento;