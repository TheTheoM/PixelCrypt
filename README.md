# PixelCrypt
A simple CLI python program that takes an image, and a string and subtly modifies the pixel data to encode that image. 4 current encoding and current decoding algorithms, more will be added in the future. You must use the same to encode or decode. 

### Note:

The currently-implement algorithms 1-3 are basic and easily identifiable. V4 is extremely hard to tell if applied, however is the least dense and works best with high resolution pixels with a variety of pixel-data (i.e. no single tones like an all white picture). Observe the two files in examples to see for yourself.

## Usage

### Encoding a Message
```bash
python PixelCrypt.py encode "Your dangerous message" source_image.png encoded_image.png Encode_V1
```
- msg: The message to be encoded.
- sourceImgName: The filename of the source image.
- outputImgName: The filename for the encoded image to be saved.
- encryptFunc: Encryption function to be applied. Choose from Encode_V1, Encode_V2, Encode_V3, Encode_V4.

### Decoding an Encoded Image

```bash
python PixelCrypt.py decode encoded_image.png Decode_V1
```
- sourceImgName: The filename of the encoded image.
- encryptFunc: Decryption function to be applied. Choose from Decode_V1, Decode_V2, Decode_V3, Decode_V4.

# Examples:

## Encoding:
```bash
python PixelCrypt.py encode "Hello, World!" input_image.png output_image.png Encode_V4
```
## Decoding:
```bash
python PixelCrypt.py decode output_image.png Decode_V4
```
