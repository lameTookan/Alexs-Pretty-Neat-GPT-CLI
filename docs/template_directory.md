
# Configuration Overview

These are the various built in templates(contained in `templates.json`) for this project. Check out the template documentation for more information on how to create your own templates.


## GPT-3 Configurations

1. **gpt-3_creative**
   - This configuration provides creative and varied responses.
   - It uses the 'gpt-3.5-turbo-16k' model.
   - The temperature is set to 0.8 which allows for more randomness in the output.

2. **gpt-3_small**
   - This is a scaled-down version of the gpt-3 settings, limiting output to a smaller token count.
   - It uses the 'gpt-3.5-turbo-16k' model.
   - The temperature is set to 0.5 which allows for moderate randomness in the output.

3. **gpt-3_default**
   - This configuration represents default settings for gpt-3.
   - It uses the 'gpt-3.5-turbo-16k' model.
   - The temperature is set to 0.5 which allows for moderate randomness in the output.

4. **gpt-3_experimental**
   - As the name suggests, it has experimental settings with higher temperature and top_p values.
   - It uses the 'gpt-3.5-turbo-16k' model.
   - The temperature is set to 0.8 allowing more randomness in output, while top_p (controlling diversity) is set at 0.9.

5. **gpt-3_conservative**
    - It produces less varied responses due to its lower temperature setting of 0.2.
    - It uses the 'gpt-3.5-turbo-16k' model.

## GPT-4 Configurations

1. **gpt-4_creative**
    - Designed for more creative responses with a higher temperature setting of 1.5.
    - It uses gpt-4 as its base model.

2. **gpt_4_conservative**
    - This configuration produces less varied responses due to its lower temperature setting of 0.2.
    - It also runs on gpt_4 as its base model.

3 .**gpt_4_default**
     - Default settings for gpt_4 with a moderate temperature setting of 0.7
     - Frequency penalty has been applied (value: 0.5) and top_p (for controlling diversity) is set at 1.

4 .**gtp_4_small**
      - A cost-saving configuration that limits number of messages to save on token usage
      - Temperature has been set at 0,5 and top_p (for controlling diversity) is again kept at 1

Remember that changing these parameters can significantly alter your AI's behavior, so it's important to experiment and find what works best for your specific use case!
