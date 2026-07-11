import os
import cv2


def save_image(image, output_folder="outputs", filename="best_slice.png"):

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, filename)

    cv2.imwrite(output_path, image)

    print("\nImage Saved Successfully")
    print(output_path)

    return output_path