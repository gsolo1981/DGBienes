SELECT 
    ente.o_ente,
    ente.XL_ENTE AS denom_ente,
    oc.n_ocompra AS nro_oc_sigaf
FROM slu.torden_compra OC, SLU.BENTE ente
WHERE oc.o_ente=ente.o_ente
AND (oc.aa_ocompra, oc.t_ocompra, oc.n_ocompra) IN (
    SELECT DISTINCT aa_ocompra, t_ocompra, n_ocompra
    FROM slu.dorden_compra_ren
    WHERE c_clase IN (990010, 560000, 790000))
      AND t_ocompra = 'OCA';