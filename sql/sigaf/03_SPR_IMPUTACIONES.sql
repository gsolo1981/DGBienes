select oc.aa_ocompra,
    oc.t_ocompra,
    oc.n_ocompra,
    oc.o_ente,
    oc.c_unid_ejec,
    oc.aa_oca_original,
    oc.n_oca_original,
    oc.fh_estado,
    ffi.c_numcred,
    ffi.c_juris,
    ffi.c_sjuris,
    ffi.c_entidad,
    ffi.c_inciso,
    ffi.c_pprincipal,
    ffi.c_pparcial,
    ffi.c_ubica_geo,
    ffi.i_total,
    oc.e_ocompra
from slu.torden_compra OC 
	JOIN slu.dorden_compra_ren REN  on ren.aa_ocompra= oc.aa_ocompra AND  ren.t_ocompra= oc.t_ocompra and ren.n_ocompra=oc.n_ocompra
	join slu.dorden_compra_ffi FFI on ffi.aa_ocompra= oc.aa_ocompra and ffi.n_ocompra=oc.n_ocompra and ffi.t_ocompra= oc.t_ocompra
	
where c_clase in (990010,560000,790000)	  and oc.t_ocompra='SPR' -- and oc.aa_ocompra=2021 and ROWNUM <= 200000
	--and oc.aa_ocompra=2021 and oc.t_ocompra='SPR' and oc.n_ocompra=48897
GROUP BY oc.aa_ocompra,
    oc.t_ocompra,
    oc.n_ocompra,
    oc.o_ente,
    oc.c_unid_ejec,
    oc.aa_oca_original,
    oc.n_oca_original,
    oc.fh_estado,
    ffi.c_numcred,
    ffi.c_juris,
    ffi.c_sjuris,
    ffi.c_entidad,
    ffi.c_inciso,
    ffi.c_pprincipal,
    ffi.c_pparcial,
    ffi.c_ubica_geo,
    ffi.i_total,
    oc.e_ocompra;
