from PIL import Image
import string
import os, time
import numpy as np

def convert_message_to_color_indices(Encoded_Message: str):
    """ Turns string into numbers. 'hello world' => [7, 4, 11, 11, 14, 62, 22, 14, 17, 11, 3]
    
    Args:
        Encoded_Message (str): string

    Returns:
        - list: List of color indices representing each character in the encoded message.
    """
    Color_Array = []
    chars = list(string.ascii_letters + string.digits + " ")
    for Letter in Encoded_Message:
        if Letter in chars:
            Int_Letter = chars.index(Letter)
            x = int(Int_Letter)
            Color_Array.append(x)
    return Color_Array

def set_last_digit_in_rgb(colour_arr, val):
    """
    Set the last digit of each color channel in an RGB tuple based on a given value.
    set_last_digit_in_rgb([10, 20, 30], 5) => [15, 25, 35]

    Parameters:
    - rgb_tuple (tuple): RGB color tuple.
    - value (int): Value used to set the last digit in each color channel.

    Returns:
    - tuple: Updated RGB tuple with modified last digits.
    """
    colour_arr = list(colour_arr)
    Digit_ARR = list(str(val))
    if len(str(val)) == 1:
        for i in range(0, 3):
            local_colour = colour_arr[i]
            temp = list(str(local_colour))
            temp[-1] = str(val)
            colour_arr[i] = int("".join(temp))

    else:
        for i in range(0, 3):
            local_colour = colour_arr[i]
            temp = list(str(local_colour))
            if i < len(Digit_ARR):
                temp[-1] = Digit_ARR[i]
            else:
                temp[-1] = "0"
            colour_arr[i] = int("".join(temp))
    return (colour_arr)

def get_combined_last_digit(colour_arr):
    """
    Retrieve the last digit of each color channel in an RGB tuple and combine them into a single value.
    get_combined_last_digit([1,2,3]) => 12


    Parameters:
    - rgb_tuple (tuple): RGB color tuple.

    Returns:
    - int: Combined value based on the last digits of each color channel.
    """
    arr = [(str(Number)[-1]) for Number in colour_arr[:3]]
    count = arr.count(arr[0])
    if count == 3:
        return int(arr[0])
    else:
        return int("".join(arr[:2]))

def Encode_V1(img, Color_Array):
    """
    Encode_V1 embeds a message into an image by modifying pixel colors sequentially based on the provided Color_Array.

    Parameters:
    - img (PIL.Image.Image): Input image.
    - Color_Array (list): List of integers representing the message to be encoded.

    Returns:
    - PIL.Image.Image: Image with the encoded message.
    """
    
    n = 0
    for y in range(2, img.size[1] - 4):
        for x in range(2, img.size[0] - 4, 2):
            if n < len(Color_Array):
                img.putpixel((x,y), (Color_Array[n], Color_Array[n], Color_Array[n]))
                n = n + 1
            else:
                img.putpixel((x,y+0), (0, 255, 0))
                img.putpixel((x,y+1), (0, 255, 0))
                img.putpixel((x,y+2), (0, 255, 0))
                img.putpixel((x,y+3), (0, 255, 0))
                return img

def Encode_V2(img, Color_Array):
    """
    This algorithm iterates through the image, modifying pixels based on specific conditions.
    The message is encoded by replacing selected pixels with values from Color_Array.

    Parameters:
    - img (PIL.Image.Image): Input image.
    - Color_Array (list): List of integers representing the message to be encoded.

    Returns:
    - PIL.Image.Image: Image with the encoded message.
    """
    
    n = 0
    for y in range(2, img.size[1] - 4, 3):
        for x in range(2, img.size[0] - 4):
            if n < len(Color_Array):
                TL = img.getpixel((x-1, y-1))[0]
                TR = img.getpixel((x+1, y-1))[0]
                BL = img.getpixel((x-1, y+1))[0]
                BR = img.getpixel((x+1, y+1))[0]

                if (TL * TR * BL * BR) != 0 and TL % 3 == 0 and TR % 3 == 0 and BL % 2 == 0 and BR % 2 == 0:
                    img.putpixel((x,y), (Color_Array[n], Color_Array[n], Color_Array[n]))
                    n = n + 1
            else:
                img.putpixel((x+1,y+1), (255, 0, 0))
                img.putpixel((x+2,y+2), (255, 0, 0))
                img.putpixel((x+3,y+3), (255, 0, 0))
                return img

def Encode_V3(img, Color_Array):
    """
    This algorithm improves concealment by subtracting Color_Array values from the left pixel.
    It iterates through the image, modifying pixels based on specific conditions.

    Parameters:
    - img (PIL.Image.Image): Input image.
    - Color_Array (list): List of integers representing the message to be encoded.

    Returns:
    - PIL.Image.Image: Image with the encoded message.
    """
    n = 0
    for y in range(2, img.size[1] - 4, 3):
        for x in range(2, img.size[0] - 4, 3):
            if n < len(Color_Array):
                TL = img.getpixel((x-1, y-1))[0]
                TR = img.getpixel((x+1, y-1))[0]
                BL = img.getpixel((x-1, y+1))[0]
                BR = img.getpixel((x+1, y+1))[0]

                if (TL * TR * BL * BR) != 0 and TL % 3 == 0 and TR % 3 == 0 and BL % 2 == 0 and BR % 2 == 0:
                    # Get Values for 1 pixels to the left, then minus the Color_array from it.
                    LR, LG, LB = img.getpixel((x-1, y))
                    R, G, B = LR - Color_Array[n], LG - Color_Array[n], LB - Color_Array[n]
                    img.putpixel((x,y), (R, G, B))
                    n = n + 1
            else:
                img.putpixel((x+1,y+1), (255, 0, 0))
                img.putpixel((x+2,y+2), (255, 0, 0))
                img.putpixel((x+3,y+3), (255, 0, 0))
                return img

def Encode_V4(img, Color_Array):
    """
    This algorithm enhances concealment by considering the left pixel and additional conditions.
    It iterates through the image, modifying pixels based on specific criteria.

    Parameters:
    - img (PIL.Image.Image): Input image.
    - Color_Array (list): List of integers representing the message to be encoded.

    Returns:
    - PIL.Image.Image: Image with the encoded message.
    """
    n = 0
    for y in range(3, img.size[1] - 5, 3):
        for x in range(3, img.size[0] - 5, 3):
            if n < len(Color_Array):
                TL = img.getpixel((x-1, y-1))[0]
                TR = img.getpixel((x+1, y-1))[0]
                BL = img.getpixel((x-1, y+1))[0]
                BR = img.getpixel((x+1, y+1))[0]

                if (TL * TR * BL * BR) != 0 and TL % 3 == 0 and TR % 3 == 0 and BL % 2 == 0 and BR % 2 == 0:
                    Current_pix = img.getpixel((x, y))
                    if Current_pix[0] < 250 and Current_pix[1] < 250 and Current_pix[2] < 250:
                        R, G, B = set_last_digit_in_rgb(Current_pix, Color_Array[n])
                        img.putpixel((x,y), (R, G, B))
                        Current_pix = img.getpixel((x, y))
                        n = n + 1

            else:
                px1 = img.getpixel((x+1, y+1))
                R1, G1, B1 = set_last_digit_in_rgb(px1, 12)
                img.putpixel((x+1,y+1), (R1, G1, B1))

                px2 = img.getpixel((x+2, y+2))
                R2, G2, B2 = set_last_digit_in_rgb(px2, 34)
                img.putpixel((x+2,y+2), (R2, G2, B2))


                px3 = img.getpixel((x+3, y+3))
                R3, G3, B3 = set_last_digit_in_rgb(px3, 56)
                img.putpixel((x+3,y+3), (R3, G3, B3))


                px4 = img.getpixel((x+4, y+4))
                R4, G4, B4 = set_last_digit_in_rgb(px4, 78)
                img.putpixel((x+4,y+4), (R4, G4, B4))

                return img

def encode_and_save(msg, sourceImgName, outputImgName, encryptFunc):
    """
    Encode a message into an image using a specified encryption function and save the result.

    Parameters:
        msg (str): The message to be encoded.
        sourceImgName (str): The filename of the source image.
        outputImgName (str): The filename for the encoded image to be saved.
        encryptFunc (function): Valid encryption functions: Encode_V1, Encode_V2, Encode_V3, Encode_V4.
    """
    print(f"Encoding with {encryptFunc.__name__}: '{msg}'")
    img = Image.open(sourceImgName)
    Color_Array = convert_message_to_color_indices(msg)
    img = encryptFunc(img, Color_Array)
    img.save(outputImgName)
    
def get_last_digit_in_rgb(colour_arr):
    arr = [(str(Number)[-1]) for Number in colour_arr[:3]]
    count = arr.count(arr[0])
    if count == 3:
        return int(arr[0])
    else:
        return int("".join(arr[:2]))

def decode_color_indices_to_message(Color_Array):
    Decoded_array = []
    chars = list(string.ascii_letters + string.digits + " ")


    for Color_value in Color_Array:
        if Color_value < len(chars):
            letter = chars[Color_value]
            Decoded_array.append(letter)
    Decoded_Message = "".join(Decoded_array)
    return Decoded_Message

def Decode_V1(img):
    """ 
    This functions decodes sequentially modified pixels.
    """
    start = False
    Color_Array = []
    for y in range(2, img.size[1] - 4, 1):
        for x in range(2, img.size[0] - 4, 2):

            if img.getpixel((x, y)) == img.getpixel((x, y+1)) == img.getpixel((x, y+2)) == img.getpixel((x, y+3)) == (0, 255, 0):
                return  Color_Array

            px = img.getpixel((x, y))[0]
            Color_Array.append(px)

    return Color_Array

def Decode_V2(img):
    """ 
    This functions decodes the algorithm which iterates through the image, modifying pixels based on specific conditions.
    """
    Color_Array = []
    for y in range(2, img.size[1] - 4, 1):
        for x in range(2, img.size[0] - 4):
            TL = img.getpixel((x-1, y-1))[0]
            TR = img.getpixel((x+1, y-1))[0]
            BL = img.getpixel((x-1, y+1))[0]
            BR = img.getpixel((x+1, y+1))[0]
  
            if img.getpixel((x+1, y+1)) == img.getpixel((x+2, y+2)) == img.getpixel((x+3, y+3)) == (255, 0, 0):
                return  Color_Array

            if (TL * TR * BL * BR) != 0 and TL % 3 == 0 and TR % 3 == 0 and BL % 2 == 0 and BR % 2 == 0:
                val = img.getpixel((x, y))[0]
                Color_Array.append(val)
    return Color_Array

def Decode_V3(img):
    """This functions decodes the algorithm with improved concealment by subtracting Color_Array values from the left pixel.
    """
    Color_Array = []
    for y in range(2, img.size[1] - 4, 3):
        for x in range(2, img.size[0] - 4, 3):
            TL = img.getpixel((x-1, y-1))[0]
            TR = img.getpixel((x+1, y-1))[0]
            BL = img.getpixel((x-1, y+1))[0]
            BR = img.getpixel((x+1, y+1))[0]
  
            if img.getpixel((x+1, y+1)) == img.getpixel((x+2, y+2)) == img.getpixel((x+3, y+3)) == (255, 0, 0):
                return  Color_Array

            if (TL * TR * BL * BR) != 0 and TL % 3 == 0 and TR % 3 == 0 and BL % 2 == 0 and BR % 2 == 0:
                Left_one = img.getpixel((x-1, y))
                LR, LG, LB = Left_one
                Current_pix = img.getpixel((x, y))
                CR, CG, CB = Current_pix
                R, G, B = LR - CR, LG - CG, LB - CB
                if R == G == B and R != 0 and R > 0:
                    Color_Array.append(R)
    return Color_Array

def Decode_V4(img):
    """This function decodes the algorithm  which considers the left pixel and additional conditions.
    """
    Color_Array = []
    for y in range(3, img.size[1] - 5, 3):
        for x in range(3, img.size[0] - 5, 3):
            TL = img.getpixel((x-1, y-1))[0]
            TR = img.getpixel((x+1, y-1))[0]
            BL = img.getpixel((x-1, y+1))[0]
            BR = img.getpixel((x+1, y+1))[0]
  
            if get_last_digit_in_rgb(img.getpixel((x+1, y+1))) == 12 and get_last_digit_in_rgb(img.getpixel((x+2, y+2))) == 34 and get_last_digit_in_rgb(img.getpixel((x+3, y+3))) == 56 and get_last_digit_in_rgb(img.getpixel((x+4, y+4))) == 78:
                return Color_Array
            
            if (TL * TR * BL * BR) != 0 and TL % 3 == 0 and TR % 3 == 0 and BL % 2 == 0 and BR % 2 == 0:
                Current_pix = img.getpixel((x, y))
                if Current_pix[0] < 250 and Current_pix[1] < 250 and Current_pix[2] < 250:
                    val = get_last_digit_in_rgb(Current_pix)
                    Color_Array.append(val)

    return Color_Array

def decode_IMG(encryptedImgName, encryptFunc):
    """
    Decode an encrypted image using a specified decryption function.

    Parameters:
        encryptedImgName (str): The filename of the encrypted image.
        encryptFunc (function): Valid decryption functions: Decode_V1, Decode_V2, Decode_V3, Decode_V4.

    Returns:
        str: The decoded message extracted from the encrypted image.
    """
    img = Image.open(encryptedImgName)
    Color_Array = encryptFunc(img)
    Decoded_Message = decode_color_indices_to_message(Color_Array)
    return Decoded_Message


if __name__ == "__main__":
    Encoded_Message = "This program will hide this message into the pixelData of an image of your choosing. Hopefully in a way that is difficult to detect."
 
    encode_and_save(Encoded_Message, 'image.png', 'encoded.png', Encode_V1)
    
    decoded_Message = (decode_IMG("encoded.png", Decode_V1))

    print(decoded_Message)