import cv2
import imutils
import numpy as np
from PIL import Image
from sudoku import Sudoku

from fast_api.utils.puzzle import locate_puzzle, extract_digit
from tensorflow.keras.preprocessing.image import img_to_array

import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''


def infer_image(model, image):
    # predict with custom created model
    predictions = model.predict(image)  # make prediction
    digit = predictions.argmax(axis=1)[0]  # extract the result
    # print(f'{digit}')
    return digit


def preprocess_image(image, resize_target):
    image = cv2.resize(image, (resize_target[0], resize_target[1]))  # resize the image according to model input size
    image = img_to_array(image)  # convert to numpy array of float32, and reshape
    image = image / 255.0  # divide by 255 to keep pixel in range of 0 to 1
    image = np.expand_dims(image, axis=0)  # include a dummy dimension
    return image


def solve_sudoku(model, image, resize_target, debug=0):
    # load and resize the image
    image = imutils.resize(image, width=600)

    # get the puzzle and warped in top down view
    puzzle, warped = locate_puzzle(image, debug=debug > 0)

    # as sudoku puzzle is normally 9x9, divide the height and width of the puzzle by 9 to
    # get the step for x and y which is used to infer the position of each cell
    height, width, _ = puzzle.shape
    x_step = width // 9
    y_step = height // 9

    # create a numpy array in shape of 9x9 with zeros to store each digit
    puzzle_board = np.zeros((9, 9), dtype='int')

    # create a list to store each cell's coordinate
    cell_coords = []

    # loop through each row
    for y in range(9):
        row = []
        # loop through each column
        for x in range(9):
            # infer the cell coordinate based on step
            x_min = x * x_step
            y_min = y * y_step
            x_max = (x+1) * x_step
            y_max = (y+1) * y_step

            # store each cell's coordinate
            cell_coord = (x_min, y_min, x_max, y_max)
            row.append(cell_coord)

            # crop the cell image and extract the digit from the cell
            cropped_cell_image = warped[y_min:y_max, x_min:x_max]
            digit_image = extract_digit(cropped_cell_image, debug=debug > 0)

            # if digit exists
            if digit_image is not None:
                # perform necessary pre-processing
                digit_image = preprocess_image(image=digit_image, resize_target=resize_target)

                # send the digit image to predict the digit
                digit_number = infer_image(model=model, image=digit_image)

                # change the value of the digit based on the location in the puzzle board
                puzzle_board[y, x] = digit_number

        cell_coords.append(row)

    print('[INFO] OCRed sudoku board:')
    puzzle = Sudoku(3, 3, board=puzzle_board.tolist())
    if debug:
        puzzle.show()

    print('[INFO] solve the puzzle...')
    results = puzzle.solve()
    if debug:
        results.show_full()
    return results
