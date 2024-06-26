'''
There is a correlation between LAB color space coordinates and color temperatures.

Although it's not direct. LAB color space represents colors based on perceptual attributes (lightness, a*, b*) rather than directly representing temperature.

Color temperature, on the other hand, is a characteristic of the light source's spectral distribution and is typically associated with hues ranging from warm (low color temperatures, around 2000-3000K, like candlelight) to cool (high color temperatures, around 5000-6500K, like daylight).

While LAB coordinates can give insight into the perceived color attributes (such as warmth or coolness), they don't directly correlate to specific color temperatures. For instance, a color in the LAB space might appear warm or cool based on its a* (green-red) and b* (blue-yellow) values, but these attributes do not translate directly into a specific color temperature like 3000K or 6500K.

以下有簡易轉換, 但是好像有點問題
'''



'''
color temperature -> LAB

Explanation:
Convert LAB to RGB: First, convert the LAB color to RGB using cv2.cvtColor from OpenCV.
OpenCV expects the LAB color to be a 3-channel numpy array of type np.uint8.

Calculate Color Temperature: Once you have the RGB values, you can estimate the color temperature using a formula based on the RGB values.
This formula estimates the correlated color temperature (CCT) based on the chromaticity coordinates (x, y) of the color.

Output: The function returns the estimated color temperature in Kelvin (K).

Notes:
This conversion provides an approximation of the color temperature based on the RGB values derived from the LAB color space.
It's not a direct mapping but can give you a rough estimate of how "warm" or "cool" a color might appear.
Adjustments might be necessary depending on the specific application and accuracy requirements.
Make sure to adjust the lab_color variable with the LAB values you want to convert in the example usage section.
'''
import cv2
import numpy as np

def lab_to_color_temperature(lab_color):
    # Convert LAB to RGB
    lab_color = np.array(lab_color, dtype=np.uint8)
    lab_color = np.reshape(lab_color, (1, 1, 3))  # Reshape for OpenCV's conversion
    rgb_color = cv2.cvtColor(lab_color, cv2.COLOR_LAB2RGB)

    # Calculate color temperature approximation
    r, g, b = rgb_color[0, 0].astype(np.float64)
    temperature = None

    if r == g == b:
        temperature = 0  # Undefined or achromatic color

    else:
        x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / (r + g + b)
        y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / (r + g + b)
        n = (x - 0.3320) / (0.1858 - y)

        # Calculate correlated color temperature
        temperature = 449 * (n ** 3) + 3525 * (n ** 2) + 6823.3 * n + 5520.33

    return temperature

# Example usage
lab_color = [50, 0, 0]  # Example LAB color, adjust as needed
temperature = lab_to_color_temperature(lab_color)
print(f"Estimated color temperature: {temperature:.2f} K")



'''
LAB -> color temperature

Explanation:
Convert Color Temperature to RGB: First, convert the given color temperature to RGB.
The method used here is a simplified approximation that maps a given color temperature to approximate RGB values.

Convert RGB to LAB: Once you have the RGB values, convert them to LAB using cv2.cvtColor from OpenCV.

Output: The function returns the LAB color as a numpy array of [L, a, b].

Notes:
The conversion from color temperature to RGB is a rough approximation and might not perfectly match the true spectral distribution of light sources at different temperatures.
Adjustments might be needed based on specific requirements or accuracy levels.
This approach provides a basic method to convert from color temperature to LAB color space, allowing you to work reversibly between these two representations.
Adjust the temperature variable in the example usage section to convert different color temperatures.
'''
import cv2
import numpy as np

def color_temperature_to_lab(temperature):
    # Convert color temperature to RGB
    x = (temperature - 2000.0) / 10000.0
    if x <= 0:
        r = 255
        g = 0
    elif x >= 1:
        r = 0
        g = 0
    elif x < 0.33:
        r = int(255 * (0.33 - x) / 0.33)
        g = int(255 * x / 0.33)
    elif x < 0.66:
        r = int(255 * (0.66 - x) / 0.33)
        g = int(255 * (x - 0.33) / 0.33)
    else:
        r = 0
        g = int(255 * (1 - x) / 0.34)
    b = int(255 - (r + g))
    rgb_color = np.array([[[r, g, b]]], dtype=np.uint8)

    # Convert RGB to LAB
    lab_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2LAB)
    lab_color = lab_color[0, 0]

    return lab_color
# Example usage
temperature = 5000  # Example color temperature in Kelvin, adjust as needed
lab_color = color_temperature_to_lab(temperature)
print(f"LAB color: {lab_color}")

