select fade2.tipo_solicitud.descripcion tipo,
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
fade2.responsable_servicio.documento as documento1,
fade2.solicitud.fecha_creacion,
fade2.solicitud.nro_expediente,
fade2.solicitud.exp_observaciones observaciones,
fade2.bui.numero,
fade2.bui.vencimiento,
fade2.bui.fechabui,
fade2.bui.total,
fade2.bui.observacion,
fade2.bui.estado,
fade2.bui.fechapago,
fade2.responsable_policia.apellido_nombre resp_cumplimiento,
fade2.responsable_policia.cuil,
fade2.responsable_policia.legajo
from fade2.solicitud
join fade2.tipo_solicitud on fade2.tipo_solicitud.id = fade2.solicitud.id_tipo_solicitud
join fade2.ente on fade2.ente.id = fade2.solicitud.id_ente
join fade2.tipo_persona on fade2.tipo_persona.id = fade2.ente.id_tipo_persona
join fade2.direccion on fade2.direccion.id = fade2.solicitud.id_direccion_prestacion
join fade2.planfinanciero on fade2.planfinanciero.id = fade2.solicitud.id_plan_financiero
join fade2.carpetacredito on fade2.carpetacredito.id = fade2.planfinanciero.idcarpetacredito
join fade2.tipo_contrato on fade2.tipo_contrato.id = fade2.carpetacredito.idtipocontrato
join fade2.tipo_calculo on fade2.tipo_calculo.id = fade2.carpetacredito.idtipocalculo
join fade2.unidadfuncional on fade2.unidadfuncional.id = fade2.planfinanciero.idunidadfuncional
join fade2.tipo_direccion on fade2.tipo_direccion.id = fade2.unidadfuncional.idtipodireccion
join fade2.carteranucleo on fade2.carteranucleo.id = fade2.unidadfuncional.idnucleo
join fade2.carterainmobiliaria on fade2.carterainmobiliaria.id = fade2.carteranucleo.idcarterainmobiliaria
join fade2.responsable_servicio on fade2.responsable_servicio.id = fade2.solicitud.id_responsable_servicio
join fade2.responsable_policia on fade2.responsable_policia.id = fade2.solicitud.id_responsable_policia
left join fade2.bui on fade2.bui.id_solicitud = fade2.solicitud.id
order by fade2.carpetacredito.id, fade2.bui.vencimiento
