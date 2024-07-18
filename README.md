# Save the Script
Place the Scripts in the Maya scripts directory:
`Windows: C:\Users\<user>\Documents\maya\scripts\`
`Linux: /home/<user>/maya/scripts/`

# Run the relinker
Run the following in the script editor:
```
import texture_relinker
wind = texture_relinker.RelinkTextureMain()
wind.show()
```
This can also be higlighted, middle mouse button dragged to a shelf to create a button