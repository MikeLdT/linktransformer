import os
import pandas as pd
from linktransformer import DATA_DIR_PATH
import linktransformer as lt


def test_data_dir_path():
    print(DATA_DIR_PATH)
    assert os.path.exists(DATA_DIR_PATH)
    assert os.path.isdir(DATA_DIR_PATH)

def test_lm_merge():
    df1 = pd.read_csv(os.path.join(DATA_DIR_PATH, "toy_comp_1.csv"))
    df2 = pd.read_csv(os.path.join(DATA_DIR_PATH, "toy_comp_2.csv"))

    # Test your function here
    df_lm_matched = lt.merge(df2, df1, merge_type='1:m', on="CompanyName", model="sentence-transformers/all-MiniLM-L6-v2", left_on=None, right_on=None)
    assert isinstance(df_lm_matched, pd.DataFrame)
    # Add more assertions to check the correctness of the output

def test_lm_aggregate():
    df_coarse = pd.read_csv(os.path.join(DATA_DIR_PATH, "coarse.csv"))
    df_fine = pd.read_csv(os.path.join(DATA_DIR_PATH, "fine.csv"))

    # Test your function here
    df_lm_aggregate = lt.aggregate_rows(df_fine, df_coarse, model="sentence-transformers/all-mpnet-base-v2", left_on="Fine Category Name", right_on="Coarse Category Name")
    assert isinstance(df_lm_aggregate, pd.DataFrame)
    # Add more assertions to check the correctness of the output

def test_lm_merge_with_multiple_columns():
    df1 = pd.read_csv(os.path.join(DATA_DIR_PATH, "toy_multi_1.csv"))
    df2 = pd.read_csv(os.path.join(DATA_DIR_PATH, "toy_multi_2.csv"))

    # Test your function here
    df_lm_matched = lt.merge(df2, df1, merge_type='1:m', on=["CompanyName", "ProductDescription"], model="sentence-transformers/all-MiniLM-L6-v2", left_on=None, right_on=None)
    assert isinstance(df_lm_matched, pd.DataFrame)
    # Add more assertions to check the correctness of the output

def test_lm_merge_with_blocking_df():
    df1 = pd.read_csv(os.path.join(DATA_DIR_PATH, "toy_comp_1.csv"))
    df2 = pd.read_csv(os.path.join(DATA_DIR_PATH, "toy_comp_2.csv"))

    # Test your function here
    df_lm_matched = lt.merge_blocking(df2, df1, merge_type='1:m', on="CompanyName", model="sentence-transformers/all-MiniLM-L6-v2", left_on=None, right_on=None, blocking_vars=["Country"])
    assert isinstance(df_lm_matched, pd.DataFrame)
    # Add more assertions to check the correctness of the output

# Add more test functions for other functionalities of your code

# French to English Translation Test
def test_french_to_english_crosslingual():
    df_french = pd.read_csv(os.path.join(DATA_DIR_PATH, "translation_1.csv"))
    df_english = pd.read_csv(os.path.join(DATA_DIR_PATH, "translation_2.csv"))

    # Test your function here
    df_lm_matched = lt.merge(df_french, df_english, merge_type='1:m', left_on="Libellé du Produit", right_on="Product Label", model="distiluse-base-multilingual-cased-v1")
    assert isinstance(df_lm_matched, pd.DataFrame)
    # Add more assertions to check the correctness of the output


###Test deduplication
def test_dedup():
    df=pd.read_csv(os.path.join(DATA_DIR_PATH,"toy_comp_2.csv"))
    df_dedup=lt.dedup_rows(df,on="CompanyName",model="sentence-transformers/all-MiniLM-L6-v2",cluster_type= "agglomerative",
        cluster_params= {'threshold': 0.7})
    assert isinstance(df_dedup, pd.DataFrame,)
    # Add more assertions to check the correctness of the output


##Test clustering
def test_cluster():
    df=pd.read_csv(os.path.join(DATA_DIR_PATH,"toy_comp_2.csv"))
    df_cluster=lt.cluster_rows(df,on="CompanyName",model="sentence-transformers/all-MiniLM-L6-v2",cluster_type= "agglomerative",
        cluster_params= {'threshold': 0.7})
    assert isinstance(df_cluster, pd.DataFrame,)
    # Add more assertions to check the correctness of the output

###Test evaluate pairs
def test_eval_pairs():
    df=pd.read_csv(os.path.join(DATA_DIR_PATH,"toy_pairs.csv"))
    df_eval=lt.evaluate_pairs(df, model="sentence-transformers/all-MiniLM-L6-v2",left_on="company_name_1",right_on="company_name_2",openai_key=None)

    assert isinstance(df_eval,pd.DataFrame)

##Test pairwise evaluate
def test_all_pairwise_eval():
    df=pd.read_csv(os.path.join(DATA_DIR_PATH,"toy_pairs.csv"))
    df_eval=lt.all_pair_combos_evaluate(df, model="sentence-transformers/all-MiniLM-L6-v2",left_on="company_name_1",right_on="company_name_2",openai_key=None)
    print(df_eval)
    assert isinstance(df_eval,pd.DataFrame)


if __name__ == "__main__":
    test_data_dir_path()
    test_lm_merge()
    test_lm_aggregate()
    test_lm_merge_with_multiple_columns()
    test_lm_merge_with_blocking_df()
    test_french_to_english_crosslingual()
    test_dedup()