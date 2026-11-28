import pandas as pd
import time
import numpy as np  

def read_sped(file:str,encoding:str)-> pd.DataFrame:
    count_sep = 0
    lst_df = []
    with open(file=file,encoding=encoding,mode='r') as txt:
        lines = txt.readlines()
        for line in lines:
            lst_df.append(line + ('|' * 100 ))
            count_sep = max([count_sep,len(line)-len(line.replace('|',''))])
    for i,item in enumerate(lst_df,start=0):
        lst_df[i] = str(item).split('|')[1:(count_sep+1)]
    df = pd.DataFrame(lst_df)
    return df    

def merger_df(df=pd.DataFrame)->pd.DataFrame:
    def filter_by_bloco(df:pd.DataFrame,bloco:str,n_columns:int)->pd.DataFrame:
        df_filter = df[(df[0] == bloco)].loc[:,:]
        df_out = df_filter.loc[:,:n_columns] 
        df_out['idx'] = df_filter['idx']
        return  df_out

    n_columns_c100 = 28
    n_columns_c170 = 36

    columns_name = {"C100":
                        ["REG","IND_OPER","IND_EMIT","COD_PART","COD_MOD","COD_SIT","SER","NUM_DOC","CHV_NFE","DT_DOC","DT_E_S","VL_DOC","IND_PGTO",
                        "VL_DESC","VL_ABAT_NT","VL_MERC","IND_FRT","VL_FRT","VL_SEG","VL_OUT_DA","VL_BC_ICMS","VL_ICMS","VL_BC_ICMS_ST","VL_ICMS_ST","VL_IPI",
                        "VL_PIS","VL_COFINS","VL_PIS_ST","VL_COFINS_ST",'idx'],
                    "C170":
                        ["REG","NUM_ITEM","COD_ITEM","DESCR_COMPL","QTD","UNID","VL_ITEM","VL_DESC","IND_MOV","CST_ICMS","CFOP","COD_NAT","VL_BC_ICMS","ALIQ_ICMS",
                         "VL_ICMS","VL_BC_ICMS_ST","ALIQ_ST","VL_ICMS_ST","IND_APUR","CST_IPI","COD_ENQ","VL_BC_IPI","ALIQ_IPI","VL_IPI","CST_PIS","VL_BC_PIS",
                         "ALIQ_PIS","QUANT_BC_PIS","ALIQ_PIS_QUANT","VL_PIS","CST_COFINS","VL_BC_COFINS","ALIQ_COFINS","QUANT_BC_COFINS","ALIQ_COFINS_QUANT","VL_COFINS",
                         "COD_CTA","idx"],
                    "0200":
                        ["REG","COD_ITEM","DESCR_ITEM","COD_BARRA","COD_ANT_ITEM","UNID_INV","TIPO_ITEM","COD_NCM","EX_IPI","COD_GEN","COD_LST","ALIQ_ICMS","idx"]}

    
    df['idx'] = np.where(df[0] == 'C100',df.index,None)
    df['idx'] = df['idx'].ffill()

    df_0200 = filter_by_bloco(df=df,bloco='0200',n_columns=11)
    df_C100 = filter_by_bloco(df=df,bloco='C100',n_columns=n_columns_c100)
    df_C170 = filter_by_bloco(df=df,bloco='C170',n_columns=n_columns_c170)

    df_C100.columns = columns_name['C100']
    df_C170.columns = columns_name['C170']
    df_0200.columns = columns_name['0200']

    df_merged = pd.merge(left=df_C100,right=df_C170,how='outer',on='idx')
    df_output = pd.merge(left=df_merged,right=df_0200,how='outer',on='COD_ITEM')

    df_output["IND_OPER"] = np.where(df_output["IND_OPER"] =="0","Entrada",np.where(df_output["IND_OPER"] =="1","Saída",""))

    return df_output

def main():

    files = ['C:\\Users\\A0182056\\OneDrive - Telefonica\\Projetos\\4. Outros\\Olera\\PIS COFINS\\PISCOFINS_20260101_20260131_45087511000120_Original_20260313221522_0C06EA721603CEED76687FA924B3EA59AA950FC3.txt']
    lst_df = []
    
    for file in files:
        df = read_sped(file=file,encoding='ISO-8859-1')    
        df_merged = merger_df(df=df)
        lst_df.append(df_merged)

    file_name =  f"{int(time.time())}_teste.xlsx"

    df_out = pd.concat(lst_df) 
    df_out.to_excel(file_name,index=False)

if __name__ == '__main__':
    initial_time = time.time()
    main()
    final_time = int(time.time() - initial_time)
    print(f'run time {final_time} seconds')