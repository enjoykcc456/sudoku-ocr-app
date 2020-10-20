from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import cv2


def locate_puzzle(image, debug=False):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply Gaussian blur with 7x7 kernel
    blurred_image = cv2.blur(gray_image, (7, 7), 3)

    if debug:
        cv2.imshow('blurred', blurred_image)
        cv2.waitKey(0)

    # apply adaptive thresholding to peg grayscale pixels toward each end of the [0, 255] pixel range
    thresh = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    if debug:
        cv2.imshow('after adaptive thresh', thresh)
        cv2.waitKey(0)

    # invert the threshold map
    thresh = cv2.bitwise_not(thresh)

    if debug:
        cv2.imshow('after bitwise not', thresh)
        cv2.waitKey(0)

    # find countours in the thresholded image
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    # sort contours by size in descending
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # initialize a contour corresponds to the puzzle outline
    puzzle_contour = None

    for contour in contours:
        # approximate the contour
        perimeter = cv2.arcLength(contour, True)    # second para specify whether it is a closed contour
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        # if the approximated contour has four points, outline of the puzzle
        # is assumed to be found
        if len(approx) == 4:
            puzzle_contour = approx
            break

    # if puzzle contour is empty, the puzzle's outline could not be found, raise an error
    if puzzle_contour is None:
        raise Exception(('Could not find Sudoku puzzle outline. '
                         'Try debugging your thresholding and contour steps.'))

    if debug:
        output_image = image.copy()
        cv2.drawContours(output_image, [puzzle_contour], -1, (0, 0, 255), 2)
        cv2.imshow('puzzle outline', output_image)
        cv2.waitKey(0)

    # apply four point transform to deskew the puzzle to get a top-down view of the puzzle
    # to determine the row, columns and cells easier
    puzzle = four_point_transform(image, puzzle_contour.reshape(4, 2))
    warped = four_point_transform(gray_image, puzzle_contour.reshape(4, 2))

    if debug:
        cv2.imshow('puzzle transformed', puzzle)
        cv2.waitKey(0)

    # return puzzle in RGB and grayscale
    return puzzle, warped


def extract_digit(cell, debug=False):
    # apply automatic thresholding to the cell
    thresh = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # clear any foreground pixels that touch the border of the cell
    thresh = clear_border(thresh)

    # if debug:
    #     cv2.imshow('Cell Thresh', thresh)
    #     cv2.waitKey(0)

    # find contours
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # if no contour, then this is an empty cell
    if len(contours) == 0:
        return None

    # else, it is not empty. hence, find the largest contour in the cell and create a mask for it
    contour = max(contours, key=cv2.contourArea)

    # get the smallest y coordinate to indicate the highest point of the contour
    smallest_pos = np.argmin(contour, axis=0).reshape(2)
    y_min = contour[smallest_pos[1]][0][1]
    # x_of_y_min = contour[smallest_pos[1]][0][0]

    mask = np.zeros(thresh.shape, dtype='uint8')
    cv2.drawContours(mask, [contour], -1, 255, -1)

    # get the percentage of masked pixels over the total image area
    h, w = thresh.shape
    percentage = cv2.countNonZero(mask) / float(w*h)

    # filter out false positive by ignoring mask that filled less than 3%,
    # as it could be noise
    if percentage < 0.03:
        return None

    # else, apply mask to the cell
    digit = cv2.bitwise_and(thresh, thresh, mask=mask)

    # calculate the offset to check if the highest point is consistent across different digit contour
    # we set the standard highest point as 10, content of image will be adjusted if there is a differ
    # in the offset
    y_offset = y_min - 10
    # center_of_x = w // 2
    # x_offset = center_of_x - x_of_y_min

    # move the image content based on offset
    if y_offset != 0:
        translation_matrix = np.float32([[1, 0, 0], [0, 1, -y_offset]])
        digit = cv2.warpAffine(thresh, translation_matrix, (w, h))

    if debug:
        cv2.imshow('digit', digit)
        cv2.waitKey(0)

    return digit
