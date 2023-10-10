"""Name-en-US: sRGB to ACEScg
Description US: Converts sRGB colors to ACEScg colors.

## Installation & Usage

1. Install OpenColorIO:  

You can install OpenColorIO using pip by running the following command in your terminal:

> pip install opencolorio

2. Create a Python script:

Create a new file called `srgb_to_acescg.py` in your preferred code editor.

3. Copy and paste the script:

Copy and paste the Python script from my previous answer into the srgb_to_acescg.py file.

4. Save the file:

Save the srgb_to_acescg.py file in your preferred directory.

5. Run the script:

In your terminal, navigate to the directory where you saved the srgb_to_acescg.py file and run the following command:

```
python srgb_to_acescg.py
```

## Usage

"""

import OpenColorIO as OCIO

def main():
    # Define the sRGB 0-255 RGB color values
    srgb_color = [255, 0, 0]

    # Create an OpenColorIO Config object
    config = OCIO.Config().CreateFromEnv()

    # Create a ColorSpace object for the input sRGB color space
    input_colorspace = OCIO.ColorSpace(name='sRGB', family='sRGB', equalityGroup='', bitDepth=OCIO.Constants.BIT_DEPTH_UINT8,
                                    isData=False, allocation=OCIO.Constants.ALLOCATION_LG2)

    # Create a ColorSpace object for the output ACEScg color space
    output_colorspace = OCIO.ColorSpace(name='ACEScg', family='ACES', equalityGroup='', bitDepth=OCIO.Constants.BIT_DEPTH_F32,
                                        isData=False, allocation=OCIO.Constants.ALLOCATION_LG2)

    # Create a ColorTransformation object to convert from the input sRGB color space to the output ACEScg color space
    transform = OCIO.ColorTransformation(src=input_colorspace, dst=output_colorspace)

    # Create an ImageDesc object for the input sRGB color values
    image_desc = OCIO.ImageDesc(width=1, height=1, numChannels=3, channelNames=['R', 'G', 'B'], channelOrder=OCIO.Constants.CHANNEL_ORDER_RGB,
                                data=srgb_color, interleaved=True)

    # Apply the color transformation to the input sRGB color values to get the output ACEScg color values
    transformed_color = config.getProcessor(transform).applyRGB(image_desc).getData()

    # Print the output ACEScg color values
    print('ACEScg color:', transformed_color)

if __name__ == "__main__":
    main()