from pyspark.sql import functions as F

from serra.transformers.transformer import Transformer
import json

class MapTransformer(Transformer):
    """
    Test transformer to add a column to dataframe
    :param config: Holds column value
    """

    def __init__(self, config):
        self.config = config
        self.name = config.get("name")
        self.map_dict = config.get("map_dict")
        self.map_dict_path = config.get("map_dict_path")
        self.col_key = config.get('col_key')

    def transform(self, df):
        """
        Add column with col_value to dataframe
        :return; Dataframe w/ new column containing col_value
        """
        if self.map_dict is None:
            with open(self.map_dict_path) as f:
                self.map_dict = json.load(f)

        for key, value in self.map_dict.items():
            df = df.withColumn(f'{self.name}_{key}', F.when(F.col(self.col_key) == key, value))

        # Select the first non-null value from the generated columns
        # create list, then unpack *
        df = df.withColumn(self.name, F.coalesce(*[F.col(f'{self.name}_{key}') for key in self.map_dict]))
        df = df.drop(*[f'{self.name}_{key}' for key in self.map_dict])
        return df
        
        
    

        
    