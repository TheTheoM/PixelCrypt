# PixelCrypt
A simple python program that takes an image, and a string and subtly modifies the pixel data to encode that image. 4 current encoding and current decoding algorithms, more will be added in the future. You must use the same to encode or decode. 

##Usage

### Encoding a Message

```python
Encoded_Message = "This program will hide this message into the pixelData of an image of your choosing. Hopefully in a way that is difficult to detect."

# Example usage with Encode_V4 encryption function. 
encode_and_save(Encoded_Message, 'image.png', 'encoded.png', Encode_V4)
```

###Decoding an Encoded Image

```python
# Example usage with Decode_V4 decryption function
decoded_Message = decode_IMG("encoded.png", Decode_V4)

print(f"Decoded: {decoded_Message}")
```


