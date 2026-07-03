from abc import ABC, abstractmethod
import pandas as pd


class DataUserInterface(ABC):
    @abstractmethod
    def get_heatmap_df(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_script(self) -> str:
        pass

    @abstractmethod
    def post_script(self,script:str):
        pass
    
    @abstractmethod
    def post_csv(self,df:pd.DataFrame):
        pass

