import pandas as pd
import pandera as pa
from datetime import datetime

from contrato import MetricasFinanceirasBase, MetricasFinanceirasOut


def extrai_dados(dir_arquivo: str) -> pd.DataFrame:
    df = pd.read_csv(dir_arquivo)

    try:
        df = MetricasFinanceirasBase.validate(df, lazy=True)
        return df
    except pa.errors.SchemaErrors as exc:
        print("Erro ao dalidar dados:")
        print(exc)

    return df 

@pa.check_output(MetricasFinanceirasOut, lazy=True)
def transforma_dados(df: pd.DataFrame) -> pd.DataFrame:
    df_transformado = df.copy()
    df_transformado["valor_do_imposto"] = df_transformado["percentual_de_imposto"] * df_transformado["receita_operacional"]
    df_transformado["custo_total"] = df_transformado["valor_do_imposto"] + df_transformado["custos_operacionais"]
    df_transformado["receita_liquida"] = df_transformado["receita_operacional"] - df_transformado["custo_total"]
    df_transformado["margem_operacional"] = (df_transformado["receita_liquida"] / df_transformado["receita_operacional"]) 
    df_transformado["transformado_em"] = datetime.now()

    return df_transformado

def carrega_dados(df: pd.DataFrame) -> None:
    pass

if __name__ == '__main__':
    dir_arquivo = "data/dados_financeiros.csv"
    df = extrai_dados(dir_arquivo)
    df_transformado = transforma_dados(df)

