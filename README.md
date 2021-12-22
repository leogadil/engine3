

# Foobar

Engine 3 is the third iteration of the Samantha Engine. Third iteration because I'm still learning python and I've been applying what I've learned since then. Samantha engine is the core and the framework of what an assistant interface might look like. its design is modular so it's easy to add functionality to the framework.

## Installation

this is built on Python 3.9+. didn't check if it runs on older version of Python

```bash
pip install -r requirements.txt
```

## Usage

```python
import imports # to add the framework folder to the sys.path | will come up with a better idea to do this better
import personalassistant as pa #importing the framework

class Samantha(pa.engine): # here. <---------------

    def __init__(self) -> None:
        super().__init__(self)
        self.name = "Samantha"
        self.version = "0.0.1"
        self.description = "A female personal assistant"
        self.author = "Jann Leo Gadil"

        self.initialize() # initialize before running. this will initiate all core components.
        self.run() # will load all non-essentials but features of the engine

if __name__ == '__main__':
    Samantha()
```

## Configuration
Don't forget to add the configuration file where? `framework/config.json`. This is the format.

> **THIS IS VERY IMPORTANT!!! FRAMEWORK WILL NEVER WORK IF CONFIG IS MISSING**

```json
{
    "weather": {
        "key": "openweatherapi_key_here",
        "units": "metric",
        "location": "your_default_location"
    }
}
```
> In the future this will be auto-generated but it still on its early stage.

## Contributing
currently, this project is only private and will not accept contributions but please do contact me if you have suggestions, I am open to suggestions.


```python
# this email is very old that's why there's a vlog in it.
$ print("leogadilvlog@gmail.com")
```
or [Issues](https://github.com/leogadil/engine3/issues)



## License
[MIT](https://github.com/leogadil/engine3/blob/master/LICENSE)