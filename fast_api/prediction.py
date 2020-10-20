from pydantic import BaseModel
from typing import List


class Prediction(BaseModel):
    file_name: str
    content_type: str
    sudoku_board: List[List[int]] = []
    sudoku_shape: tuple
    sudoku_size: int
