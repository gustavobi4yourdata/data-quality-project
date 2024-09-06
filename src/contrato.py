import pandera as pa
from pandera.typing import Series 


class MetricasFinanceirasBase(pa.DataFrameModel):
    setor_da_empresa: Series[str]
    receita_operacional: Series[float] = pa.Field(ge=0)
    data: Series[pa.DateTime] 
    percentual_de_imposto: Series[float] = pa.Field(in_range= {"min_value": 0, "max_value": 1})
    custos_operacionais: Series[float] = pa.Field(ge=0)

    class Config:
        strict = True
        coerce = True

    @pa.check(
            "setor_da_empresa", 
            name = "Checagem código dos setores",
            error = "Cógido do setor da empresa é inválido")
    def checa_codigo_setor(cls, codigo: Series[str]) -> Series[bool]:
        return codigo.str[:4].isin(['REP_', 'MNT_', 'VND_'])

