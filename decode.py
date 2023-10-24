from PIL import Image

def text_to_bin(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary


def encode_lsb(image_path, text):
    img = Image.open('40.png')
    binary_text = text_to_bin(text)

    width, height = img.size
    max_chars = (width * height * 3) // 8

    if len(binary_text) > max_chars:
        raise ValueError(f"Text too long to encode in this image. Maximum characters: {max_chars}")

    binary_text += '1111111111111110'  # Adding the stop sequence

    data_index = 0
    encoded_pixels = []
    for pixel in img.getdata():
        new_pixel = list(pixel)

        for i in range(3):
            if data_index < len(binary_text):
                new_pixel[i] = pixel[i] & 0xFE | int(binary_text[data_index])
                data_index += 1

        encoded_pixels.append(tuple(new_pixel))

    encoded_img = Image.new('RGB', (width, height))
    encoded_img.putdata(encoded_pixels)
    return encoded_img

def decode_lsb(image_path):
    img = Image.open('40.png')
    binary_text = ''

    for pixel in img.getdata():
        for i in range(3):
            binary_text += str(pixel[i] & 1)

    binary_chunks = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]

    decoded_text = ''.join([chr(int(chunk, 2)) for chunk in binary_chunks])
    return decoded_text.split('1111111111111110')[0]

# Example usage to encode and decode
encoded_image = encode_lsb('40.png', 'Hello, this is a hidden message!')
encoded_image.save('encoded_image.png')

decoded_text = decode_lsb('encoded_image.png')

